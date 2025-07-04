const express = require('express');
const multer = require('multer');
const path = require('path');
const crypto = require('crypto');
const fs = require('fs');

const app = express();
const PORT = process.env.PORT || 3000;

// Serve static files from 'public'
app.use(express.static('public'));

// Create upload directory if it doesn't exist
const uploadPath = path.join(__dirname, 'file-uploader');
if (!fs.existsSync(uploadPath)) {
  fs.mkdirSync(uploadPath);
}

// Multer setup for random file names
const storage = multer.diskStorage({
  destination: (req, file, cb) => cb(null, uploadPath),
  filename: (req, file, cb) => {
    const ext = path.extname(file.originalname);
    const randomID = crypto.randomBytes(6).toString('hex').toUpperCase(); // 12 chars
    cb(null, `${randomID}${ext}`);
  }
});
const upload = multer({ storage });

// Upload route
app.post('/upload', upload.single('file'), (req, res) => {
  if (!req.file) return res.status(400).send('No file uploaded.');

  const fileUrl = `${req.protocol}://${req.get('host')}/file-uploader/${req.file.filename}`;
  res.send(`File uploaded! <a href="${fileUrl}">${fileUrl}</a>`);
});

// Serve uploaded files
app.use('/file-uploader', express.static(path.join(__dirname, 'file-uploader')));

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});

