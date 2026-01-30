import { Send, ArrowLeft, Snowflake } from 'lucide-react';
import useChristmasStore from '../store/christmasStore';

const ChatView = ({ chatEndRef, onSearch }) => {
  const { query, history, isLoading, setView, setQuery } = useChristmasStore();

  return (
    <div className="flex flex-col h-screen bg-white">
      <div className="flex items-center px-4 py-4 border-b border-gray-100 bg-white sticky top-0 z-10">
        <button 
          onClick={() => setView('home')}
          type="button"
          className="p-2 hover:bg-gray-50 rounded-full transition-colors mr-2"
        >
          <ArrowLeft size={24} className="text-gray-700" />
        </button>
        <h1 className="text-xl font-bold text-gray-800">YuletideAI Chat</h1>
      </div>

      <div className="flex-1 overflow-y-auto p-4 space-y-6">
        {history.map((msg, idx) => (
          <div key={idx} className={`flex ${msg.type === 'user' ? 'justify-end' : 'justify-start'}`}>
            <div 
              className={`max-w-[85%] sm:max-w-[75%] p-4 rounded-2xl text-[15px] leading-relaxed ${
                msg.type === 'user' 
                  ? 'bg-gray-100 text-gray-800 rounded-tr-sm' 
                  : 'bg-white shadow-[0_2px_8px_rgba(0,0,0,0.05)] border border-gray-100 text-gray-700 rounded-tl-sm'
              }`}
            >
              {msg.content}
              
              {msg.chunks && msg.chunks.length > 0 && (
                <div className="mt-4 pt-4 border-t border-gray-100">
                  <p className="text-xs text-gray-500 mb-2 font-medium">Sources:</p>
                  {msg.chunks.map((chunk, i) => (
                    <div key={i} className="text-xs text-gray-600 mb-1">
                      • {chunk.section} ({(chunk.relevance * 100).toFixed(0)}% relevant)
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        ))}
        <div ref={chatEndRef} />
      </div>

      <div className="p-4 border-t border-gray-100 bg-white">
        <div className="relative max-w-4xl mx-auto flex items-center gap-2">
          <div className="relative flex-1">
             <div className="absolute left-4 top-1/2 -translate-y-1/2 text-blue-300">
               <Snowflake size={18} />
             </div>
             <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && onSearch(query)}
              placeholder="Ask a question..."
              className="w-full pl-10 pr-4 py-3 rounded-xl border border-gray-200 focus:outline-none focus:ring-2 focus:ring-red-100 focus:border-red-200 bg-white"
            />
          </div>
          <button 
            onClick={() => onSearch(query)}
            disabled={!query.trim() || isLoading}
            type="button"
            className="p-3 bg-red-400 text-white rounded-xl hover:bg-red-500 disabled:opacity-50 disabled:cursor-not-allowed transition-colors shadow-sm"
          >
            <Send size={20} />
          </button>
        </div>
        <div className="text-center mt-2">
          <p className="text-[10px] text-gray-400">AI can make mistakes. Verify information.</p>
        </div>
      </div>
    </div>
  );
};

export default ChatView;
