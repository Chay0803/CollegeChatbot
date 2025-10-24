document.getElementById("employee-form").addEventListener("submit", async (e) => {
  e.preventDefault();
  const formData = new FormData(e.target);
  const resultsDiv = document.getElementById("employee-results");

  resultsDiv.innerHTML = "⏳ Searching employee data...";

  try {
    const response = await fetch("/employees/search", {
      method: "POST",
      body: formData,
    });

    const data = await response.json();
    resultsDiv.innerHTML = "";

    if (data.error) {
      resultsDiv.innerHTML = `<p style="color:red;">⚠️ ${data.error}</p>`;
      return;
    }

    if (!data.results || data.results.length === 0) {
      resultsDiv.innerHTML = "<p style='color:red;'>No data found.</p>";
      return;
    }

    // Build a clean table for results
    const table = document.createElement("table");
    table.classList.add("results-table");

    // Table header
    const headers = Object.keys(data.results[0]);
    const thead = document.createElement("thead");
    const headerRow = document.createElement("tr");
    headers.forEach((key) => {
      const th = document.createElement("th");
      th.textContent = key;
      headerRow.appendChild(th);
    });
    thead.appendChild(headerRow);
    table.appendChild(thead);

    // Table body
    const tbody = document.createElement("tbody");
    data.results.forEach((row) => {
      const tr = document.createElement("tr");
      headers.forEach((key) => {
        const td = document.createElement("td");
        td.textContent = row[key];
        tr.appendChild(td);
      });
      tbody.appendChild(tr);
    });
    table.appendChild(tbody);

    resultsDiv.appendChild(table);

  } catch (err) {
    console.error(err);
    resultsDiv.innerHTML = "⚠️ Error fetching employee data.";
  }
});
