import React, { useState, useEffect } from 'react';
import './EnhancedMathApp.css';
import GameifiedLearning from './GameifiedLearning';

const EnhancedMathApp = () => {
  const [question, setQuestion] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [examples, setExamples] = useState([]);
  const [problemTypes, setProblemTypes] = useState([]);
  const [selectedExample, setSelectedExample] = useState('');
  const [showGamifiedLearning, setShowGamifiedLearning] = useState(false);

  // Load examples and problem types on component mount
  useEffect(() => {
    fetchExamples();
    fetchProblemTypes();
  }, []);

  const fetchExamples = async () => {
    try {
      const response = await fetch('http://localhost:5001/api/examples');
      const data = await response.json();
      setExamples(data.examples || []);
    } catch (error) {
      console.error('Failed to fetch examples:', error);
    }
  };

  const fetchProblemTypes = async () => {
    try {
      const response = await fetch('http://localhost:5001/api/problem-types');
      const data = await response.json();
      setProblemTypes(data.supported_types || []);
    } catch (error) {
      console.error('Failed to fetch problem types:', error);
    }
  };

  const solveProblem = async () => {
    if (!question.trim()) {
      alert('Please enter a mathematical question');
      return;
    }

    setLoading(true);
    setResult(null);

    try {
      const response = await fetch('http://localhost:5001/api/solve', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ question: question.trim() }),
      });

      const data = await response.json();
      setResult(data);
    } catch (error) {
      setResult({
        success: false,
        error: 'Failed to connect to the mathematical AI server. Please ensure the server is running on port 5001.',
      });
    } finally {
      setLoading(false);
    }
  };

  const handleExampleSelect = (exampleQuestion) => {
    setQuestion(exampleQuestion);
    setSelectedExample(exampleQuestion);
  };

  const clearAll = () => {
    setQuestion('');
    setResult(null);
    setSelectedExample('');
  };

  const handleGameComplete = (gameResult) => {
    console.log('Game completed:', gameResult);
    setShowGamifiedLearning(false);
    
    // Show completion message
    if (gameResult.correct) {
      alert(`🎉 Great job! You earned ${gameResult.xpGained} XP!`);
    } else {
      alert(`Keep trying! You earned ${gameResult.xpGained} XP for the attempt.`);
    }
  };

  const handleGameExit = () => {
    setShowGamifiedLearning(false);
  };

  const openGamifiedLearning = () => {
    setShowGamifiedLearning(true);
  };

  if (showGamifiedLearning) {
    return (
      <GameifiedLearning
        problem={result}
        onComplete={handleGameComplete}
        onExit={handleGameExit}
      />
    );
  }

  return (
    <div className="enhanced-math-app">
      {/* Header */}
      <header className="app-header">
        <div className="header-content">
          <h1 className="app-title">
            <span className="math-icon">🧮</span>
            AI for Engineers
            <span className="subtitle">Enhanced Mathematical Reasoning</span>
          </h1>
          <p className="app-description">
            Superior to ChatGPT for step-by-step mathematical explanations
          </p>
        </div>
      </header>

      {/* Main Content */}
      <main className="main-content">
        <div className="container">
          
          {/* Problem Types Section */}
          <section className="problem-types-section">
            <h2>🎯 Supported Problem Types</h2>
            <div className="problem-types-grid">
              {problemTypes.map((type, index) => (
                <div key={index} className="problem-type-card">
                  {type}
                </div>
              ))}
            </div>
          </section>

          {/* Examples Section */}
          <section className="examples-section">
            <h2>📚 Try These Examples</h2>
            <div className="examples-grid">
              {examples.map((example, index) => (
                <div 
                  key={index} 
                  className={`example-card ${selectedExample === example.question ? 'selected' : ''}`}
                  onClick={() => handleExampleSelect(example.question)}
                >
                  <div className="example-type">{example.type}</div>
                  <div className="example-question">{example.question}</div>
                  <div className="example-difficulty">
                    <span className={`difficulty ${example.difficulty.toLowerCase()}`}>
                      {example.difficulty}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </section>

          {/* Input Section */}
          <section className="input-section">
            <div className="input-card">
              <h2>🤔 Ask Your Mathematical Question</h2>
              <div className="input-area">
                <textarea
                  value={question}
                  onChange={(e) => setQuestion(e.target.value)}
                  onKeyDown={handleKeyPress}
                  placeholder="Enter your mathematical question here... (e.g., 'Find the integral of x² + 3x - 2 dx')"
                  className="question-input"
                  rows={4}
                />
                <div className="input-actions">
                  <button 
                    onClick={clearAll}
                    className="clear-btn"
                    disabled={loading}
                  >
                    Clear
                  </button>
                  <button 
                    onClick={solveProblem}
                    className="solve-btn"
                    disabled={loading || !question.trim()}
                  >
                    {loading ? (
                      <>
                        <span className="spinner"></span>
                        Solving...
                      </>
                    ) : (
                      <>
                        <span className="solve-icon">🚀</span>
                        Solve Step-by-Step
                      </>
                    )}
                  </button>
                </div>
                <div className="input-hint">
                  💡 Tip: Press Ctrl+Enter to solve quickly
                </div>
              </div>
            </div>
          </section>

          {/* Results Section */}
          {result && (
            <section className="results-section">
              <div className="result-card">
                {result.success ? (
                  <div className="success-result">
                    <div className="result-header">
                      <h2>✅ Solution</h2>
                      {result.problem_type && (
                        <span className="problem-type-badge">
                          {result.problem_type}
                        </span>
                      )}
                      {result.confidence && (
                        <span className={`confidence-badge ${result.confidence}`}>
                          {result.confidence} confidence
                        </span>
                      )}
                    </div>

                    <div className="question-display">
                      <strong>Question:</strong> {result.question}
                    </div>

                    {result.solution && (
                      <div className="solution-section">
                        <h3>📝 Detailed Explanation</h3>
                        <div className="solution-text">
                          {result.solution}
                        </div>
                      </div>
                    )}

                    {result.steps && result.steps.length > 0 && (
                      <div className="steps-section">
                        <h3>🔢 Step-by-Step Breakdown</h3>
                        <ol className="steps-list">
                          {result.steps.map((step, index) => (
                            <li key={index} className="step-item">
                              {step}
                            </li>
                          ))}
                        </ol>
                      </div>
                    )}

                    {result.mathematical_concepts && result.mathematical_concepts.length > 0 && (
                      <div className="concepts-section">
                        <h3>🧠 Mathematical Concepts</h3>
                        <div className="concepts-list">
                          {result.mathematical_concepts.map((concept, index) => (
                            <span key={index} className="concept-tag">
                              {concept}
                            </span>
                          ))}
                        </div>
                      </div>
                    )}

                    {result.mathematical_tips && result.mathematical_tips.length > 0 && (
                      <div className="tips-section">
                        <h3>💡 Mathematical Tips</h3>
                        <ul className="tips-list">
                          {result.mathematical_tips.map((tip, index) => (
                            <li key={index} className="tip-item">
                              {tip}
                            </li>
                          ))}
                        </ul>
                      </div>
                    )}

                    {result.verification && (
                      <div className="verification-section">
                        <h3>✓ Verification</h3>
                        <div className="verification-text">
                          {result.verification}
                        </div>
                      </div>
                    )}

                    <div className="result-footer">
                      <div className="model-info">
                        <span className="model-badge">
                          {result.model_type || 'Enhanced Mathematical AI'}
                        </span>
                        <span className="api-version">
                          API v{result.api_version || '2.0'}
                        </span>
                      </div>
                      <div className="learning-actions">
                        <button 
                          className="gamified-learning-btn"
                          onClick={openGamifiedLearning}
                        >
                          🎮 Need Help? Play Learning Games!
                        </button>
                      </div>
                    </div>
                  </div>
                ) : (
                  <div className="error-result">
                    <h2>❌ Error</h2>
                    <div className="error-message">
                      {result.error}
                    </div>
                    <div className="error-suggestions">
                      <h3>💡 Suggestions:</h3>
                      <ul>
                        <li>Make sure your question is clearly stated</li>
                        <li>Try one of the example problems above</li>
                        <li>Check that the AI server is running</li>
                        <li>Ensure your question is mathematical in nature</li>
                      </ul>
                    </div>
                  </div>
                )}
              </div>
            </section>
          )}

          {/* Features Section */}
          <section className="features-section">
            <h2>🌟 Why Choose Our Mathematical AI?</h2>
            <div className="features-grid">
              <div className="feature-card">
                <div className="feature-icon">🎯</div>
                <h3>Step-by-Step Solutions</h3>
                <p>Unlike ChatGPT, we provide detailed mathematical reasoning with clear step-by-step explanations</p>
              </div>
              <div className="feature-card">
                <div className="feature-icon">🧠</div>
                <h3>Educational Focus</h3>
                <p>Designed specifically for learning, not just getting answers</p>
              </div>
              <div className="feature-card">
                <div className="feature-icon">✅</div>
                <h3>Solution Verification</h3>
                <p>Includes verification steps to help you understand and check your work</p>
              </div>
              <div className="feature-card">
                <div className="feature-icon">📚</div>
                <h3>Concept Identification</h3>
                <p>Identifies and explains the mathematical concepts used in each solution</p>
              </div>
            </div>
          </section>
        </div>
      </main>

      {/* Footer */}
      <footer className="app-footer">
        <div className="footer-content">
          <p>© 2024 AI for Engineers - Building Better Engineers Through Conceptual Understanding</p>
          <div className="team-info">
            <p>Developed by: Sai Spoorthy Eturu, Sahithi Rithvika Katakam, Shivani Edigi, Hari Hansika Kommera</p>
            <p>Under the guidance of: A Naga Kalyani, BVRIT Hyderabad</p>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default EnhancedMathApp;