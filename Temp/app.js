const text = `Hi! 😊
So today's a special day for you.

But before we begin, I need you to be fully here.

This journey will take around 15–25 minutes.
Can you stay with me for a while?

If yes... let’s begin.`;

const typewriterElement = document.getElementById('typewriter');
const continueBtn = document.getElementById('continue-btn');
const popupOverlay = document.getElementById('popup-overlay');
const startBtn = document.getElementById('start-btn');

let i = 0;

function typeWriter() {
  if (i < text.length) {
    typewriterElement.textContent += text.charAt(i);
    i++;
    setTimeout(typeWriter, 40);
  } else {
    continueBtn.classList.remove('hidden');
  }
}

startBtn.addEventListener('click', () => {
  popupOverlay.style.display = 'none';
  typeWriter();
});
