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
      
      {/* Nova Seção - Ajuda para Relógios Parados */}
      <div className="help-section">
        <div className="help-container">
          <h2 className="help-title">Seu Relógio Parou? Nós Podemos Ajudar!</h2>
          
          <div className="help-features">
            {/* Feature 1 */}
            <div className="feature-card">
              <div className="feature-icon">
                <svg viewBox="0 0 24 24" fill="currentColor" width="48" height="48">
                  <path d="M9.5,3A6.5,6.5 0 0,1 16,9.5C16,11.11 15.41,12.59 14.44,13.73L14.71,14H15.5L20.5,19L19,20.5L14,15.5V14.71L13.73,14.44C12.59,15.41 11.11,16 9.5,16A6.5,6.5 0 0,1 3,9.5A6.5,6.5 0 0,1 9.5,3M9.5,5C7,5 5,7 5,9.5C5,12 7,14 9.5,14C12,14 14,12 14,9.5C14,7 12,5 9.5,5Z" />
                </svg>
              </div>
              <h3>Diagnóstico Preciso</h3>
              <p>Identificamos o problema com precisão.</p>
            </div>
            
            {/* Feature 2 */}
            <div className="feature-card">
              <div className="feature-icon">
                <svg viewBox="0 0 24 24" width="48" height="48">
                  <path d="M8,4 L16,4 L16,7 L8,7 Z M8,17 L16,17 L16,20 L8,20 Z M6,7 C4,8 3,10 3,12 C3,14 4,16 6,17 M6,7 L6,17 M6,7 L8,7 L8,17 L6,17 M13,9 C11.34,9 10,10.34 10,12 C10,13.66 11.34,15 13,15 C14.66,15 16,13.66 16,12 C16,10.34 14.66,9 13,9 Z M17,7 L21,3 M19,12 L23,12 M17,17 L21,21 M15,9 L17,7 M15,15 L17,17" 
                    fill="none" 
                    stroke="currentColor" 
                    strokeWidth="1.2" 
                    strokeLinecap="round" 
                    strokeLinejoin="round" />
                  <circle cx="13" cy="12" r="0.5" fill="currentColor" />
                  <circle cx="19" cy="9" r="1.8" fill="none" stroke="currentColor" strokeWidth="1.2" />
                  <circle cx="19" cy="9" r="0.5" fill="currentColor" />
                </svg>
              </div>
              <h3>Equipamentos Modernos</h3>
              <p>Reparos eficientes com tecnologia de ponta.</p>
            </div>
          </div>
        </div>
      </div>
      
      {/* Seção de Restauração de Relógios Antigos */}
      <div className="restoration-section">
        <div className="restoration-container">
          <h2 className="restoration-title">Restauração de Relógios Antigos: Reviva a História</h2>
          
          <div className="restoration-grid">
            {/* Restoration Feature 1 */}
            <div className="restoration-card">
              <div className="restoration-image">
                <img 
                  src="/vintage-pocket-watch.jpg" 
                  alt="Relógio de bolso antigo" 
                />
              </div>
              <h3>Relíquias de Família</h3>
              <p>
                Deixe seu relógio de herança funcionando como novo.
              </p>
            </div>
            
            {/* Restoration Feature 2 */}
            <div className="restoration-card">
              <div className="restoration-image">
                <img 
                  src="/watchmaker-working.jpg" 
                  alt="Técnico trabalhando em relógio" 
                />
              </div>
              <h3>Técnico Especializado</h3>
              <p>
                Profissional com mais de 60 anos de experiência cuidando do seu relógio.
              </p>
            </div>
            
            {/* Restoration Feature 3 */}
            <div className="restoration-card">
              <div className="restoration-image">
                <img 
                  src="/restored-clock.jpg" 
                  alt="Relógio restaurado" 
                />
              </div>
              <h3>Resultados Impressionantes</h3>
              <p>
                Seu relógio restaurado com perfeição e cuidado.
              </p>
            </div>
          </div>
        </div>
      </div>
      
      {/* Seção de Contato */}
      <div className="contact-section">
        <div className="contact-container">
          <div className="contact-content">
            <div className="contact-image">
              <img 
                src="/uberlandia-city.jpg" 
                alt="Cidade de Uberlândia" 
              />
            </div>
            <div className="contact-info">
              <h2>Uberlândia - MG</h2>
              
              <div className="contact-details">
                <div className="contact-item">
                  <h3>Telefone:</h3>
                  <p>(34) 99666-8299</p>
                </div>
                
                <div className="contact-item">
                  <h3>Endereço:</h3>
                  <p>Rua Sebastiana Arantes Fonseca, 463 - Santa Mônica, Uberlândia - MG, 38408-232</p>
                </div>
                
                <div className="contact-item">
                  <h3>E-mail:</h3>
                  <p>aladimborges@gmail.com</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default BorgesWatchmaker;