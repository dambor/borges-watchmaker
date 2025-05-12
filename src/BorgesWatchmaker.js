import React from 'react';
import './BorgesWatchmaker.css';

const BorgesWatchmaker = () => {
  return (
    <div>
      {/* Hero Section */}
      <div className="hero-section">
        <div className="hero-container">
          <div className="hero-content">
            <div className="text-content">
              <h1>Borges</h1>
              <h2>O seu relojoeiro!</h2>
              <p>
                Descubra a excelência em consertos de relógio. Com mais de 60 
                anos de experiência atuando em Uberlândia e região.
              </p>
            </div>
            <div className="image-content">
              <img 
                src="/borges-portrait.jpg" 
                alt="Senhor Borges, relojoeiro" 
              />
            </div>
          </div>
        </div>
      </div>
      
      {/* Services Section */}
      <div className="services-section">
        <div className="services-container">
          <h2>Nossos Serviços de Manutenção e Reparo</h2>
          
          <div className="services-grid">
            {/* Service 1 */}
            <div className="service-card">
              <div className="service-image">
                <img 
                  src="/service-1.gif" 
                  alt="Manutenção de relógio" 
                />
              </div>
              <h3>Manutenção Completa</h3>
              <p>
                Recuperamos a funcionalidade e estética do seu relógio.
              </p>
            </div>
            
            {/* Service 2 */}
            <div className="service-card">
              <div className="service-image">
                <img 
                  src="/service-2.jpg" 
                  alt="Serviço express de relógio" 
                />
              </div>
              <h3>Serviço Express</h3>
              <p>
                Troca de bateria e ajustes rápidos na hora.
              </p>
            </div>
            
            {/* Service 3 */}
            <div className="service-card">
              <div className="service-image">
                <img 
                  src="/service-3.jpg" 
                  alt="Acessórios para relógios" 
                />
              </div>
              <h3>Acessórios</h3>
              <p>
                Pulseira, elos e outros acessórios para variadas marcas.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default BorgesWatchmaker;