import React from "react";
import HeroSection from "../components/HeroSection";
import "./HomePage.css";

const HomePage = () => {
  return (
    <div className="homepage">
      <div className="hero-container">
        <HeroSection />
      </div>
    </div>
  );
};

export default HomePage;
