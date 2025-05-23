import { useState } from "react";

export default function Home() {
  const [messages, setMessages] = useState([
    { role: "system", content: "Ask me anything about Military Law." }
  ]);
  const [input, setInput] = useState("");

  const sendMessage = async () => {
    if (!input.trim()) return;

    const newMessages = [...messages, { role: "user", content: input }];
    setMessages(newMessages);
    setInput("");

    try {
      const res = await fetch("https://tsmilitarylaw-backend.onrender.com/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: input })
      });

      const data = await res.json();
      const reply = data.message || "No response received.";

      setMessages([...newMessages, { role: "assistant", content: reply }]);
    } catch (err) {
      setMessages([...newMessages, { role: "assistant", content: "Error contacting backend." }]);
    }
  };

  return (
    <div style={{ padding: 20, fontFamily: "monospace" }}>
      <h1>TSMilitaryLaw Chatbot</h1>
      <div style={{
        background: "#f4f4f4", padding: 15, border: "1px solid #ccc", minHeight: "300px", whiteSpace: "pre-wrap"
      }}>
        {messages.map((msg, i) => (
          <p key={i}><strong>{msg.role}:</strong> {msg.content}</p>
        ))}
      </div>
      <div style={{ marginTop: 20 }}>
        <input
          value={input}
          onChange={e => setInput(e.target.value)}
          placeholder="Ask a question like 'What is Sec 41 Army Act?'"
          style={{ width: "80%", padding: 8 }}
        />
        <button onClick={sendMessage} style={{ padding: "8px 16px", marginLeft: 10 }}>Send</button>
      </div>
    </div>
  );
}
