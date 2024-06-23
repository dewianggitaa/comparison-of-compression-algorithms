import React, { useState } from 'react';
import Naavbar from '../Navbar/Naavbar';

const CompressAudio = () => {
    const [selectedMusic, setSelectedMusic] = useState(null);
    const [dctAudioURL, setDctAudioURL] = useState(null);

    const handleFileChange = (event) => {
        setSelectedMusic(event.target.files[0]);
    };

    const handleUpload = async () => {
        if (!selectedMusic) return;

        const formData = new FormData();
        formData.append('files[]', selectedMusic);

        try {
            const response = await fetch('/compress-audio', {
                method: 'POST',
                body: formData,
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const data = await response.json();
            setDctAudioURL(data.dct_audio_url); // Update state with compressed audio URL

        } catch (error) {
            console.error('Error uploading the file:', error);
        }
    };

    return (
        <div className="grid h-screen bg-pink">
            <Naavbar />
            <div className="flex flex-col justify-center h-screen items-center">
                <div>Compress Audio</div>
                <input type="file" onChange={handleFileChange} className="border border-spacing-1 m-4 bg-white" />
                <button onClick={handleUpload} className="bg-yellow p-1 rounded-2xl">
                    Compress
                </button>
                {dctAudioURL && <audio controls src={dctAudioURL} className="mt-4" />}
            </div>
        </div>
    );
};

export default CompressAudio;
