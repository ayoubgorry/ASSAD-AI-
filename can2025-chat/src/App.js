import React, { useState, useRef, useEffect } from 'react';
import { Send, Loader2, Sparkles, Trophy, MapPin, Calendar } from 'lucide-react';
import ReactMarkdown from 'react-markdown'; // N'oubliez pas de faire : npm install react-markdown
import logoCan from './logo.png';
import logoCanf from './logof.png';

const ChatInterface = () => {
  const [messages, setMessages] = useState([
    {
      role: 'assistant',
      content: 'Bienvenue sur la plateforme officielle d\'assistance de la CAN 2025. Je suis votre guide pour le tournoi au Maroc. Comment puis-je vous aider aujourd\'hui ? 🇲🇦⚽'
    }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  // Gestion du titre et du favicon
  useEffect(() => {
    document.title = "CAN 2025 - Assistant Officiel";
    const link = document.querySelector("link[rel~='icon']") || document.createElement('link');
    link.rel = 'icon';
    link.href = logoCanf;
    if (!document.querySelector("link[rel~='icon']")) {
      document.getElementsByTagName('head')[0].appendChild(link);
    }
    scrollToBottom();
  }, [messages]);

  const suggestedQuestions = [
    { text: "Stades & Villes", icon: <MapPin className="w-3 h-3" /> },
    { text: "Calendrier des matchs demi finale", icon: <Calendar className="w-3 h-3" /> },
    { text: "Informations sur le Gabon", icon: <Sparkles className="w-3 h-3" /> }
  ];

  const handleSend = async () => {
    if (!input.trim() || isLoading) return;
    const userMessage = { role: 'user', content: input };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      const response = await fetch('http://127.0.0.1:8000/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: input }),
      });
      const data = await response.json();
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: data.response || 'Désolé, une erreur est survenue.'
      }]);
    } catch (error) {
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: '❌ Erreur de connexion au serveur (Port 8000). Verifiez que votre API Python est lancée.'
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#004d3d] flex items-center justify-center p-2 sm:p-4 font-sans relative overflow-hidden">
      {/* Styles spécifiques pour le Markdown (Listes et gras) */}
      <style>{`
        .markdown-content ul { list-style-type: disc; margin-left: 1.5rem; margin-bottom: 1rem; }
        .markdown-content li { margin-bottom: 0.25rem; }
        .markdown-content strong { color: #c1272d; font-weight: 800; }
        .markdown-content p { margin-bottom: 0.75rem; }
      `}</style>

      {/* Background Pattern */}
      <div className="absolute inset-0 opacity-10 pointer-events-none" 
           style={{ backgroundImage: `url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M30 0l15 30-15 30L15 30z' fill='%23ffffff' fill-opacity='1' fill-rule='evenodd'/%3E%3C/svg%3E")`, backgroundSize: '40px 40px' }}>
      </div>

      <div className="w-full max-w-5xl h-[92vh] bg-white rounded-3xl shadow-2xl overflow-hidden flex flex-col border-4 border-[#c19d56] z-10">
        
        {/* Header */}
        <div className="bg-[#004d3d] p-5 text-white border-b-4 border-[#c1272d]">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <div className="bg-white p-2 rounded-lg">
                <img src={logoCan} alt="CAN 2025" className="w-16 h-16 object-contain" />
              </div>
              <div>
                <h1 className="text-xl sm:text-2xl font-black tracking-tight text-[#c19d56]">ASSAD AI : CAN 2025 ASSISTANT</h1>
                <div className="flex items-center gap-2">
                  <span className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></span>
                  <p className="text-xs uppercase tracking-widest font-bold text-gray-200">Support Officiel - Maroc</p>
                </div>
              </div>
            </div>
            <div className="hidden md:block">
               <Trophy className="text-[#c19d56] w-10 h-10 opacity-50" />
            </div>
          </div>
        </div>

        {/* Messages Area */}
        <div className="flex-1 overflow-y-auto p-4 sm:p-8 space-y-6 bg-[#f8f9fa]">
          {messages.map((message, index) => (
            <div key={index} className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}>
              <div className={`max-w-[85%] sm:max-w-[75%] rounded-2xl px-5 py-4 shadow-sm ${
                message.role === 'user'
                  ? 'bg-[#c1272d] text-white rounded-br-none'
                  : 'bg-white text-[#1a1a1a] rounded-bl-none border-l-4 border-[#004d3d]'
              }`}>
                {message.role === 'assistant' && (
                  <div className="flex items-center gap-2 mb-2 border-b border-gray-100 pb-1">
                    <Sparkles className="w-4 h-4 text-[#004d3d]" />
                    <span className="text-[10px] uppercase font-black text-[#004d3d] tracking-widest">Expert CAF</span>
                  </div>
                )}
                {/* Utilisation de ReactMarkdown pour corriger l'affichage des listes */}
                <div className="text-sm sm:text-base leading-relaxed markdown-content">
                  <ReactMarkdown>{message.content}</ReactMarkdown>
                </div>
              </div>
            </div>
          ))}
          
          {isLoading && (
            <div className="flex justify-start">
              <div className="bg-white rounded-2xl rounded-bl-none p-4 shadow-sm border border-gray-100 flex items-center gap-3">
                <Loader2 className="w-5 h-5 animate-spin text-[#004d3d]" />
                <span className="text-xs font-bold text-[#004d3d] uppercase tracking-widest">ASSAD prépare sa réponse...</span>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        {/* Input & Suggestions */}
        <div className="bg-white p-4 border-t border-gray-100">
          {messages.length === 1 && (
            <div className="mb-4">
              <div className="flex flex-wrap gap-2 justify-center">
                {suggestedQuestions.map((q, index) => (
                  <button
                    key={index}
                    onClick={() => setInput(q.text)}
                    className="flex items-center gap-2 text-xs font-bold bg-gray-50 hover:bg-[#004d3d] hover:text-white text-[#004d3d] px-4 py-2 rounded-full border border-[#004d3d]/20 transition-all duration-300"
                  >
                    {q.icon}
                    {q.text}
                  </button>
                ))}
              </div>
            </div>
          )}

          <div className="relative max-w-4xl mx-auto flex gap-3 items-center">
            <div className="relative flex-1">
              <textarea
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && !e.shiftKey && (e.preventDefault(), handleSend())}
                placeholder="Posez votre question sur la CAN 2025..."
                className="w-full resize-none bg-gray-100 border-2 border-transparent focus:border-[#004d3d] rounded-2xl px-5 py-4 pr-12 text-sm focus:outline-none transition-all"
                rows="1"
              />
              <button
                onClick={handleSend}
                disabled={isLoading || !input.trim()}
                className="absolute right-3 top-1/2 -translate-y-1/2 p-2 text-[#004d3d] hover:text-[#c1272d] disabled:text-gray-400 transition-colors"
              >
                {isLoading ? <Loader2 className="w-6 h-6 animate-spin" /> : <Send className="w-6 h-6" />}
              </button>
            </div>
          </div>
          <p className="text-[9px] text-center mt-3 text-gray-400 font-bold uppercase tracking-[0.2em]">
            TotalEnergies CAF Africa Cup of Nations • Morocco 2025
          </p>
        </div>
      </div>
    </div>
  );
};

export default ChatInterface;