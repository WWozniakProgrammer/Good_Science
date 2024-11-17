import React, { useState } from "react";
import "./MeetingForm.css";

const MeetingForm = () => {
    const [formData, setFormData] = useState({
      topic: "",
      description: "",
      date: "",
      startTime: "",
      endTime: "",
    });
  
    const [errorMessage, setErrorMessage] = useState("");
    const [successMessage, setSuccessMessage] = useState("");
  
    const handleChange = (e) => {
      const { name, value } = e.target;
      setFormData({ ...formData, [name]: value });
    };
  
    const handleSubmit = async (e) => {
      e.preventDefault();
  
      try {
        const response = await fetch("https://your-endpoint.com/meeting", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(formData),
        });
  
        const data = await response.json();
  
        if (response.ok) {
          setSuccessMessage("Spotkanie zostało zapisane!");
          setErrorMessage("");
          setFormData({
            topic: "",
            description: "",
            date: "",
            startTime: "",
            endTime: "",
          });
        } else {
          throw new Error(
            data.message || "Błąd podczas zapisywania spotkania. Spróbuj ponownie."
          );
        }
      } catch (error) {
        setErrorMessage(error.message);
        setSuccessMessage("");
      }
    };
  
    return (
        <div className="meeting-container">
          <form className="meeting-form" onSubmit={handleSubmit}>
            <h2>Tworzenie spotkania</h2>
            <div className="form-group">
              <label htmlFor="topic">Nazwa</label>
              <input
                type="text"
                id="topic"
                name="topic"
                value={formData.topic}
                onChange={handleChange}
                placeholder="Wpisz nazwę spotkania"
                required
              />
            </div>
            <div className="form-group">
              <label htmlFor="description">Opis</label>
              <textarea
                id="description"
                name="description"
                value={formData.description}
                onChange={handleChange}
                placeholder="Wpisz opis spotkania"
                required
              />
            </div>
            <div className="form-group">
              <label htmlFor="date">Termin</label>
              <div className="date-time-group">
                <input
                  type="date"
                  id="date"
                  name="date"
                  value={formData.date}
                  onChange={handleChange}
                  placeholder="Wybierz datę"
                  required
                />
                <span className="time-label">od</span>
                <input
                  type="time"
                  id="startTime"
                  name="startTime"
                  value={formData.startTime}
                  onChange={handleChange}
                  placeholder="Godzina początkowa"
                  required
                />
                <span className="time-label">do</span>
                <input
                  type="time"
                  id="endTime"
                  name="endTime"
                  value={formData.endTime}
                  onChange={handleChange}
                  placeholder="Godzina końcowa"
                  required
                />
              </div>
            </div>
            <div className="form-actions">
              <button type="button" className="register-button">Wróć</button>
              <button type="submit">Wyślij</button>
            </div>
            {errorMessage && <p className="error">{errorMessage}</p>}
            {successMessage && <p className="success">{successMessage}</p>}
          </form>
        </div>
    );
};
    export default MeetingForm;
    
