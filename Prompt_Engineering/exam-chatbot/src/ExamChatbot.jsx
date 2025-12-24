import React, { useState, useEffect } from 'react';
import { Send, BookOpen, CheckCircle, XCircle } from 'lucide-react';

function ExamChatbot() {
  const [subject, setSubject] = useState('');
  const [topic, setTopic] = useState('');
  const [sessionStarted, setSessionStarted] = useState(false);
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [questions, setQuestions] = useState([]);
  const [selectedAnswer, setSelectedAnswer] = useState('');
  const [answered, setAnswered] = useState(false);
  const [score, setScore] = useState(0);
  const [loading, setLoading] = useState(false);
  const [sessionComplete, setSessionComplete] = useState(false);
  const [nextQuestions, setNextQuestions] = useState(null); // UPDATED: Added prefetch state

  const subjects = [
    'Mathematics',
    'English Language',
    'Biology',
    'Chemistry',
    'Physics',
    'Social Studies',
    'Literature',
  ];

  const topics = {
    Mathematics: ['Algebra', 'Geometry', 'Trigonometry', 'Statistics', 'Calculus'],
    'English Language': ['Grammar', 'Comprehension', 'Vocabulary', 'Essay Writing'],
    Biology: ['Cells', 'Genetics', 'Ecology', 'Photosynthesis', 'Respiration'],
    Chemistry: ['Atomic Structure', 'Chemical Bonding', 'Reactions', 'States of Matter'],
    Physics: ['Mechanics', 'Thermodynamics', 'Waves', 'Electricity', 'Magnetism'],
    'Social Studies': ['History', 'Government', 'Geography', 'Economics'],
    Literature: ['Poetry', 'Prose', 'Drama', 'Literary Devices'],
  };

  const generateQuestions = async () => {
    setLoading(true);
    try {
      const apiKey = import.meta.env.VITE_GEMINI_API_KEY;

      const response = await fetch(
        `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=${apiKey}`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            contents: [
              {
                parts: [
                  {
                    text: `Generate 5 multiple-choice exam questions for ${subject} - ${topic}. 
                    
                    Return ONLY a valid JSON array with this exact structure, no other text:
                    [
                      {
                        "question": "Question text here?",
                        "options": ["Option A", "Option B", "Option C", "Option D"],
                        "correct": 0,
                        "explanation": "Why this is correct and others are wrong"
                      }
                    ]
                    
                    Make questions appropriate for WAEC, JAMB, or NECO exams. Correct answer index should be 0, 1, 2, or 3.`,
                  },
                ],
              },
            ],
          }),
        }
      );

      const data = await response.json();
      
      if (data.error) {
        alert('Error: ' + data.error.message);
        setLoading(false);
        return;
      }

      const text = data.candidates[0].content.parts[0].text.replace(/```json|```/g, '').trim();
      const parsedQuestions = JSON.parse(text);
      setQuestions(parsedQuestions);
      setSessionStarted(true);
      setCurrentQuestion(0);
      setScore(0);
      setAnswered(false);
      setSelectedAnswer('');
      setSessionComplete(false);
    } catch (error) {
      alert('Error generating questions. Please check your .env file and try again.');
      console.error(error);
    }
    setLoading(false);
  };

  // UPDATED: Added prefetch function and useEffect
  const prefetchQuestions = async (subj, top) => {
    try {
      const apiKey = import.meta.env.VITE_GEMINI_API_KEY;

      const response = await fetch(
        `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=${apiKey}`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            contents: [
              {
                parts: [
                  {
                    text: `Generate 5 multiple-choice exam questions for ${subj} - ${top}. 
                    
                    Return ONLY a valid JSON array with this exact structure, no other text:
                    [
                      {
                        "question": "Question text here?",
                        "options": ["Option A", "Option B", "Option C", "Option D"],
                        "correct": 0,
                        "explanation": "Why this is correct and others are wrong"
                      }
                    ]
                    
                    Make questions appropriate for WAEC, JAMB, or NECO exams. Correct answer index should be 0, 1, 2, or 3.`,
                  },
                ],
              },
            ],
          }),
        }
      );

      const data = await response.json();
      if (data.error) {
        console.error('Prefetch error:', data.error.message);
        return;
      }

      const text = data.candidates[0].content.parts[0].text.replace(/```json|```/g, '').trim();
      const parsedQuestions = JSON.parse(text);
      setNextQuestions(parsedQuestions);
    } catch (error) {
      console.error('Prefetch error:', error);
    }
  };

  // UPDATED: useEffect for prefetching when subject/topic changes
  useEffect(() => {
    if (subject && topic && !sessionStarted) {
      prefetchQuestions(subject, topic);
    }
  }, [subject, topic, sessionStarted]);

  const handleStartSession = () => {
    if (subject && topic) {
      generateQuestions();
    } else {
      alert('Please select both subject and topic');
    }
  };

  const handleAnswerSelect = (index) => {
    if (!answered) {
      setSelectedAnswer(index);
    }
  };

  const handleSubmitAnswer = () => {
    if (selectedAnswer === '') {
      alert('Please select an answer');
      return;
    }

    setAnswered(true);
    if (selectedAnswer === questions[currentQuestion].correct) {
      setScore(score + 1);
    }
  };

  const handleNextQuestion = () => {
    if (currentQuestion < questions.length - 1) {
      setCurrentQuestion(currentQuestion + 1);
      setSelectedAnswer('');
      setAnswered(false);
    } else {
      setSessionComplete(true);
    }
  };

  const handleRestart = () => {
    setSubject('');
    setTopic('');
    setSessionStarted(false);
    setCurrentQuestion(0);
    setQuestions([]);
    setSelectedAnswer('');
    setAnswered(false);
    setScore(0);
    setSessionComplete(false);
  };

  if (sessionComplete) {
    return (
      <div className="min-h-screen bg-linear-to-br from-purple-600 to-purple-800 flex items-center justify-center p-4">
        <div className="bg-white rounded-lg shadow-2xl p-8 max-w-md w-full text-center">
          <BookOpen className="w-16 h-16 text-purple-600 mx-auto mb-4" />
          <h2 className="text-3xl font-bold text-gray-800 mb-2">Quiz Complete!</h2>
          <p className="text-4xl font-bold text-purple-600 mb-2">{score}/5</p>
          <p className="text-gray-600 mb-6">
            {score === 5
              ? "Perfect score! You're ready for the exam!"
              : score >= 3
              ? 'Great job! Keep practicing.'
              : 'Keep studying and try again!'}
          </p>
          <button
            onClick={handleRestart}
            className="bg-purple-600 text-white px-6 py-2 rounded-lg hover:bg-purple-700 transition font-semibold"
          >
            Start New Session
          </button>
        </div>
      </div>
    );
  }

  if (!sessionStarted) {
    return (
      <div className="min-h-screen bg-linear-to-br from-purple-600 to-purple-800 flex items-center justify-center p-4">
        <div className="bg-white rounded-lg shadow-2xl p-8 max-w-md w-full">
          <div className="flex items-center justify-center mb-6">
            <BookOpen className="w-12 h-12 text-purple-600 mr-2" />
            <h1 className="text-3xl font-bold text-gray-800">Exam Tutor</h1>
          </div>

          <div className="mb-6">
            <label className="block text-gray-700 font-semibold mb-2">
              Select Subject
            </label>
            <select
              value={subject}
              onChange={(e) => {
                setSubject(e.target.value);
                setTopic('');
              }}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-purple-600"
            >
              <option value="">Choose a subject...</option>
              {subjects.map((s) => (
                <option key={s} value={s}>
                  {s}
                </option>
              ))}
            </select>
          </div>

          {subject && (
            <div className="mb-6">
              <label className="block text-gray-700 font-semibold mb-2">
                Select Topic
              </label>
              <select
                value={topic}
                onChange={(e) => setTopic(e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-purple-600"
              >
                <option value="">Choose a topic...</option>
                {topics[subject]?.map((t) => (
                  <option key={t} value={t}>
                    {t}
                  </option>
                ))}
              </select>
            </div>
          )}

          <button
            onClick={handleStartSession}
            disabled={loading || !subject || !topic}
            className="w-full bg-purple-600 text-white px-6 py-3 rounded-lg hover:bg-purple-700 transition disabled:bg-gray-400 font-semibold"
          >
            {loading ? 'Generating Questions...' : 'Start Practice Session'}
          </button>
        </div>
      </div>
    );
  }

  if (questions.length === 0) {
    return (
      <div className="min-h-screen bg-linear-to-br from-purple-600 to-purple-800 flex items-center justify-center p-4">
        <div className="text-white text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-white mx-auto mb-4"></div>
          <p>Generating questions...</p>
        </div>
      </div>
    );
  }

  const q = questions[currentQuestion];
  const optionLabels = ['A', 'B', 'C', 'D'];

  return (
    <div className="min-h-screen bg-linear-to-br from-purple-600 to-purple-800 flex items-center justify-center p-4">
      <div className="bg-white rounded-lg shadow-2xl p-8 max-w-2xl w-full">
        <div className="flex justify-between items-center mb-6">
          <h2 className="text-2xl font-bold text-gray-800">
            {subject} - {topic}
          </h2>
          <span className="text-purple-600 font-semibold">
            Question {currentQuestion + 1}/5
          </span>
        </div>

        <div className="bg-gray-50 p-4 rounded-lg mb-6">
          <p className="text-lg text-gray-800 font-semibold mb-4">{q.question}</p>

          <div className="space-y-3">
            {q.options.map((option, idx) => (
              <button
                key={idx}
                onClick={() => handleAnswerSelect(idx)}
                disabled={answered}
                className={`w-full p-4 text-left rounded-lg border-2 transition ${
                  selectedAnswer === idx
                    ? 'border-purple-600 bg-purple-50'
                    : 'border-gray-200 hover:border-purple-400'
                } ${answered ? 'cursor-default' : 'cursor-pointer'}
                ${
                  answered && idx === q.correct
                    ? 'border-green-500 bg-green-50'
                    : ''
                }
                ${
                  answered && selectedAnswer === idx && idx !== q.correct
                    ? 'border-red-500 bg-red-50'
                    : ''
                }`}
              >
                <div className="flex items-center justify-between">
                  <span className="font-semibold text-gray-700">
                    {optionLabels[idx]}) {option}
                  </span>
                  {answered && idx === q.correct && (
                    <CheckCircle className="w-5 h-5 text-green-600" />
                  )}
                  {answered && selectedAnswer === idx && idx !== q.correct && (
                    <XCircle className="w-5 h-5 text-red-600" />
                  )}
                </div>
              </button>
            ))}
          </div>
        </div>

        {answered && (
          <div
            className={`p-4 rounded-lg mb-6 ${
              selectedAnswer === q.correct
                ? 'bg-green-50 border border-green-200'
                : 'bg-red-50 border border-red-200'
            }`}
          >
            <p
              className={`font-semibold mb-2 ${
                selectedAnswer === q.correct ? 'text-green-800' : 'text-red-800'
              }`}
            >
              {selectedAnswer === q.correct ? '✓ Correct!' : '✗ Incorrect'}
            </p>
            <p className="text-gray-700 text-sm">{q.explanation}</p>
          </div>
        )}

        <div className="flex gap-4">
          {!answered ? (
            <button
              onClick={handleSubmitAnswer}
              className="flex-1 bg-purple-600 text-white px-6 py-3 rounded-lg hover:bg-purple-700 transition font-semibold flex items-center justify-center gap-2"
            >
              <Send className="w-4 h-4" />
              Submit Answer
            </button>
          ) : (
            <button
              onClick={handleNextQuestion}
              className="flex-1 bg-purple-600 text-white px-6 py-3 rounded-lg hover:bg-purple-700 transition font-semibold"
            >
              {currentQuestion === questions.length - 1
                ? 'See Results'
                : 'Next Question'}
            </button>
          )}
        </div>

        <div className="mt-6 bg-gray-100 p-3 rounded-lg">
          <p className="text-gray-700 text-sm">
            <span className="font-semibold">Score: {score}/{currentQuestion}</span>
          </p>
          <div className="w-full bg-gray-300 rounded-full h-2 mt-2">
            <div
              className="bg-purple-600 h-2 rounded-full transition-all"
              style={{ width: `${((currentQuestion + 1) / 5) * 100}%` }}
            ></div>
          </div>
        </div>
      </div>
    </div>
  );
}
export default ExamChatbot;