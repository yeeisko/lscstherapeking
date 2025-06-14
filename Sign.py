from flask import Flask, request, send_file, abort, jsonify
import subprocess
import os
import tempfile
import shutil

app = Flask(__name__)

@app.route('/sign-ipa', methods=['POST'])
def sign_ipa():
    # Check all required files and password present
    if 'ipaFile' not in request.files or 'p12File' not in request.files or 'mobileprovisionFile' not in request.files:
        return abort(400, 'Missing one or more files (.ipa, .p12, .mobileprovision)')
    
    p12_password = request.form.get('p12Password')
    if not p12_password:
        return abort(400, 'Missing p12 password')

    ipa_file = request.files['ipaFile']
    p12_file = request.files['p12File']
    mobileprovision_file = request.files['mobileprovisionFile']

    temp_dir = tempfile.mkdtemp()
    try:
        # Save uploaded files temporarily
        input_ipa_path = os.path.join(temp_dir, 'input.ipa')
        ipa_file.save(input_ipa_path)

        p12_path = os.path.join(temp_dir, 'cert.p12')
        p12_file.save(p12_path)

        mobileprovision_path = os.path.join(temp_dir, 'profile.mobileprovision')
        mobileprovision_file.save(mobileprovision_path)

        output_ipa_path = os.path.join(temp_dir, 'signed.ipa')

        # Run signing script
        cmd = [
            'python3', 'Sign.py',
            '--input', input_ipa_path,
            '--output', output_ipa_path,
            '--p12', p12_path,
            '--p12-password', p12_password,
            '--mobileprovision', mobileprovision_path
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print('Sign.py error:', result.stderr)
            return abort(500, 'Failed to sign IPA')

        # Return the signed IPA file as download
        return send_file(output_ipa_path, as_attachment=True, download_name='signed.ipa')

    finally:
        shutil.rmtree(temp_dir)


if __name__ == '__main__':
    app.run(debug=True)
