import './App.css';
import {BrowserRouter, Routes, Route} from "react-router-dom"
import { LandingPage, CompressAudio, CompressImage } from './component';

function App() {
  return (
    <>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<LandingPage/>}/>
          <Route path="/compress-audio" element={<CompressAudio/>}/>
          <Route path="/compress-image" element={<CompressImage/>}/>
        </Routes>
      </BrowserRouter>
    </>
  );
}

export default App;
