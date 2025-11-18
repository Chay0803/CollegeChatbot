
const chatBox = document.getElementById("chat-box");
const chatForm = document.getElementById("chat-form");
const chatInput = document.getElementById("chat-input");


function addMessage(role, text) {
  const msg = document.createElement("div");
  msg.className = `chat-message ${role}-message`;

  try {
    msg.innerHTML = marked.parse(text); 
  } catch {
    msg.textContent = text;
  }

  chatBox.appendChild(msg);
  chatBox.scrollTop = chatBox.scrollHeight;
}


function showTyping() {
  const tip = document.createElement("div");
  tip.className = "chat-message bot-message typing";
  tip.textContent = "Assistant is typing";
  chatBox.appendChild(tip);
  chatBox.scrollTop = chatBox.scrollHeight;
}

function removeTyping() {
  const t = chatBox.querySelector(".typing");
  if (t) t.remove();
}

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}


chatInput.addEventListener("keydown", function (e) {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    chatForm.dispatchEvent(new Event("submit"));
  }
});


chatForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  const userMsg = chatInput.value.trim();
  if (!userMsg) return;

  addMessage("user", userMsg);
  chatInput.value = "";
  showTyping();

  try {
    const res = await fetch("/digital_icfai_chat", {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body: new URLSearchParams({ user_message: userMsg }),
    });

    const data = await res.json();
    await sleep(400); 
    removeTyping();
    addMessage("bot", data.answer || "⚠️ No response received.");
  } catch (err) {
    removeTyping();
    addMessage("bot", "⚠️ Error connecting to server.");
    console.error(err);
  }
});
