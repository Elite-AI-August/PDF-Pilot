import React, { useEffect } from 'react';
import Chatbot from "./Chatbot";
import Draggable from 'react-draggable';
import './App.css';

function App() {
  const imageUrl = `${process.env.PUBLIC_URL}/logo.png`;

  useEffect(() => {
    const timer = setTimeout(() => {
      const movingImage = document.getElementById('moving-image');
      movingImage.style.transform = 'translate(35px, -240px)';
    }, 100);

    return () => clearTimeout(timer);
  }, []);

  const onImageFollowMouse = () => {
    const movingImage = document.getElementById('moving-image');
    movingImage.style.position = 'fixed';
    movingImage.style.pointerEvents = 'none';
  
    const rect = movingImage.getBoundingClientRect();
    let mouseX = rect.x;
    let mouseY = rect.y;
    let currentX = rect.x;
    let currentY = rect.y;
    const acceleration = 0.03;
  
    const updateMousePosition = (e) => {
      mouseX = e.clientX - movingImage.clientWidth / 2;
      mouseY = e.clientY - movingImage.clientHeight * 2 + 780;
    };
  
    const moveImage = () => {
      currentX += (mouseX - currentX) * acceleration;
      currentY += (mouseY - currentY) * acceleration;
  
      movingImage.style.left = `${currentX}px`;
      movingImage.style.top = `${currentY}px`;
  
      requestAnimationFrame(moveImage);
    };
  
    window.addEventListener('mousemove', updateMousePosition);
    requestAnimationFrame(moveImage);
  };
  
  

  return (
    <div className="App">
      <header className="App-header">
        <Draggable defaultPosition={{ x: 50, y: 0 }}>
          <img id="moving-image" className="App-logo" src={imageUrl} alt="Application Logo" />

        </Draggable>
        <div className="App-chatbot-wrapper">
          <div className="App-chatbot">
            <Chatbot onImageFollowMouse={onImageFollowMouse} />
          </div>
        </div>
      </header>
    </div>
  );
}

export default App;
