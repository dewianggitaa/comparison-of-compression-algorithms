import React, { useState } from 'react';

function App() {
    const [selectedFile, setSelectedFile] = useState(null);
    const [uploadedImageUrl, setUploadedImageUrl] = useState(null);

    const handleFileChange = (event) => {
        setSelectedFile(event.target.files[0]);
    };

    const handleUpload = async () => {
        if (!selectedFile) return;

        const formData = new FormData();
        formData.append('files[]', selectedFile);

        try {
        const response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const blob = await response.blob();
        const imageUrl = URL.createObjectURL(blob);
        setUploadedImageUrl(imageUrl);
        } catch (error) {
        console.error('Error uploading the file:', error);
        }
    };

    return (
        <div className="App">
        <h1>Image Compressor</h1>
        <input type="file" onChange={handleFileChange} />
        <button onClick={handleUpload}>Compress</button>
        {uploadedImageUrl && (
            <div>
            <h2>Uploaded Image:</h2>
            <img src={uploadedImageUrl} alt="Uploaded" />
            </div>
        )}
        </div>
    );
}

export default App;
