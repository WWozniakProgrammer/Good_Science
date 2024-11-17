import React from "react";
import { useNavigate } from "react-router-dom";
import "./HeroSection.css";

const HeroSection = () => {
  const navigate = useNavigate();

  const handleStartSurvey = () => {
    navigate("/survey");
  };

  return (
    <div class="pageContainer">
      {/* Hero Section */}
      <div class="hero">
        <div style={styles.heroContent}>
          <p style={styles.heroText}>
            Jako zespół <span style={styles.heroTextSpan}>MatchAI</span>{" "}
            wierzymy w wizję współpracy między różnymi obszarami. Razem możemy
            więcej.
          </p>
          <button
            style={styles.heroButton}
            onClick={handleStartSurvey}
            onMouseEnter={(e) => (e.target.style.backgroundColor = "#45c1c5")}
            onMouseLeave={(e) => (e.target.style.backgroundColor = "#56d7dc")}
          >
            🚀 ZACZYNAMY!
          </button>
        </div>
      </div>

      {/* Info Windows Section */}
      <div style="infoWindows">
        <div style="window">
          <h2 style="windowHeader">Dla inwestorów</h2>
          <p style="windowText">
            Znajdź startupy i uczelnie szukających Twojego wsparcia
          </p>
        </div>
        <div style="window">
          <h2 style="windowHeader">Dla uczelni</h2>
          <p style="windowText">
            Połącz się z biznesem i inwestorami tworząc współprace
          </p>
        </div>
        <div style="window">
          <h2 style="windowHeader">Dla biznesu</h2>
          <p style="windowText">
            Odkrywaj szanse rozwoju z inwestorami i uczelnianymi partnerami
          </p>
        </div>
      </div>
    </div>
  );
};

export default HeroSection;
