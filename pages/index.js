const res = await fetch("https://tsmilitarylaw-backend.onrender.com/chat", {
  method: "POST",
  headers: {
    "Content-Type": "application/json"
  },
  body: JSON.stringify({ query: input })
});
