document.addEventListener('DOMContentLoaded', () => {
    const cards = document.querySelectorAll('.card');
    let current = 0;
    let intervalId;
    let pause = false;

    function flipTo(index) {
        cards.forEach((c, i) => {
            if (i === index) c.classList.add('flipped');
            else c.classList.remove('flipped');
        });
    }

    function startAutoFlip() {
        intervalId = setInterval(() => {
            if (!pause) {
                flipTo(current);
                current = (current + 1) % cards.length;
            }
        }, 5000);
    }

    // Click to flip any card manually
    cards.forEach((card, index) => {
        card.addEventListener('click', (e) => {
            e.stopPropagation(); // Don’t trigger outside click
            pause = true;
            flipTo(index);

            clearTimeout(pauseTimeout);
            clearInterval(intervalId);

            // Resume after 5 sec
            pauseTimeout = setTimeout(() => {
                pause = false;
                current = (index + 1) % cards.length;
                startAutoFlip();
            }, 5000);
        });
    });

    // Click outside to unflip
    document.addEventListener('click', () => {
        cards.forEach(c => c.classList.remove('flipped'));
    });

    // Start on load
    startAutoFlip();

    let pauseTimeout;
});