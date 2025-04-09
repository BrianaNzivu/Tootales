document.getElementById("generateStoryBtn").addEventListener("click", () => {
  const prompt = document.getElementById("storyPrompt").value;
  const ageGroup = document.getElementById("ageGroup").value;

  fetch("/generate_story", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ prompt, age_group: ageGroup })
  })
  .then(res => res.json())
  .then(data => {
    document.getElementById("generatedStory").innerHTML = `
      <div class="card p-3 shadow-sm">
        <h4>Your Generated Story:</h4>
        <p style="white-space: pre-wrap;">${data.story}</p>
      </div>
    `;
  });
});
