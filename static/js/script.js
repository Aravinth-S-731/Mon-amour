const popupOverlay = document.getElementById('popup-overlay');
const codePopupOverlay = document.getElementById('code-popup-overlay');
const continueBtn = document.getElementById('continue-btn');
const startBtn = document.getElementById('start-btn');
const typewriterElement = document.getElementById('typewriter');
const text = `Hi! 😊
So today's a special day for you.

But before we begin, I need you to be fully here.

This journey will take around 15 minutes.
Can you stay with me for a while?

If yes... let’s begin.`;

let i = 0;

function typeWriter() {
  if (i < text.length) {
    typewriterElement.textContent += text.charAt(i);
    i++;
    setTimeout(typeWriter, 60);
  } else {
    continueBtn.classList.remove('hidden');
  }
}

startBtn.addEventListener('click', () => {
  popupOverlay.style.display = 'none';
  typeWriter();
});

continueBtn.addEventListener('click', () => {
  // Hide intro container and continue button
  document.querySelector('.intro-container').style.display = 'none';

  // Show second popup form for code entry
  codePopupOverlay.classList.remove('hidden');
});
