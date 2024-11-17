import React, { useState } from "react";
import "./Survey.css";
import questionsData from "../data/questions.json";

const Survey = () => {
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [answers, setAnswers] = useState({});
  const [additionalText, setAdditionalText] = useState("");
  const [selectedType, setSelectedType] = useState(null);

  const typeMapping = {
    Inwestorem: "inwestor",
    "Z biznesu": "biznes",
    "Z środowiska uczelnianego": "uczelnia",
  };

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

  const updateAnswer = (question, answer) => {
    setAnswers((prev) => ({ ...prev, [question]: answer }));
  };

  const handleOptionClick = (option) => {
    const question = currentQuestion.pytanie;

    if (currentQuestion.typ === "typ") {
      const interpretedType = typeMapping[option];
      setSelectedType(interpretedType);
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

  const handleTextInput = (event) => {
    const text = event.target.value;
    setAdditionalText(text);
    updateAnswer(`${currentQuestion.pytanie}_tekst`, text);
  };

  const handleNext = () => {
    if (currentQuestionIndex < filteredQuestions.length - 1) {
      setCurrentQuestionIndex((prev) => prev + 1);
      setAdditionalText("");
    }
  };

  const handlePrevious = () => {
    if (currentQuestionIndex > 0) {
      setCurrentQuestionIndex((prev) => prev - 1);
      setAdditionalText("");
    }
  };

  const handleFinish = () => {
    console.log("Survey completed with answers:", answers);
    alert("Dziękujemy za wypełnienie ankiety!");
    // Additional logic to save answers (e.g., API call) can be added here
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
        {currentQuestion.opcje.length === 0 ? (
          <button onClick={handleFinish}>Finish Survey</button>
        ) : (
          <button
            onClick={handleNext}
            disabled={currentQuestionIndex === filteredQuestions.length - 1}
          >
            Next
          </button>
        )}
      </div>
    </div>
  );
};

export default Survey;
