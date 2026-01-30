import { create } from 'zustand';

const useChristmasStore = create((set, get) => ({
  view: 'home',
  query: '',
  history: [],
  isLoading: false,

  setView: (view) => set({ view }),
  setQuery: (query) => set({ query }),
  setIsLoading: (isLoading) => set({ isLoading }),
  
  addUserMessage: (content) => set((state) => ({
    history: [...state.history, { type: 'user', content }]
  })),
  
  updateAIMessage: (content, chunks = null) => set((state) => {
    const newHistory = [...state.history];
    const lastMsg = newHistory[newHistory.length - 1];
    
    if (lastMsg && lastMsg.type === 'ai') {
      lastMsg.content = content;
      if (chunks) lastMsg.chunks = chunks;
    } else {
      newHistory.push({ type: 'ai', content, chunks });
    }
    
    return { history: newHistory };
  }),
  
  addErrorMessage: (content) => set((state) => ({
    history: [...state.history, { type: 'ai', content }]
  })),
  
  clearQuery: () => set({ query: '' }),
}));

export default useChristmasStore;
