import React from "react";
import "./Matching.css";

const Matching = () => {
  const proposals = [
    { name: "Firma X", type: "Biznes", industry: "IT", location: "Warszawa", rating: 4 },
    { name: "Uczelnia Y", type: "Edukacja", industry: "Technologia", location: "Kraków", rating: 5 },
    { name: "Inwestor Z", type: "Inwestor", industry: "Finanse", location: "Gdańsk", rating: 3 },
  ];

  const handleMeetingClick = () => {
    window.location.href = "http://localhost:3000/meeting";
  };

  return (
    <div className="proposals-container">
      <h1>Proponowane współprace</h1>
      {proposals.map((proposal, index) => (
        <div className="proposal-card" key={index}>
          <div className="left-content">
            <h3>{proposal.name}</h3>
            <p>[typ: {proposal.type}]</p>
            <p>[branża/obszary: {proposal.industry}]</p>
            <p>[lokalizacja: {proposal.location}]</p>
          </div>
          <div className="right-content">
            <div className="rating">
              {Array(5)
                .fill(0)
                .map((_, i) => (
                  <span
                    key={i}
                    className={`rating-star ${i < proposal.rating ? "full" : "empty"}`}
                  >
                    ★
                  </span>
                ))}
            </div>
            <button onClick={handleMeetingClick}>Umów spotkanie</button>
          </div>
        </div>
      ))}
    </div>
  );
};

export default Matching;
