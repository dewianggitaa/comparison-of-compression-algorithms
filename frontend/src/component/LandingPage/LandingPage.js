import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import "../Navbar/Naavbar"
import Naavbar from '../Navbar/Naavbar';

function App() {
    
    return(
        <div class="grid h-screen bg-blue">
            <Naavbar/>
            <div class="grid place-content-center">
                <div class="bg-pink px-32 py-8 text-center grid place-items-center border border-spacing-1 border-dark-blue">
                    <div class="text-center text-3xl font-press-start text-cream">Commparaison</div>
                    <div class="text-center text-3xl font-press-start text-cream">Algortihm</div>
                    <div class="text-center text-3xl font-press-start text-cream">Compression</div>
                    <div class="w-60">
                        <div>halo halo halo halo halo halo halo halo halo halo halo halo halo halo halo halo halo halo hlo halo</div>
                    </div> 
                </div>
                <div class="grid place-content-center mt-6">
                    <div class="flex justify-between gap-40">
                        <Link to="/compress-image">
                            <button class="px-5 bg-white">Image Compression</button>
                        </Link>
                        <Link to="/compress-audio">
                            <button class="px-5 bg-white">Audio Compression</button>
                        </Link> 
                    </div>
                    <div class="flex justify-center mt-4">
                        <Link to="/compress-video">
                            <button class="px-5 text-center bg-white">Video Compression</button>
                        </Link>
                    </div>
                </div>
                
            </div>
            
        </div>
    )
}

export default App;
