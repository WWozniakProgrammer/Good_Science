import React from "react";
import { useNavigate } from "react-router-dom";
import "./HeroSection.css";

const HeroSection = () => {
  const navigate = useNavigate();

  const handleStartSurvey = () => {
    navigate("/survey");
  };

  return (
    <div className="page-container">
      <div className="hero-content">
        <p className="hero-text">
          Jako zespół <span className="hero-text-sspan">MatchAI</span> wierzymy
          w wizję współpracy między różnymi obszarami. Razem możemy więcej!
        </p>
      </div>
      <div className="info-windows">
        <div className="window">
          <h2 className="window-h2">Dla inwestorów 📈</h2>
          <p className="window-p">
            Znajdź startupy i uczelnie szukających Twojego wsparcia
          </p>
        </div>
        <div className="window">
          <h2 className="window-h2">Dla uczelni 👩🏻‍🏫</h2>
          <p className="window-p">
            Połącz się z biznesem i inwestorami tworząc współprace
          </p>
        </div>
        <div className="window">
          <h2 className="window-h2">Dla biznesu 💼</h2>
          <p className="window-p">
            Odkrywaj szanse rozwoju z inwestorami i uczelnianymi partnerami
          </p>
        </div>
      </div>
      <button
        className="hero-button"
        onClick={handleStartSurvey}
        onMouseEnter={(e) => (e.target.style.backgroundColor = "#45c1c5")}
        onMouseLeave={(e) => (e.target.style.backgroundColor = "#56d7dc")}
      >
        🚀 ZACZYNAMY!
      </button>
    </div>
  );
};

export default HeroSection;
