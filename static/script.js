// Tab switching
const tabs = document.querySelectorAll(".tab");
const contents = document.querySelectorAll(".tab-content");

tabs.forEach(tab => {
  tab.addEventListener("click", () => {
    tabs.forEach(t => t.classList.remove("active"));
    contents.forEach(c => c.classList.remove("active"));
    tab.classList.add("active");
    document.getElementById(tab.dataset.tab).classList.add("active");
  });
});

// Chatbot
const chatForm = document.getElementById("chat-form");
const chatBox = document.getElementById("chat-box");
const chatInput = document.getElementById("chat-input");

chatForm?.addEventListener("submit", async (e) => {
  e.preventDefault();
  const message = chatInput.value.trim();
  if (!message) return;
  addMessage("user", message);
  chatInput.value = "";

  addMessage("bot", "Typing...");

  const res = await fetch("/chat", {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: new URLSearchParams({ user_message: message })
  });

  const data = await res.json();
  removeLastBot();
  addMessage("bot", data.answer);
});

function addMessage(role, text) {
  const div = document.createElement("div");
  div.className = `chat-message ${role}-message`;
  div.innerHTML = text;
  chatBox.appendChild(div);
  chatBox.scrollTop = chatBox.scrollHeight;
}

function removeLastBot() {
  const bots = chatBox.querySelectorAll(".bot-message");
  if (bots.length) bots[bots.length - 1].remove();
}

// Course Recommender
const courseForm = document.getElementById("course-form");
courseForm?.addEventListener("submit", async (e) => {
  e.preventDefault();
  const formData = new FormData(courseForm);
  const res = await fetch("/recommend", { method: "POST", body: formData });
  const data = await res.json();

  const resultsDiv = document.getElementById("course-results");
  if (data.recommendations?.length) {
    resultsDiv.innerHTML = `<strong>Recommended Courses:</strong><ul>${data.recommendations.map(c => `<li>${c}</li>`).join("")}</ul>`;
  } else {
    resultsDiv.textContent = "No matching courses found or invalid input.";
  }
});

// Employee Lookup
const empForm = document.getElementById("employee-form");
empForm?.addEventListener("submit", async (e) => {
  e.preventDefault();
  const formData = new FormData(empForm);
  const res = await fetch("/employees/search", { method: "POST", body: formData });
  const data = await res.json();

  const resultsDiv = document.getElementById("employee-results");
  if (data.results?.length) {
    const table = `
      <table>
        <thead>
          <tr>${Object.keys(data.results[0]).map(k => `<th>${k}</th>`).join("")}</tr>
        </thead>
        <tbody>
          ${data.results.map(r => `<tr>${Object.values(r).map(v => `<td>${v}</td>`).join("")}</tr>`).join("")}
        </tbody>
      </table>`;
    resultsDiv.innerHTML = table;
  } else {
    resultsDiv.textContent = data.error || "No results found.";
  }
});
