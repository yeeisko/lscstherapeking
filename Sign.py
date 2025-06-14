# server.py (example backend in Python using Flask to connect with previous script)

import os
import tempfile
from flask import Flask, request, send_file, abort
import subprocess

app = Flask(__name__)

def run_sign_script(ipa_path, output_path, p12_path, p12_password, mobileprovision_path, identity):
    # Call the previous sign.py script here. Adapt path accordingly.
    cmd = [
        'python3', 'sign.py',
        '--input', ipa_path,
        '--output', output_path,
        '--p12', p12_path,
        '--p12-password', p12_password,
        '--mobileprovision', mobileprovision_path,
        '--identity', identity
    ]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        raise Exception(result.stderr)
    return output_path

@app.route('/sign', methods=['POST'])
def sign_ipa():
    if not all(k in request.files or k in request.form for k in ('ipa', 'p12', 'mobileprovision')):
        abort(400, "Missing required files")

    ipa = request.files['ipa']
    p12 = request.files['p12']
    mobileprovision = request.files['mobileprovision']
    p12_password = request.form.get('p12_password', '')
    identity = request.form.get('identity', '')

    if not ipa or not p12 or not mobileprovision or not p12_password or not identity:
        abort(400, "Missing required parameters")

    with tempfile.TemporaryDirectory() as tmpdir:
        ipa_path = os.path.join(tmpdir, 'input.ipa')
        ipa.save(ipa_path)
        p12_path = os.path.join(tmpdir, 'cert.p12')
        p12.save(p12_path)
        mobileprovision_path = os.path.join(tmpdir, 'profile.mobileprovision')
        mobileprovision.save(mobileprovision_path)
        output_path = os.path.join(tmpdir, 'signed.ipa')

        try:
            run_sign_script(ipa_path, output_path, p12_path, p12_password, mobileprovision_path, identity)
            return send_file(output_path, as_attachment=True, download_name='signed.ipa')
        except Exception as e:
            return f"Signing failed:\n{str(e)}", 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
