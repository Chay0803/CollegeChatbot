const chatBox = document.getElementById("chat-box");
const chatForm = document.getElementById("chat-form");
const chatInput = document.getElementById("chat-input");

// Add message bubbles to chat
function addMessage(role, text) {
  const msg = document.createElement("div");
  msg.className = `chat-message ${role}-message`;

  // Convert Markdown to HTML using marked.js
  try {
    msg.innerHTML = marked.parse(text);
  } catch (err) {
    console.error("Markdown parse error:", err);
    msg.textContent = text; // fallback
  }

  chatBox.appendChild(msg);
  chatBox.scrollTop = chatBox.scrollHeight;
}

// Simulated typing animation
function showTypingIndicator() {
  const indicator = document.createElement("div");
  indicator.className = "chat-message bot-message typing";
  indicator.textContent = "Assistant is typing...";
  chatBox.appendChild(indicator);
  chatBox.scrollTop = chatBox.scrollHeight;
}

function removeTypingIndicator() {
  const indicator = chatBox.querySelector(".typing");
  if (indicator) indicator.remove();
}

chatForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  const userMessage = chatInput.value.trim();
  if (!userMessage) return;

  addMessage("user", userMessage);
  chatInput.value = "";
  showTypingIndicator();

  try {
    const response = await fetch("/chat", {
      method: "POST",
      body: new URLSearchParams({ user_message: userMessage }),
    });

    const data = await response.json();
    removeTypingIndicator();
    addMessage("bot", marked.parse(data.answer)); // render markdown

  } catch (err) {
    console.error("⚠️ Chat error:", err);
    removeTypingIndicator();
    addMessage("bot", "⚠️ Error connecting to server. Please try again.");
  }
});

