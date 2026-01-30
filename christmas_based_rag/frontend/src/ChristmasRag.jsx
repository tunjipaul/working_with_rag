import { useRef, useEffect } from 'react';
import useChristmasStore from './store/christmasStore';
import { useSearch } from './hooks/useSearch';
import HomeView from './components/HomeView';
import ChatView from './components/ChatView';

const ChristmasRag = () => {
  const chatEndRef = useRef(null);
  const { view, history } = useChristmasStore();
  const { handleSearch } = useSearch();

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [history]);

  return (
    <div className="min-h-screen bg-white">
      {view === 'home' ? (
        <HomeView onSearch={handleSearch} />
      ) : (
        <ChatView chatEndRef={chatEndRef} onSearch={handleSearch} />
      )}
    </div>
  );
};

export default ChristmasRag;