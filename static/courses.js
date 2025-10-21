const courseForm = document.getElementById("course-form");
const courseResults = document.getElementById("course-results");

courseForm.addEventListener("submit", async (e) => {
  e.preventDefault();

  courseResults.innerHTML = "<p><em>Generating recommendations...</em></p>";

  const formData = new FormData(courseForm);

  try {
    const res = await fetch("/recommend", { method: "POST", body: formData });
    const data = await res.json();

    if (data.recommendations && data.recommendations.length > 0) {
      courseResults.innerHTML = `
        <h3>Recommended Courses:</h3>
        <ul>
          ${data.recommendations.map(c => `<li>${c}</li>`).join("")}
        </ul>
      `;
    } else {
      courseResults.innerHTML = "<p>No matching courses found.</p>";
    }
  } catch (err) {
    courseResults.innerHTML = "<p>⚠️ Error fetching recommendations.</p>";
    console.error(err);
  }
});
