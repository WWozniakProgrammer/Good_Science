import React from "react";
import HeroSection from "../components/HeroSection";
import InfoWindows from "../components/InfoWindows";
import "./HomePage.css";

const HomePage = () => {
  return (
    <div className="homepage">
      <div className="hero-container">
        <HeroSection />
      </div>
      <div className="info-container">{/* <InfoWindows /> */}</div>
    </div>
  );
};

export default HomePage;
