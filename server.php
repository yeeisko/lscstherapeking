<?php
// index.php

$request_uri = $_SERVER['REQUEST_URI'];

// Helper function to serve a file with correct headers
function serve_file($filepath) {
    if (file_exists($filepath)) {
        // Determine content type based on file extension
        $ext = pathinfo($filepath, PATHINFO_EXTENSION);
        $mime_types = [
            'html' => 'text/html',
            'htm' => 'text/html',
            // add more mime types if needed
        ];
        header('Content-Type: ' . ($mime_types[$ext] ?? 'application/octet-stream'));
        readfile($filepath);
        exit;
    } else {
        http_response_code(404);
        echo "404 Not Found";
        exit;
    }
}

switch ($request_uri) {
    case '/':
        serve_file(__DIR__ . '/index.html');
        break;

    case '/uploads/index1.html':
        serve_file(__DIR__ . '/uploads/index1.html');
        break;

    case '/uploads/Chibadirectinstall.html':
        serve_file(__DIR__ . '/uploads/Chibadirectinstall.html');
        break;

    case '/app-access.html':
        serve_file(__DIR__ . '/app-access.html');
        break;

    case '/uploads/arabbank.html':
        serve_file(__DIR__ . '/uploads/arabbank.html');
        break;

    default:
        http_response_code(404);
        echo "404 Not Found";
        break;
}
