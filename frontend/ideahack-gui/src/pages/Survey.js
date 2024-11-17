import React, { useState, useEffect, useRef } from "react";
import "./Survey.css";
import questionsData from "../data/questions.json";

const Survey = () => {
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const answersRef = useRef(Array(5).fill("")); // Answers stored in a ref
  const selectedTypeRef = useRef(null); // Store selectedType in a ref
  const textInputRef = useRef("");
  const [forceUpdate, setForceUpdate] = useState(false);

  const typeMapping = {
    Inwestorem: "inwestor",
    "Z biznesu": "biznes",
    "Z środowiska uczelnianego": "uczelnia",
  };

  const getFilteredQuestions = () => {
    if (!selectedTypeRef.current) {
      return questionsData.filter((q) => q.typ === "typ");
    }
    return [
      ...questionsData.filter((q) => q.typ === "typ"),
      ...questionsData.filter((q) => q.typ === selectedTypeRef.current),
      ...questionsData.filter((q) => q.typ === "wszystkie"),
    ];
  };
  useEffect(() => {
    console.log(
      "Current question index:",
      currentQuestionIndex,
      filteredQuestions
    );
  }, [currentQuestionIndex]);
  const filteredQuestions = getFilteredQuestions();
  const currentQuestion = filteredQuestions[currentQuestionIndex];
  console.log("asdas", currentQuestionIndex);

  const handleOptionClick = (option) => {
    const updatedAnswers = [...answersRef.current];

    if (currentQuestionIndex === 0) {
      // Handle the first question separately to set selectedType
      const interpretedType = typeMapping[option];
      selectedTypeRef.current = interpretedType;
      updatedAnswers[0] = interpretedType;
    } else if (currentQuestion.jednokrotny) {
      // Single select
      updatedAnswers[currentQuestionIndex] = option;
    } else {
      // Multi-select
      const currentSelections = updatedAnswers[currentQuestionIndex] || [];
      updatedAnswers[currentQuestionIndex] = currentSelections.includes(option)
        ? currentSelections.filter((item) => item !== option)
        : [...currentSelections, option];
    }

    answersRef.current = updatedAnswers;
    console.log("Updated answers:", answersRef.current[currentQuestionIndex]);
    setForceUpdate((prev) => !prev);
  };

  const handleTextInput = (event) => {
    textInputRef.current = event.target.value;
  };

  const handleNext = () => {
    if (currentQuestion.tekst) {
      const updatedAnswers = [...answersRef.current];
      updatedAnswers[currentQuestionIndex] += " " + textInputRef.current;
      answersRef.current = updatedAnswers;
    }
    textInputRef.current = "";
    setCurrentQuestionIndex((prev) => prev + 1);
  };

  const handlePrevious = () => {
    if (currentQuestionIndex > 0) {
      setCurrentQuestionIndex((prev) => prev - 1);
    }
  };

  const handleFinish = () => {
    const surveyResult = {
      type: answersRef.current[0], // Maps to "type"
      industry: answersRef.current[1], // Maps to "industry"
      budget: answersRef.current[2], // Maps to "budget"
      location: answersRef.current[3], // Maps to "location"
      notes: textInputRef.current, // Maps to "notes"
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
          currentQuestion.opcje.map(
            (option, index) => (
              console.log("option", option),
              (
                <button
                  key={index}
                  className={`option-button ${
                    currentQuestion.jednokrotny
                      ? answersRef.current[currentQuestionIndex] === option
                        ? "selected"
                        : ""
                      : answersRef.current[currentQuestionIndex]?.includes(
                          option
                        )
                      ? "selected"
                      : ""
                  }`}
                  onClick={() => handleOptionClick(option)}
                >
                  {option}
                </button>
              )
            )
          )}
      </div>

      {currentQuestion.tekst && (
        <div className="additional-input">
          <label>
            {currentQuestion.tekst}
            <input
              type="text"
              defaultValue={
                answersRef.current[currentQuestionIndex] || ""
              } /* Keep the current value on input */
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
        {currentQuestionIndex === 4 ? (
          <button onClick={handleFinish}>Zakończ</button>
        ) : (
          <button onClick={handleNext}>Dalej</button>
        )}
      </div>
    </div>
  );
};

export default Survey;
