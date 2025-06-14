from flask import Flask, request, send_from_directory, jsonify
import os
import tempfile
import shutil
import subprocess
import uuid

app = Flask(__name__)
UPLOAD_FOLDER = './uploads'
SIGNED_FOLDER = './signed'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(SIGNED_FOLDER, exist_ok=True)

def unzip_ipa(ipa_path, dest_folder):
    subprocess.check_call(['unzip', '-q', ipa_path, '-d', dest_folder])

def zip_ipa(src_folder, output_path):
    # Zip contents of src_folder into output_path
    cwd = os.getcwd()
    os.chdir(src_folder)
    subprocess.check_call(['zip', '-qr', output_path, '.'])
    os.chdir(cwd)

def codesign_app(app_path, cert_name, p12_path, p12_password):
    # Import p12 first
    keychain_name = tempfile.NamedTemporaryFile().name
    keychain_password = "temp_password"

    # Create temporary keychain
    subprocess.check_call([
        'security', 'create-keychain', '-p', keychain_password, keychain_name
    ])
    subprocess.check_call([
        'security', 'import', p12_path, '-k', keychain_name, '-P', p12_password,
        '-T', '/usr/bin/codesign', '-T', '/usr/bin/security'
    ])
    subprocess.check_call(['security', 'list-keychains', '-s', keychain_name])
    subprocess.check_call(['security', 'unlock-keychain', '-p', keychain_password, keychain_name])

    # Sign app bundle (recursively sign frameworks too)
    # --deep can simplify re-signing child codes
    subprocess.check_call([
        'codesign', '--force', '--timestamp', '--sign', cert_name,
        '--keychain', keychain_name, '--deep', app_path
    ])

    # Delete keychain
    subprocess.check_call(['security', 'delete-keychain', keychain_name])

def replace_profile(app_path, mobileprovision_path):
    embedded_profile_path = os.path.join(app_path, "embedded.mobileprovision")
    shutil.copy(mobileprovision_path, embedded_profile_path)

@app.route('/upload-and-sign', methods=['POST'])
def upload_and_sign():
    ipa_file = request.files.get('ipa')
    p12_file = request.files.get('p12')
    mobileprovision_file = request.files.get('mobileprovision')
    p12_password = request.form.get('p12_password')
    cert_name = request.form.get('cert_name')  # e.g. "iPhone Distribution: Company name"

    if not ipa_file or not p12_file or not mobileprovision_file or not p12_password or not cert_name:
        return jsonify({"error": "Missing file or parameter"}), 400

    # Save uploaded files to temp dir
    work_dir = tempfile.mkdtemp()
    ipa_path = os.path.join(work_dir, "input.ipa")
    p12_path = os.path.join(work_dir, "cert.p12")
    mobileprov_path = os.path.join(work_dir, "profile.mobileprovision")
    ipa_file.save(ipa_path)
    p12_file.save(p12_path)
    mobileprovision_file.save(mobileprov_path)

    # Unzip IPA
    unzip_dir = os.path.join(work_dir, "unzipped")
    os.makedirs(unzip_dir)
    unzip_ipa(ipa_path, unzip_dir)

    # The .app folder is inside Payload/, find it
    payload_path = os.path.join(unzip_dir, "Payload")
    apps = [d for d in os.listdir(payload_path) if d.endswith('.app')]
    if len(apps) == 0:
        shutil.rmtree(work_dir)
        return jsonify({"error": "No .app found in IPA"}), 400
    app_path = os.path.join(payload_path, apps[0])

    # Replace embedded.mobileprovision with uploaded one
    replace_profile(app_path, mobileprov_path)

    try:
        # Sign app
        codesign_app(app_path, cert_name, p12_path, p12_password)
    except subprocess.CalledProcessError as e:
        shutil.rmtree(work_dir)
        return jsonify({"error": "Codesign failed", "detail": str(e)}), 500

    # Create signed IPA
    signed_ipa_name = str(uuid.uuid4()) + ".ipa"
    signed_ipa_path = os.path.join(SIGNED_FOLDER, signed_ipa_name)
    zip_ipa(unzip_dir, signed_ipa_path)

    shutil.rmtree(work_dir)

    download_url = f"/download/{signed_ipa_name}"
    return jsonify({"signed_ipa_url": download_url})

@app.route('/upload-only', methods=['POST'])
def upload_only():
    ipa_file = request.files.get('ipa')
    if not ipa_file:
        return jsonify({"error": "IPA file is required"}), 400
    filename = str(uuid.uuid4()) + ".ipa"
    save_path = os.path.join(UPLOAD_FOLDER, filename)
    ipa_file.save(save_path)
    download_url = f"/download/{filename}"
    return jsonify({"ipa_url": download_url})

@app.route('/download/<filename>', methods=['GET'])
def download(filename):
    # Serve signed or unsigned IPA file
    if filename in os.listdir(UPLOAD_FOLDER):
        return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)
    elif filename in os.listdir(SIGNED_FOLDER):
        return send_from_directory(SIGNED_FOLDER, filename, as_attachment=True)
    else:
        return jsonify({"error": "File not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
