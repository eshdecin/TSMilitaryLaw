import { useState } from 'react';

export default function Home() {
  const [messages, setMessages] = useState([{ role: 'system', content: 'Ask me anything about Military Law.' }]);
  const [input, setInput] = useState('');

  const handleSend = () => {
    if (!input.trim()) return;
    const userMessage = { role: 'user', content: input };
    const botReply = {
      role: 'assistant',
      content: `This is a placeholder answer for: "${input}" (The real brain is coming soon, Sir!)`
    };
    setMessages([...messages, userMessage, botReply]);
    setInput('');
  };

  return (
    <main style={{ fontFamily: 'monospace', padding: '2rem' }}>
      <h1>TSMilitaryLaw Chatbot</h1>
      <div style={{ border: '1px solid #ccc', padding: '1rem', height: '300px', overflowY: 'scroll', marginBottom: '1rem' }}>
        {messages.map((msg, i) => (
          <div key={i}><strong>{msg.role === 'user' ? 'You' : msg.role}:</strong> {msg.content}</div>
        ))}
      </div>
      <input
        style={{ width: '80%', padding: '0.5rem' }}
        value={input}
        onChange={e => setInput(e.target.value)}
        onKeyDown={e => e.key === 'Enter' && handleSend()}
        placeholder="Ask a question like 'What is Sec 41 Army Act?'"
      />
      <button onClick={handleSend} style={{ marginLeft: '1rem', padding: '0.5rem 1rem' }}>Send</button>
    </main>
  );
}
