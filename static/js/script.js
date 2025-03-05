document.addEventListener('DOMContentLoaded', function() {
    // Dark Mode Toggle
    const darkModeToggle = document.getElementById('darkModeToggle');
    if (localStorage.getItem('darkMode') === 'true') {
      darkModeToggle.checked = true;
      document.body.classList.add('dark-mode');
    }
    darkModeToggle.addEventListener('change', function() {
      if (this.checked) {
        document.body.classList.add('dark-mode');
        localStorage.setItem('darkMode', 'true');
      } else {
        document.body.classList.remove('dark-mode');
        localStorage.setItem('darkMode', 'false');
      }
    });
  
    // Text-to-Speech for Listen Tab
    const playAudioButton = document.getElementById('playAudio');
    if (playAudioButton) {
      playAudioButton.addEventListener('click', function() {
        // For demonstration, we use a sample text.
        // In a real application, you would pass the full text of the book.
        const sampleText = "This is a sample text for the audio reading of the book. In the final version, the complete text would be read aloud.";
        speakText(sampleText);
      });
    }
  });
  
  function speakText(text) {
    // Check if browser supports speech synthesis
    if ('speechSynthesis' in window) {
      const utterance = new SpeechSynthesisUtterance(text);
      // Optionally, set voice, pitch, and rate
      utterance.voice = speechSynthesis.getVoices()[0];
      utterance.pitch = 1;
      utterance.rate = 1;
      window.speechSynthesis.speak(utterance);
    } else {
      alert("Sorry, your browser does not support text-to-speech.");
    }
  }
  