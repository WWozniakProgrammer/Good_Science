import React, { useState, useEffect } from "react";
import "./Survey.css";
import questionsData from "../data/questions.json";

const Survey = () => {
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [answers, setAnswers] = useState([]);
  const [additionalText, setAdditionalText] = useState("");
  const [selectedType, setSelectedType] = useState(null);

  const typeMapping = {
    Inwestorem: "inwestor",
    "Z biznesu": "biznes",
    "Z środowiska uczelnianego": "uczelnia",
  };

  useEffect(() => {
    const initialAnswers = Array(5).fill(null);
    setAnswers(initialAnswers);
  }, []);

  const getFilteredQuestions = () => {
    if (!selectedType) {
      return questionsData.filter((q) => q.typ === "typ");
    }
    return [
      ...questionsData.filter((q) => q.typ === selectedType),
      ...questionsData.filter((q) => q.typ === "wszystkie"),
    ];
  };

  const filteredQuestions = getFilteredQuestions();
  const currentQuestion = filteredQuestions[currentQuestionIndex];

  const handleOptionClick = (option) => {
    const updatedAnswers = [...answers];

    if (currentQuestion.typ === "typ") {
      const interpretedType = typeMapping[option];
      setSelectedType(interpretedType);
      updatedAnswers[currentQuestionIndex] = interpretedType;
    } else if (currentQuestion.jednokrotny) {
      updatedAnswers[currentQuestionIndex] = option;
    } else {
      const currentSelections = updatedAnswers[currentQuestionIndex] || [];
      updatedAnswers[currentQuestionIndex] = currentSelections.includes(option)
        ? currentSelections.filter((item) => item !== option)
        : [...currentSelections, option];
    }

    setAnswers(updatedAnswers);
    console.log("Current answers:", updatedAnswers, answers);
  };

  const handleTextInput = (event) => {
    const text = event.target.value;
    setAdditionalText(text);

    const updatedAnswers = [...answers];
    updatedAnswers[currentQuestionIndex] = text;
    setAnswers(updatedAnswers);
  };

  const handleNext = () => {
    if (currentQuestionIndex < filteredQuestions.length - 1) {
      setCurrentQuestionIndex((prev) => prev + 1);
      setAdditionalText("");
    }
  };

  const handleFinish = () => {
    const surveyResult = {
      type: answers[0],
      industry: answers[1],
      budget: answers[2],
      location: answers[3],
      notes: answers[4],
    };

    console.log("Survey completed with structured JSON:", surveyResult);

    fetch("/api/save-survey", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(surveyResult),
    })
      .then((response) => response.json())
      .then((data) => {
        console.log("Server response:", data);
        alert("Dziękujemy za wypełnienie ankiety!");
      })
      .catch((error) => console.error("Error submitting survey:", error));
  };

  return (
    <div className="survey">
      <h1>{currentQuestion.pytanie}</h1>

      <div className="options">
        {currentQuestion.opcje.length > 0 &&
          currentQuestion.opcje.map((option, index) => (
            <button
              key={index}
              className={`option-button ${
                currentQuestion.jednokrotny
                  ? answers[currentQuestionIndex] === option
                    ? "selected"
                    : ""
                  : answers[currentQuestionIndex]?.includes(option)
                  ? "selected"
                  : ""
              }`}
              onClick={() => handleOptionClick(option)}
            >
              {option}
            </button>
          ))}
      </div>

      {currentQuestion.tekst && (
        <div className="additional-input">
          <label>
            {currentQuestion.tekst}
            <input
              type="text"
              value={additionalText}
              onChange={handleTextInput}
              placeholder="Podaj szczegóły..."
            />
          </label>
        </div>
      )}

      <div className="navigation-buttons">
        {currentQuestionIndex === filteredQuestions.length - 1 ? (
          <button onClick={handleFinish}>Zakończ</button>
        ) : (
          <button onClick={handleNext}>Dalej</button>
        )}
      </div>
    </div>
  );
};

export default Survey;
