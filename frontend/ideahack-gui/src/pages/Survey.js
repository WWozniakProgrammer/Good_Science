import React, { useState } from "react";
import "./Survey.css";
import questionsData from "../data/questions.json";

const Survey = () => {
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [answers, setAnswers] = useState({}); // Store answers
  const [additionalText, setAdditionalText] = useState(""); // For text input
  const [selectedType, setSelectedType] = useState(null); // To store the selected type

  // Dynamically filter questions based on the selected type
  const getFilteredQuestions = () => {
    if (!selectedType) {
      // Show only the first question to select the type
      return questionsData.filter((q) => q.typ === "typ");
    }
    // After type is selected, filter type-specific and "wszystkie" questions
    return [
      ...questionsData.filter((q) => q.typ === selectedType),
      ...questionsData.filter((q) => q.typ === "wszystkie"),
    ];
  };

  const filteredQuestions = getFilteredQuestions();
  const currentQuestion = filteredQuestions[currentQuestionIndex];

  // Update answer for the current question
  const updateAnswer = (question, answer) => {
    setAnswers((prev) => ({ ...prev, [question]: answer }));
  };

  // Handle option selection (single/multiple)
  const handleOptionClick = (option) => {
    const question = currentQuestion.pytanie;

    if (currentQuestion.typ === "typ") {
      // For the first question, set the selected type
      setSelectedType(option);
    }

    if (currentQuestion.jednokrotny) {
      updateAnswer(question, option);
    } else {
      const currentAnswers = answers[question] || [];
      const updatedAnswers = currentAnswers.includes(option)
        ? currentAnswers.filter((item) => item !== option)
        : [...currentAnswers, option];
      updateAnswer(question, updatedAnswers);
    }
  };

  // Handle text input
  const handleTextInput = (event) => {
    const text = event.target.value;
    setAdditionalText(text);
    updateAnswer(`${currentQuestion.pytanie}_tekst`, text);
  };

  // Navigation
  const handleNext = () => {
    if (currentQuestionIndex < filteredQuestions.length - 1) {
      setCurrentQuestionIndex((prev) => prev + 1);
      setAdditionalText(""); // Reset text input for the next question
    }
  };

  const handlePrevious = () => {
    if (currentQuestionIndex > 0) {
      setCurrentQuestionIndex((prev) => prev - 1);
    }
  };

  return (
    <div className="survey">
      <h1>{currentQuestion.pytanie}</h1>

      <div className="options">
        {currentQuestion.opcje.map((option, index) => (
          <button
            key={index}
            className={`option-button ${
              currentQuestion.jednokrotny
                ? answers[currentQuestion.pytanie] === option
                  ? "selected"
                  : ""
                : answers[currentQuestion.pytanie]?.includes(option)
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
          Previous
        </button>
        <button
          onClick={handleNext}
          disabled={currentQuestionIndex === filteredQuestions.length - 1}
        >
          Next
        </button>
      </div>

      <pre className="debug">{JSON.stringify(answers, null, 2)}</pre>
    </div>
  );
};

export default Survey;
