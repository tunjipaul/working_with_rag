import { useState } from 'react';
import { Search, Sparkles, Gift, TreePine, Star, Loader2, Snowflake, Flame } from 'lucide-react';

const ChristmasRag = () => {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  
  const handleSearch = async () => {
    if (!query.trim()) return;

    setIsLoading(true);
    setError(null);
    
    try {
    
      const response = await fetch('http://localhost:8000/search', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        }, 
        body: JSON.stringify({
          query: query,
          n_results: 3
        })
      });

     
      if (!response.ok) {
        throw new Error(`API Error: ${response.statusText}`);
      }

      
      const data = await response.json();
      
      
      setResults({
        answer: data.chunks.length > 0 
          ? data.chunks[0].text 
          : "No information found about this topic.",
        chunks: data.chunks.map((chunk, idx) => ({
          id: idx + 1,
          text: chunk.text,
          section: chunk.section,
          relevance: chunk.relevance
        }))
      });
    } catch (err) {
      console.error('Error:', err);
      setError(err.message || 'Failed to fetch results. Make sure FastAPI backend is running on port 8000.');
    } finally {
      setIsLoading(false);
    }
  };

  const clearSearch = () => {
    setQuery('');
    setResults(null);
    setError(null);
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      handleSearch();
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-red-50 via-white to-green-50">
      {/* Decorative Background Elements */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none hidden md:block">
        <Snowflake className="absolute top-10 left-10 text-blue-200 opacity-30 animate-spin" size={40} style={{animationDuration: '20s'}} />
        <Snowflake className="absolute top-32 right-20 text-blue-200 opacity-20 animate-spin" size={32} style={{animationDuration: '15s'}} />
        <Snowflake className="absolute bottom-20 left-1/4 text-blue-200 opacity-25 animate-spin" size={48} style={{animationDuration: '25s'}} />
        <Star className="absolute top-20 right-1/4 text-yellow-300 opacity-40 animate-pulse" size={32} />
        <Star className="absolute bottom-32 right-10 text-yellow-300 opacity-30 animate-pulse" size={24} />
      </div>

      {/* Header */}
      <header className="relative bg-gradient-to-r from-red-700 via-red-600 to-green-700 text-white shadow-2xl">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 py-6 sm:py-8">
          <div className="flex items-center justify-center gap-2 sm:gap-4">
            <TreePine className="text-green-200" size={32} />
            <h1 className="text-3xl sm:text-4xl md:text-5xl font-bold text-center">
              Christmas Knowledge Base
            </h1>
            <Gift className="text-red-200" size={32} />
          </div>
          <p className="text-center text-red-100 mt-2 sm:mt-3 text-base sm:text-lg px-4">
            Ask me anything about Christmas traditions, history, and celebrations
          </p>
          <p className="text-center text-red-50 text-xs sm:text-sm mt-2">
            Powered by FastAPI + ChromaDB RAG System
          </p>
        </div>
      </header>

      {/* Main Content */}
      <main className="relative max-w-6xl mx-auto px-4 sm:px-6 py-8 sm:py-12">
        {/* Search Section */}
        <div className="bg-white rounded-2xl shadow-xl p-4 sm:p-6 md:p-8 border-4 border-red-200">
          <div className="space-y-3 sm:space-y-4">
            <div className="relative">
              <Search className="absolute left-3 sm:left-4 top-1/2 transform -translate-y-1/2 text-red-400" size={20} />
              <input
                type="text"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                onKeyDown={handleKeyPress}
                placeholder="What would you like to know about Christmas?"
                className="w-full pl-10 sm:pl-14 pr-3 sm:pr-4 py-3 sm:py-4 text-base sm:text-lg border-2 border-green-300 rounded-xl focus:outline-none focus:ring-4 focus:ring-red-300 focus:border-red-400 transition-all"
              />
            </div>
            
            <div className="flex flex-col sm:flex-row gap-3">
              <button
                onClick={handleSearch}
                disabled={isLoading || !query.trim()}
                className="w-full sm:flex-1 bg-gradient-to-r from-red-600 to-red-700 text-white py-3 sm:py-4 px-6 rounded-xl font-semibold text-base sm:text-lg hover:from-red-700 hover:to-red-800 disabled:opacity-50 disabled:cursor-not-allowed transition-all transform hover:scale-105 active:scale-95 shadow-lg flex items-center justify-center gap-2"
              >
                {isLoading ? (
                  <>
                    <Loader2 className="animate-spin" size={20} />
                    Searching...
                  </>
                ) : (
                  <>
                    <Sparkles size={20} />
                    Search
                  </>
                )}
              </button>
              
              {(results || error) && (
                <button
                  onClick={clearSearch}
                  className="w-full sm:w-auto bg-green-600 text-white py-3 sm:py-4 px-6 sm:px-8 rounded-xl font-semibold text-base sm:text-lg hover:bg-green-700 transition-all transform hover:scale-105 active:scale-95 shadow-lg"
                >
                  Clear
                </button>
              )}
            </div>

            {/* Error Message */}
            {error && (
              <div className="bg-red-100 border-2 border-red-400 text-red-800 px-4 py-3 rounded-lg">
                <p className="font-semibold">Error</p>
                <p className="text-sm">{error}</p>
                <p className="text-xs mt-2">Make sure FastAPI backend is running: <code className="bg-red-200 px-2 py-1 rounded">uvicorn main:app --reload --port 8000</code></p>
              </div>
            )}
          </div>

          {/* Sample Questions */}
          {!results && !error && (
            <div className="mt-6 sm:mt-8 pt-6 sm:pt-8 border-t-2 border-green-200">
              <div className="flex items-center gap-2 mb-3 sm:mb-4">
                <Flame className="text-yellow-500" size={20} />
                <h3 className="text-base sm:text-lg font-semibold text-gray-700">Try asking:</h3>
              </div>
              <div className="flex flex-wrap gap-2">
                {[
                  "When is Christmas celebrated?",
                  "Who is Santa Claus?",
                  "What are Christmas traditions?",
                  "What do people eat at Christmas?",
                  "How is Christmas celebrated around the world?"
                ].map((question, idx) => (
                  <button
                    key={idx}
                    onClick={() => setQuery(question)}
                    className="bg-green-100 hover:bg-green-200 text-green-800 px-3 sm:px-4 py-2 rounded-lg text-xs sm:text-sm font-medium transition-all border-2 border-green-300 hover:border-green-400"
                  >
                    {question}
                  </button>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* Results Section */}
        {results && !error && (
          <div className="mt-6 sm:mt-8 space-y-4 sm:space-y-6">
            {/* Answer Card */}
            <div className="bg-gradient-to-br from-green-50 to-red-50 rounded-2xl shadow-xl p-4 sm:p-6 md:p-8 border-4 border-green-300">
              <div className="flex items-center gap-2 sm:gap-3 mb-3 sm:mb-4">
                <div className="bg-red-600 p-1.5 sm:p-2 rounded-lg">
                  <Sparkles className="text-white" size={20} />
                </div>
                <h2 className="text-xl sm:text-2xl font-bold text-gray-800">Answer</h2>
              </div>
              <p className="text-base sm:text-lg text-gray-700 leading-relaxed">
                {results.answer}
              </p>
            </div>

            {/* Source Chunks */}
            <div className="bg-white rounded-2xl shadow-xl p-4 sm:p-6 md:p-8 border-4 border-red-200">
              <div className="flex items-center gap-2 sm:gap-3 mb-4 sm:mb-6">
                <Star className="text-yellow-500" size={24} />
                <h2 className="text-xl sm:text-2xl font-bold text-gray-800">
                  Source References ({results.chunks.length})
                </h2>
              </div>
              
              <div className="space-y-3 sm:space-y-4">
                {results.chunks.map((chunk, idx) => (
                  <div
                    key={chunk.id}
                    className="bg-gradient-to-r from-red-50 to-green-50 p-4 sm:p-6 rounded-xl border-2 border-green-200 hover:border-green-400 transition-all hover:shadow-lg"
                  >
                    <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 sm:gap-4 mb-3">
                      <div className="flex items-center gap-2 sm:gap-3">
                        <div className="bg-red-600 text-white w-7 h-7 sm:w-8 sm:h-8 rounded-full flex items-center justify-center font-bold text-sm sm:text-base flex-shrink-0">
                          {idx + 1}
                        </div>
                        <span className="text-xs sm:text-sm font-semibold text-green-700 bg-green-100 px-2 sm:px-3 py-1 rounded-full">
                          {chunk.section}
                        </span>
                      </div>
                      <div className="flex items-center gap-2 ml-9 sm:ml-0">
                        <div className="w-12 sm:w-16 h-2 bg-gray-200 rounded-full overflow-hidden">
                          <div 
                            className="h-full bg-gradient-to-r from-green-500 to-red-500"
                            style={{ width: `${chunk.relevance * 100}%` }}
                          />
                        </div>
                        <span className="text-xs font-medium text-gray-600">
                          {Math.round(chunk.relevance * 100)}%
                        </span>
                      </div>
                    </div>
                    <p className="text-sm sm:text-base text-gray-700 leading-relaxed">
                      {chunk.text}
                    </p>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* Info Footer */}
        {!results && !error && (
          <div className="mt-8 sm:mt-12 text-center">
            <div className="inline-flex flex-col sm:flex-row items-center gap-2 sm:gap-3 bg-white px-4 sm:px-8 py-3 sm:py-4 rounded-full shadow-lg border-2 border-yellow-300">
              <TreePine className="text-green-600 hidden sm:block" size={28} />
              <p className="text-gray-600 font-medium text-sm sm:text-base text-center">
                Powered by FastAPI, ChromaDB, and Sentence Embeddings
              </p>
              <Gift className="text-red-600 hidden sm:block" size={28} />
            </div>
          </div>
        )}
      </main>
    </div>
  );
};

export default ChristmasRag;