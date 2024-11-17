import React from "react";
import "./InfoWindows.css";

const InfoWindows = () => {
  return (
    <div class="page-container">
      <div className="info-windows">
        <div className="window">
          <h2>Dla inwestorów</h2>
          <p>Znajdź startupy i uczelnie szukających Twojego wsparcia</p>
        </div>
        <div className="window">
          <h2>Dla uczelni</h2>
          <p>Połącz się z biznesem i inwestorami tworząc współprace</p>
        </div>
        <div className="window">
          <h2>Dla biznesu</h2>
          <p>Odkrywaj szanse rozwoju z inwestorami i uczelnianymi partnerami</p>
        </div>
      </div>
    </div>
  );
};

export default InfoWindows;
