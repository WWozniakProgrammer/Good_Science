import React, { useEffect, useState } from "react";
import "./Matching.css"; // Include your CSS for styling

const Matching = () => {
  const [companies, setCompanies] = useState([]);

  useEffect(() => {
    // Fetch company data from the API
    fetch("/api/companies") // Replace with your actual API endpoint
      .then((response) => response.json())
      .then((data) => setCompanies(data))
      .catch((error) => console.error("Error fetching data:", error));
  }, []);

  return (
    <div className="matching-container">
      {companies.map((company, index) => (
        <div key={index} className="company-card">
          <h2>{company.name}</h2>
          <p>
            <strong>Typ:</strong> {company.typ}
          </p>
          <p>
            <strong>Branża:</strong> {company.brażna}
          </p>
          <p>
            <strong>Lokalizacja:</strong> {company.lokalizacja}
          </p>
          <p>
            <strong>Number of Stars:</strong> {company.stars}
          </p>
          <button onClick={() => alert(`Umów spotkanie with ${company.name}`)}>
            Umów spotkanie
          </button>
        </div>
      ))}
    </div>
  );
};

export default Matching;
