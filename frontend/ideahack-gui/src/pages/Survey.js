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
    // Initialize answers array with null for all questions
    const initialAnswers = Array(questionsData.length).fill(null);
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
      console.log("Interpreted type:", interpretedType, answers);
      setSelectedType(interpretedType);
      updatedAnswers[currentQuestionIndex] = interpretedType;
    }

    if (currentQuestion.jednokrotny) {
      // Single select
      updatedAnswers[currentQuestionIndex] = option;
    } else {
      // Multi-select
      const currentSelections = updatedAnswers[currentQuestionIndex] || [];
      updatedAnswers[currentQuestionIndex] = currentSelections.includes(option)
        ? currentSelections.filter((item) => item !== option)
        : [...currentSelections, option];
    }

    setAnswers(updatedAnswers);
    console.log("Current answers:", answers);
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
      setAdditionalText(""); // Reset additional text for the next question
    }
  };

  const handlePrevious = () => {
    if (currentQuestionIndex > 0) {
      setCurrentQuestionIndex((prev) => prev - 1);
      setAdditionalText(""); // Reset additional text for the previous question
    }
  };

  const handleFinish = () => {
    const surveyResult = {
      type: answers[0], // Maps to "type" (first question)
      industry: answers[1], // Maps to "industry"
      budget: answers[2], // Maps to "budget"
      location: answers[3], // Maps to "location"
      notes: answers[4], // Maps to "notes" (last question)
    };

    console.log("Survey completed with structured JSON:", surveyResult);

    // Example: API call to save the result
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
        <button onClick={handlePrevious} disabled={currentQuestionIndex === 0}>
          Wróć
        </button>
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
