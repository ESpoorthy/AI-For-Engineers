import React, { useState, useEffect } from 'react';
import './GameifiedLearning.css';

const GameifiedLearning = ({ problem, onComplete, onExit }) => {
  const [currentGame, setCurrentGame] = useState(null);
  const [userProgress, setUserProgress] = useState({
    level: 1,
    xp: 0,
    badges: [],
    streak: 0,
    totalProblems: 0,
    correctAnswers: 0
  });
  const [gameState, setGameState] = useState({
    score: 0,
    lives: 3,
    currentQuestion: 0,
    isComplete: false
  });

  const games = {
    'step_builder': {
      name: 'Step Builder',
      description: 'Arrange the solution steps in correct order',
      icon: '🧩',
      difficulty: 'beginner'
    },
    'concept_match': {
      name: 'Concept Matcher',
      description: 'Match mathematical concepts with their definitions',
      icon: '🎯',
      difficulty: 'intermediate'
    },
    'formula_quest': {
      name: 'Formula Quest',
      description: 'Complete the mathematical formulas',
      icon: '⚡',
      difficulty: 'intermediate'
    },
    'visual_solver': {
      name: 'Visual Solver',
      description: 'Solve problems using interactive visualizations',
      icon: '📊',
      difficulty: 'advanced'
    },
    'math_puzzle': {
      name: 'Math Puzzle',
      description: 'Solve mathematical puzzles and brain teasers',
      icon: '🧠',
      difficulty: 'advanced'
    }
  };

  useEffect(() => {
    // Load user progress from localStorage
    const savedProgress = localStorage.getItem('mathLearningProgress');
    if (savedProgress) {
      setUserProgress(JSON.parse(savedProgress));
    }
  }, []);

  const saveProgress = (newProgress) => {
    setUserProgress(newProgress);
    localStorage.setItem('mathLearningProgress', JSON.stringify(newProgress));
  };

  const calculateXP = (difficulty, correct) => {
    const baseXP = { beginner: 10, intermediate: 20, advanced: 30 };
    const multiplier = correct ? 1 : 0.3;
    return Math.floor(baseXP[difficulty] * multiplier);
  };

  const checkLevelUp = (currentXP, newXP) => {
    const currentLevel = Math.floor(currentXP / 100) + 1;
    const newLevel = Math.floor(newXP / 100) + 1;
    return newLevel > currentLevel;
  };

  const awardBadge = (badgeType, progress) => {
    const badges = {
      'first_solve': { name: 'First Solver', icon: '🌟', condition: p => p.correctAnswers >= 1 },
      'streak_master': { name: 'Streak Master', icon: '🔥', condition: p => p.streak >= 5 },
      'problem_crusher': { name: 'Problem Crusher', icon: '💪', condition: p => p.totalProblems >= 10 },
      'accuracy_ace': { name: 'Accuracy Ace', icon: '🎯', condition: p => p.correctAnswers / p.totalProblems >= 0.8 && p.totalProblems >= 5 },
      'level_up': { name: 'Level Up!', icon: '⬆️', condition: p => p.level >= 3 },
      'math_wizard': { name: 'Math Wizard', icon: '🧙‍♂️', condition: p => p.level >= 5 && p.correctAnswers >= 20 }
    };

    const newBadges = [];
    Object.entries(badges).forEach(([key, badge]) => {
      if (!progress.badges.includes(key) && badge.condition(progress)) {
        newBadges.push(key);
      }
    });

    return newBadges;
  };

  const completeGame = (correct, gameType) => {
    const difficulty = games[gameType]?.difficulty || 'intermediate';
    const xpGained = calculateXP(difficulty, correct);
    
    const newProgress = {
      ...userProgress,
      xp: userProgress.xp + xpGained,
      totalProblems: userProgress.totalProblems + 1,
      correctAnswers: userProgress.correctAnswers + (correct ? 1 : 0),
      streak: correct ? userProgress.streak + 1 : 0
    };

    // Check for level up
    const leveledUp = checkLevelUp(userProgress.xp, newProgress.xp);
    if (leveledUp) {
      newProgress.level = Math.floor(newProgress.xp / 100) + 1;
    }

    // Award badges
    const newBadges = awardBadge('', newProgress);
    newProgress.badges = [...userProgress.badges, ...newBadges];

    saveProgress(newProgress);

    // Show completion animation
    setGameState({ ...gameState, isComplete: true });

    return { xpGained, leveledUp, newBadges };
  };

  const StepBuilderGame = () => {
    const [steps, setSteps] = useState([]);
    const [shuffledSteps, setShuffledSteps] = useState([]);
    const [userOrder, setUserOrder] = useState([]);
    const [draggedItem, setDraggedItem] = useState(null);

    useEffect(() => {
      if (problem?.steps) {
        const problemSteps = problem.steps.map((step, index) => ({
          id: index,
          text: step,
          correct: index
        }));
        setSteps(problemSteps);
        
        // Shuffle steps
        const shuffled = [...problemSteps].sort(() => Math.random() - 0.5);
        setShuffledSteps(shuffled);
      }
    }, [problem]);

    const handleDragStart = (e, step) => {
      setDraggedItem(step);
      e.dataTransfer.effectAllowed = 'move';
    };

    const handleDragOver = (e) => {
      e.preventDefault();
      e.dataTransfer.dropEffect = 'move';
    };

    const handleDrop = (e, targetIndex) => {
      e.preventDefault();
      if (draggedItem) {
        const newOrder = [...userOrder];
        newOrder[targetIndex] = draggedItem;
        setUserOrder(newOrder);
        
        // Remove from shuffled steps
        setShuffledSteps(shuffledSteps.filter(step => step.id !== draggedItem.id));
        setDraggedItem(null);
      }
    };

    const checkAnswer = () => {
      const isCorrect = userOrder.every((step, index) => step?.correct === index);
      const result = completeGame(isCorrect, 'step_builder');
      
      setTimeout(() => {
        onComplete({
          correct: isCorrect,
          gameType: 'step_builder',
          ...result
        });
      }, 2000);
    };

    return (
      <div className="step-builder-game">
        <div className="game-header">
          <h3>🧩 Step Builder</h3>
          <p>Drag the steps to arrange them in the correct order</p>
        </div>

        <div className="game-content">
          <div className="shuffled-steps">
            <h4>Available Steps:</h4>
            <div className="steps-container">
              {shuffledSteps.map((step) => (
                <div
                  key={step.id}
                  className="step-card draggable"
                  draggable
                  onDragStart={(e) => handleDragStart(e, step)}
                >
                  {step.text}
                </div>
              ))}
            </div>
          </div>

          <div className="solution-area">
            <h4>Solution Order:</h4>
            <div className="drop-zones">
              {Array.from({ length: steps.length }, (_, index) => (
                <div
                  key={index}
                  className={`drop-zone ${userOrder[index] ? 'filled' : 'empty'}`}
                  onDragOver={handleDragOver}
                  onDrop={(e) => handleDrop(e, index)}
                >
                  <div className="step-number">{index + 1}</div>
                  {userOrder[index] ? (
                    <div className="dropped-step">
                      {userOrder[index].text}
                    </div>
                  ) : (
                    <div className="placeholder">Drop step here</div>
                  )}
                </div>
              ))}
            </div>
          </div>
        </div>

        <div className="game-actions">
          <button 
            className="check-answer-btn"
            onClick={checkAnswer}
            disabled={userOrder.filter(Boolean).length !== steps.length}
          >
            Check Answer
          </button>
        </div>
      </div>
    );
  };

  const ConceptMatchGame = () => {
    const [concepts, setConcepts] = useState([]);
    const [definitions, setDefinitions] = useState([]);
    const [matches, setMatches] = useState({});
    const [selectedConcept, setSelectedConcept] = useState(null);

    useEffect(() => {
      // Generate concept-definition pairs based on problem
      const conceptPairs = [
        { concept: 'Derivative', definition: 'Rate of change of a function' },
        { concept: 'Integral', definition: 'Area under a curve or antiderivative' },
        { concept: 'Limit', definition: 'Value a function approaches as input approaches a point' },
        { concept: 'Matrix', definition: 'Rectangular array of numbers arranged in rows and columns' },
        { concept: 'Vector', definition: 'Quantity with both magnitude and direction' },
        { concept: 'Gradient', definition: 'Vector of partial derivatives' }
      ];

      const shuffledConcepts = [...conceptPairs].sort(() => Math.random() - 0.5);
      const shuffledDefinitions = [...conceptPairs].sort(() => Math.random() - 0.5);
      
      setConcepts(shuffledConcepts.slice(0, 4));
      setDefinitions(shuffledDefinitions.slice(0, 4));
    }, []);

    const handleConceptClick = (concept) => {
      setSelectedConcept(concept);
    };

    const handleDefinitionClick = (definition) => {
      if (selectedConcept) {
        const newMatches = { ...matches };
        newMatches[selectedConcept.concept] = definition.definition;
        setMatches(newMatches);
        setSelectedConcept(null);
      }
    };

    const checkMatches = () => {
      const correctMatches = concepts.filter(concept => 
        matches[concept.concept] === concept.definition
      ).length;
      
      const isCorrect = correctMatches === concepts.length;
      const result = completeGame(isCorrect, 'concept_match');
      
      setTimeout(() => {
        onComplete({
          correct: isCorrect,
          gameType: 'concept_match',
          score: correctMatches,
          total: concepts.length,
          ...result
        });
      }, 2000);
    };

    return (
      <div className="concept-match-game">
        <div className="game-header">
          <h3>🎯 Concept Matcher</h3>
          <p>Match each concept with its correct definition</p>
        </div>

        <div className="game-content">
          <div className="concepts-column">
            <h4>Concepts:</h4>
            {concepts.map((concept, index) => (
              <div
                key={index}
                className={`concept-card ${selectedConcept?.concept === concept.concept ? 'selected' : ''} ${matches[concept.concept] ? 'matched' : ''}`}
                onClick={() => handleConceptClick(concept)}
              >
                {concept.concept}
              </div>
            ))}
          </div>

          <div className="definitions-column">
            <h4>Definitions:</h4>
            {definitions.map((definition, index) => (
              <div
                key={index}
                className={`definition-card ${Object.values(matches).includes(definition.definition) ? 'matched' : ''}`}
                onClick={() => handleDefinitionClick(definition)}
              >
                {definition.definition}
              </div>
            ))}
          </div>
        </div>

        <div className="matches-display">
          <h4>Your Matches:</h4>
          {Object.entries(matches).map(([concept, definition]) => (
            <div key={concept} className="match-pair">
              <span className="concept">{concept}</span>
              <span className="arrow">→</span>
              <span className="definition">{definition}</span>
            </div>
          ))}
        </div>

        <div className="game-actions">
          <button 
            className="check-matches-btn"
            onClick={checkMatches}
            disabled={Object.keys(matches).length !== concepts.length}
          >
            Check Matches
          </button>
        </div>
      </div>
    );
  };

  const ProgressDisplay = () => (
    <div className="progress-display">
      <div className="level-info">
        <div className="level-badge">Level {userProgress.level}</div>
        <div className="xp-bar">
          <div 
            className="xp-fill" 
            style={{ width: `${(userProgress.xp % 100)}%` }}
          ></div>
          <span className="xp-text">{userProgress.xp % 100}/100 XP</span>
        </div>
      </div>

      <div className="stats">
        <div className="stat">
          <span className="stat-icon">🎯</span>
          <span className="stat-value">{userProgress.correctAnswers}/{userProgress.totalProblems}</span>
          <span className="stat-label">Accuracy</span>
        </div>
        <div className="stat">
          <span className="stat-icon">🔥</span>
          <span className="stat-value">{userProgress.streak}</span>
          <span className="stat-label">Streak</span>
        </div>
      </div>

      <div className="badges">
        <h4>🏆 Badges Earned:</h4>
        <div className="badge-grid">
          {userProgress.badges.map((badgeKey, index) => {
            const badgeInfo = {
              'first_solve': { name: 'First Solver', icon: '🌟' },
              'streak_master': { name: 'Streak Master', icon: '🔥' },
              'problem_crusher': { name: 'Problem Crusher', icon: '💪' },
              'accuracy_ace': { name: 'Accuracy Ace', icon: '🎯' },
              'level_up': { name: 'Level Up!', icon: '⬆️' },
              'math_wizard': { name: 'Math Wizard', icon: '🧙‍♂️' }
            }[badgeKey] || { name: 'Unknown', icon: '❓' };

            return (
              <div key={index} className="badge">
                <span className="badge-icon">{badgeInfo.icon}</span>
                <span className="badge-name">{badgeInfo.name}</span>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );

  const GameSelector = () => (
    <div className="game-selector">
      <div className="selector-header">
        <h2>🎮 Choose Your Learning Game</h2>
        <p>Select a game to help you understand the concept better!</p>
      </div>

      <ProgressDisplay />

      <div className="games-grid">
        {Object.entries(games).map(([key, game]) => (
          <div
            key={key}
            className={`game-card ${game.difficulty}`}
            onClick={() => setCurrentGame(key)}
          >
            <div className="game-icon">{game.icon}</div>
            <h3>{game.name}</h3>
            <p>{game.description}</p>
            <div className="difficulty-badge">{game.difficulty}</div>
          </div>
        ))}
      </div>

      <div className="selector-actions">
        <button className="exit-btn" onClick={onExit}>
          Back to Solution
        </button>
      </div>
    </div>
  );

  const renderCurrentGame = () => {
    switch (currentGame) {
      case 'step_builder':
        return <StepBuilderGame />;
      case 'concept_match':
        return <ConceptMatchGame />;
      default:
        return <GameSelector />;
    }
  };

  return (
    <div className="gamified-learning">
      <div className="game-container">
        {currentGame && (
          <div className="game-nav">
            <button 
              className="back-btn"
              onClick={() => setCurrentGame(null)}
            >
              ← Back to Games
            </button>
            <div className="game-progress">
              <div className="lives">
                {Array.from({ length: gameState.lives }, (_, i) => (
                  <span key={i} className="life">❤️</span>
                ))}
              </div>
              <div className="score">Score: {gameState.score}</div>
            </div>
          </div>
        )}

        {renderCurrentGame()}
      </div>
    </div>
  );
};

export default GameifiedLearning;