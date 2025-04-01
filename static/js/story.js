document.addEventListener('DOMContentLoaded', function() {
    const generateStoryBtn = document.getElementById('generateStoryBtn');
    const startInteractiveStoryBtn = document.getElementById('startInteractiveStory');
    const generatedStoryDiv = document.getElementById('generatedStory');
    const interactiveStoryDiv = document.getElementById('interactiveStoryContainer');
  
    // Generate Story Functionality
    generateStoryBtn.addEventListener('click', async function() {
      const storyPrompt = document.getElementById('storyPrompt').value.trim();
      if (!storyPrompt) {
        alert('Please enter a story idea!');
        return;
      }
      try {
        const response = await fetch('/generate_story_api', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ prompt: storyPrompt })
        });
        const data = await response.json();
        generatedStoryDiv.innerHTML = `<h3>Your Generated Story:</h3><p>${data.story}</p>`;
      } catch (err) {
        console.error("Error generating story:", err);
        generatedStoryDiv.innerHTML = `<p class="text-danger">An error occurred while generating your story.</p>`;
      }
    });
  
    // Interactive Story Functionality
    startInteractiveStoryBtn.addEventListener('click', function() {
      interactiveStoryDiv.innerHTML = `
        <p>Once upon a time, in a magical land, you find yourself at a crossroads...</p>
        <button onclick="continueStory('left')" class="btn btn-warning mt-2">Go Left</button>
        <button onclick="continueStory('right')" class="btn btn-danger mt-2">Go Right</button>
      `;
    });
  });
  
  function continueStory(choice) {
    if (choice === 'left') {
      document.getElementById('interactiveStoryContainer').innerHTML = `<p>You went left and discovered a secret garden full of wonder!</p>`;
    } else {
      document.getElementById('interactiveStoryContainer').innerHTML = `<p>You went right and encountered a friendly dragon on a quest for treasure!</p>`;
    }
  }
  