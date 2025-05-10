import React from 'react';
import './BorgesWatchmaker.css'; // We'll create this CSS file

const BorgesWatchmaker = () => {
  return (
    <div className="borges-container">
      <div className="content-wrapper">
        <div className="text-content">
          <h1 className="main-title">Borges</h1>
          <h2 className="subtitle">O seu relojoeiro!</h2>
          <p className="description">
            Descubra a excelência em consertos de relógio. Com mais de 60 
            anos de experiência atuando em Uberlândia e região.
          </p>
        </div>
        <div className="image-container">
          <img 
            src="/borges-portrait.jpg" 
            alt="Senhor Borges, relojoeiro" 
            className="portrait-image"
          />
        </div>
      </div>
    </div>
  );
};

export default BorgesWatchmaker;