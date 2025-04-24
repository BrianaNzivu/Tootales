// static/js/story.js

document.addEventListener('DOMContentLoaded', function() {
    const storyPromptInput = document.getElementById('storyPrompt');
    const generateStoryBtn = document.getElementById('generateStoryBtn');
    const generatedStoryDiv = document.getElementById('generatedStory');

    generateStoryBtn.addEventListener('click', generateStory);

    async function generateStory() {
        const prompt = storyPromptInput.value.trim();
        
        if (!prompt) {
            alert('Please enter a story prompt!');
            return;
        }

        generateStoryBtn.disabled = true;
        generateStoryBtn.innerHTML = 'Generating... <span class="spinner-border spinner-border-sm"></span>';
        generatedStoryDiv.innerHTML = '<div class="alert alert-info">Creating your story... This may take a moment.</div>';

        try {
            console.log("Sending request to generate story with prompt:", prompt);
            
            const response = await fetch('/api/generate-story', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ prompt: prompt })
            });

            console.log("Response status:", response.status);
            
            const contentType = response.headers.get('content-type');
            if (!contentType || !contentType.includes('application/json')) {
                const textResponse = await response.text();
                console.error("Received non-JSON response:", textResponse);
                throw new Error("Expected JSON response but got HTML or other content type");
            }

            const data = await response.json();
            console.log("Response data:", data);
            
            if (response.ok) {

                generatedStoryDiv.innerHTML = `
                    <div class="card mt-4 shadow">
                        <div class="card-header bg-primary text-white">
                            <h3>Your Story</h3>
                        </div>
                        <div class="card-body text-start">
                            <p>${data.story.replace(/\n/g, '<br>')}</p>
                        </div>
                        <div class="card-footer">
                            <button class="btn btn-outline-primary" id="copyButton">
                                <i class="bi bi-clipboard"></i> Copy Story
                            </button>
                        </div>
                    </div>
                `;
                

                document.getElementById('copyButton').addEventListener('click', function() {
                    const storyText = data.story;
                    navigator.clipboard.writeText(storyText)
                        .then(() => {
                            alert('Story copied to clipboard!');
                        })
                        .catch(err => {
                            console.error('Failed to copy: ', err);
                        });
                });
            } else {
                generatedStoryDiv.innerHTML = `<div class="alert alert-danger">Error: ${data.error || 'Failed to generate story'}</div>`;
            }
        } catch (error) {
            console.error('Error generating story:', error);
            generatedStoryDiv.innerHTML = `<div class="alert alert-danger">
                <h4>Something went wrong</h4>
                <p>There was an error generating your story: ${error.message}</p>
                <p>Please try again later or contact support if the problem persists.</p>
            </div>`;
        } finally {

            generateStoryBtn.disabled = false;
            generateStoryBtn.innerHTML = 'Generate Story';
        }
    }
});