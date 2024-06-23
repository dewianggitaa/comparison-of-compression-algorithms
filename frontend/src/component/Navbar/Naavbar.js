import React from 'react'
import "./Navbar.css"
import {Link} from 'react-router-dom'

const Naavbar = () => {
    return (
        <div class="fixed flex justify-between w-full bg-blue border border-b-1 border-dark-blue">
            <div>
                <Link to="/">
                    <div class="text-2xl font-bold font-press-start px-8 pt-3">CAC</div>
                </Link>
            </div>
            <div class="px-8 py-3">
                <ul class="flex gap-5">
                    <li class="bg-yellow w-20 text-center p-1 rounded-2xl border border-spacing-1 border-dark-blue">Home</li>
                    <li class="bg-dark-blue w-24 text-center text-white p-1 rounded-2xl border border-spacing-1 border-black">About Us</li>
                    <li class="bg-cream w-20 text-center p-1 rounded-2xl border border-spacing-1 border-dark-blue">Contact</li>
                </ul>
            </div>
            
            
        </div>
    )
}

export default Naavbar