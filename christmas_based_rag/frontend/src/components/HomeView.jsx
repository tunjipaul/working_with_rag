import { Search, Sparkles, Snowflake, LucideTrees } from 'lucide-react';
import useChristmasStore from '../store/christmasStore';
import { suggestedQuestions } from '../constants';

const HomeView = ({ onSearch }) => {
  const { query, setQuery } = useChristmasStore();

  return (
    <div className="flex flex-col items-center justify-center min-h-screen px-4 max-w-2xl mx-auto w-full relative">
      <Snowflake className="absolute top-20 left-10 text-yellow-200 opacity-60" size={32} />
      <Sparkles className="absolute top-32 right-16 text-red-100 opacity-80" size={40} />
      <LucideTrees className="absolute top-10 right-10 text-green-700 opacity-20" size={64} />
      <div className="absolute bottom-32 left-10 opacity-40 text-4xl">
        🎄
      </div>

      <div className="text-center mb-12 relative z-10">
        <h1 className="text-5xl md:text-6xl font-serif text-gray-900 mb-4 tracking-tight">
          YuletideAI
        </h1>
      </div>

      <div className="w-full relative mb-12 shadow-sm">
        <div className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-400">
          <Search size={20} />
        </div>
        <input 
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && onSearch(query)}
          placeholder="What would you like to know about Christmas?"
          className="w-full pl-12 pr-4 py-4 rounded-xl border border-gray-200 focus:outline-none focus:ring-2 focus:ring-green-100 focus:border-green-300 text-gray-600 shadow-sm transition-all"
        />
      </div>

      <div className="w-full">
        <h2 className="text-lg font-semibold text-gray-800 mb-4">Suggested Questions</h2>
        <div className="flex flex-wrap gap-3">
          {suggestedQuestions.map((q, idx) => (
            <button
              key={idx}
              onClick={() => onSearch(q)}
              type="button"
              className="px-5 py-3 rounded-full bg-green-50 text-green-800 border border-green-100 hover:bg-green-100 transition-colors text-sm font-medium"
            >
              {q}
            </button>
          ))}
        </div>
      </div>

      <div className="absolute bottom-8 text-gray-400 text-xs text-center px-4">
        AI can make mistakes. Verify information.
      </div>
    </div>
  );
};

export default HomeView;
