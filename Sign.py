<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Upload IPA File</title>
</head>
<body>
  <h1>Upload your IPA file</h1>
  <form id="uploadForm" enctype="multipart/form-data" method="post">
    <input type="file" id="ipaFile" name="ipa" accept=".ipa" required />
    <button type="submit">Upload</button>
  </form>
  <p id="result"></p>

  <script>
    document.getElementById('uploadForm').addEventListener('submit', async function(e) {
      e.preventDefault();
      const fileInput = document.getElementById('ipaFile');
      if (!fileInput.files.length) {
        alert('Please select an IPA file');
        return;
      }

      const file = fileInput.files[0];
      if (!file.name.endsWith('.ipa')) {
        alert('Only .ipa files are allowed');
        return;
      }

      const formData = new FormData();
      formData.append('ipa', file);

      try {
        const response = await fetch('/upload', {
          method: 'POST',
          body: formData
        });

        if (!response.ok) {
          const errorText = await response.text();
          document.getElementById('result').innerText = 'Error: ' + errorText;
          return;
        }

        const text = await response.text();
        // Show direct download link
        document.getElementById('result').innerHTML = text;
      } catch (err) {
        document.getElementById('result').innerText = 'Upload failed: ' + err.message;
      }
    });
  </script>
</body>
</html>
