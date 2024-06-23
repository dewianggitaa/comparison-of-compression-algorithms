import React, { useState } from 'react';
import Naavbar from '../Navbar/Naavbar';

const CompressImage = () => {
    const [selectedFile, setSelectedFile] = useState(null);
    const [dctImageUrl, setDctImageUrl] = useState(null);
    const [dwtImageUrl, setDwtImageUrl] = useState(null);

    const handleFileChange = (event) => {
        setSelectedFile(event.target.files[0]);
    };

    const handleUpload = async () => {
        if (!selectedFile) return;

        const formData = new FormData();
        formData.append('files[]', selectedFile);

        try {
            const response = await fetch('/compress-image', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const data = await response.json();
            setDctImageUrl(data.dct_image_url);
            setDwtImageUrl(data.dwt_image_url);
        } catch (error) {
            console.error('Error uploading the file:', error);
        }
    };

    return (
        <div class="grid place-content-center h-screen bg-blue">
            <Naavbar/>
            <div class="text-center text-xl font-bold mb-20">Image Compressor</div>
            <input type="file" onChange={handleFileChange} />
            <button onClick={handleUpload} class="bg-yellow">Compress</button>
            {dctImageUrl && (
                <div>
                    <h2>DCT Compressed Image:</h2>
                    <img src={dctImageUrl} alt="DCT Compressed" className="w-80" />
                </div>
            )}
            {dwtImageUrl && (
                <div>
                    <h2>DWT Compressed Image:</h2>
                    <img src={dwtImageUrl} alt="DWT Compressed" className="w-80" />
                </div>
            )}
        </div>
    );
};

export default CompressImage;
