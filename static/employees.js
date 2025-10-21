const employeeForm = document.getElementById("employee-form");
const employeeResults = document.getElementById("employee-results");

employeeForm.addEventListener("submit", async (e) => {
  e.preventDefault();

  employeeResults.innerHTML = "<p><em>Searching...</em></p>";

  const formData = new FormData(employeeForm);

  try {
    const res = await fetch("/employees/search", { method: "POST", body: formData });
    const data = await res.json();

    if (data.results && data.results.length > 0) {
      const headers = Object.keys(data.results[0]);
      const rows = data.results
        .map(row =>
          `<tr>${headers.map(h => `<td>${row[h] ?? ""}</td>`).join("")}</tr>`
        )
        .join("");

      employeeResults.innerHTML = `
        <table class="results-table">
          <thead>
            <tr>${headers.map(h => `<th>${h}</th>`).join("")}</tr>
          </thead>
          <tbody>${rows}</tbody>
        </table>
      `;
    } else {
      employeeResults.innerHTML = `<p>${data.error || "No results found."}</p>`;
    }
  } catch (err) {
    employeeResults.innerHTML = "<p>⚠️ Error fetching employee details.</p>";
    console.error(err);
  }
});
