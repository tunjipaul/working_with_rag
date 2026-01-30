import useChristmasStore from '../store/christmasStore';
import { API_URL } from '../constants';

export const useSearch = () => {
  const { 
    setView,
    setIsLoading,
    addUserMessage,
    updateAIMessage,
    addErrorMessage,
    clearQuery,
    history
  } = useChristmasStore();

  const handleSearch = async (searchQuery) => {
    if (!searchQuery?.trim()) return;

    // Switch to chat view and add user message
    setView('chat');
    addUserMessage(searchQuery);
    clearQuery();
    setIsLoading(true);

    // Format history for API (convert to role/content format)
    const formattedHistory = history.map(msg => ({
      role: msg.type === 'user' ? 'user' : 'assistant',
      content: msg.content
    }));

    try {
      const response = await fetch(`${API_URL}/search/stream`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          query: searchQuery, 
          n_results: 3,
          history: formattedHistory
        })
      });

      if (!response.ok) throw new Error('Network response was not ok');

      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let buffer = '';
      let currentAnswer = '';
      let chunks = [];

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split('\n');
        buffer = lines.pop() || '';

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            try {
              const data = JSON.parse(line.slice(6));
              
              if (data.token) {
                currentAnswer += data.token;
                updateAIMessage(currentAnswer);
              } else if (data.chunks) {
                chunks = data.chunks;
                updateAIMessage(currentAnswer, chunks);
              } else if (data.done) {
                setIsLoading(false);
              } else if (data.error) {
                throw new Error(data.error);
              }
            } catch (e) {
              console.error('Parse error:', e);
            }
          }
        }
      }

    } catch (err) {
      setIsLoading(false);
      addErrorMessage("Sorry, I'm having trouble connecting to the North Pole servers right now. Please try again later.");
    }
  };

  return { handleSearch };
};
