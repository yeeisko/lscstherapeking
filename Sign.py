from flask import Flask, request, send_file, render_template_string
import os
import tempfile
import subprocess
import shutil
import plistlib
import zipfile

app = Flask(__name__)

def run_cmd(cmd, check=True):
    # Runs a shell command
    proc = subprocess.run(cmd, shell=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if check and proc.returncode != 0:
        raise RuntimeError(f"Command failed: {cmd}\nstdout:{proc.stdout}\nstderr:{proc.stderr}")
    return proc.stdout.strip()

def unzip_ipa(ipa_path, extract_to):
    with zipfile.ZipFile(ipa_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)

def zip_ipa(folder_path, output_path):
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, folder_path)
                zipf.write(full_path, rel_path)

def find_app_folder(payload_path):
    # Should be only 1 app folder inside Payload
    for name in os.listdir(payload_path):
        if name.endswith(".app"):
            return os.path.join(payload_path, name)
    raise RuntimeError("Cannot find .app folder inside Payload")

def import_p12_to_keychain(p12_path, p12_password, keychain_name):
    # Import P12 to temporary keychain
    run_cmd(f'security create-keychain -p "" {keychain_name}')
    run_cmd(f'security import {p12_path} -k {keychain_name} -P "{p12_password}" -T /usr/bin/codesign')
    # Unlock keychain and set as default temporarily
    run_cmd(f'security unlock-keychain -p "" {keychain_name}')
    run_cmd(f'security list-keychains -s {keychain_name}')

def delete_keychain(keychain_name):
    run_cmd(f'security delete-keychain {keychain_name}')

def get_signing_identity(keychain_name):
    # Get identity of certificate in keychain
    output = run_cmd(f'security find-identity -v -p codesigning {keychain_name}')
    # Result looks like: 1) CERT_HASH "Name"
    for line in output.splitlines():
        if '"' in line:
            return line.split('"')[1]
    raise RuntimeError("No signing identity found in keychain")

def codesign_item(path, identity, entitlements=None, keychain=None):
    cmd = f'codesign -fs "{identity}" --timestamp=none'
    if entitlements:
        cmd += f' --entitlements "{entitlements}"'
    if keychain:
        cmd += f' --keychain "{keychain}"'
    cmd += f' "{path}"'
    run_cmd(cmd)

def resign_app(app_path, identity, keychain):
    # Sign frameworks first (if exist)
    frameworks_path = os.path.join(app_path, "Frameworks")
    if os.path.exists(frameworks_path):
        for fw in os.listdir(frameworks_path):
            full_fw_path = os.path.join(frameworks_path, fw)
            codesign_item(full_fw_path, identity, keychain=keychain)

    # Sign the main app bundle
    codesign_item(app_path, identity, keychain=keychain)

@app.route('/')
def index():
    # Serve the index.html inline for simplicity
    return render_template_string(open("index.html").read())

@app.route('/sign', methods=['POST'])
def sign():
    p12_file = request.files.get('p12')
    p12_pass = request.form.get('p12pass')
    mobileprovision_file = request.files.get('mobileprovision')
    ipa_file = request.files.get('ipa')

    if not p12_file or not p12_pass or not mobileprovision_file or not ipa_file:
        return "Missing required files or password", 400

    with tempfile.TemporaryDirectory() as tmpdir:
        # Save uploaded files
        p12_path = os.path.join(tmpdir, "cert.p12")
        p12_file.save(p12_path)

        mobileprovision_path = os.path.join(tmpdir, "profile.mobileprovision")
        mobileprovision_file.save(mobileprovision_path)

        ipa_path = os.path.join(tmpdir, "input.ipa")
        ipa_file.save(ipa_path)

        # Unzip IPA
        unzip_dir = os.path.join(tmpdir, "unzip")
        os.mkdir(unzip_dir)
        unzip_ipa(ipa_path, unzip_dir)

        payload_path = os.path.join(unzip_dir, "Payload")
        app_path = find_app_folder(payload_path)

        # Replace embedded.mobileprovision
        embedded_path = os.path.join(app_path, "embedded.mobileprovision")
        shutil.copy(mobileprovision_path, embedded_path)

        # Create temporary keychain to import p12
        keychain_name = os.path.join(tmpdir, "temp.keychain-db")
        import_p12_to_keychain(p12_path, p12_pass, keychain_name)
        try:
            identity = get_signing_identity(keychain_name)

            # Resign app
            resign_app(app_path, identity, keychain_name)

            # Repackage IPA
            output_ipa = os.path.join(tmpdir, "signed.ipa")
            zip_ipa(unzip_dir, output_ipa)

            # Return signed IPA
            return send_file(output_ipa, download_name="signed.ipa", as_attachment=True)

        finally:
            # Clean up the temporary keychain
            delete_keychain(keychain_name)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
