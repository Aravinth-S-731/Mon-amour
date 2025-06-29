document.addEventListener("DOMContentLoaded", () => {
    const puzzleContainer = document.getElementById("puzzle-container");
    const hintOverlay = document.getElementById("hint-overlay");
    const hintBtn = document.getElementById("hint-btn");
    const dropSound = new Audio("/static/audio/drag-drop.mp3");

    const gridSize = 3;
    const imageSize = 300;
    const tileSize = imageSize / gridSize;

    let dragged = null;
    let touchStartIndex = null;

    // 🔒 Prevent page scroll/refresh while dragging on mobile
    document.addEventListener("touchmove", function (e) {
        if (e.target.closest(".tile")) {
            e.preventDefault();
        }
    }, { passive: false });

    // 🧩 Create tiles in correct order first
    const totalTiles = gridSize * gridSize;
    const tileElements = [];

    for (let i = 0; i < totalTiles; i++) {
        const tile = document.createElement("div");
        tile.className = "tile";
        tile.style.backgroundImage = "url('/static/images/puzzle-image.jpg')";
        tile.style.backgroundSize = `${imageSize}px ${imageSize}px`;
        tile.style.backgroundPosition = `-${(i % gridSize) * tileSize}px -${Math.floor(i / gridSize) * tileSize}px`;
        tile.dataset.order = i;

        // Optional fade-in animation
        tile.style.animation = `fadeIn 0.3s ease ${(i * 60)}ms forwards`;
        tile.style.opacity = 0;

        tileElements.push(tile);
    }

    shuffle(tileElements);
    tileElements.forEach(tile => puzzleContainer.appendChild(tile));
    bindEvents();

    function shuffle(array) {
        for (let i = array.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [array[i], array[j]] = [array[j], array[i]];
        }
    }

    function bindEvents() {
        let tiles = Array.from(document.querySelectorAll('.tile'));

        tiles.forEach((tile) => {
            tile.draggable = true;

            tile.addEventListener("dragstart", () => {
                dragged = tile;
                tile.classList.add("dragging");
            });

            tile.addEventListener("dragover", (e) => e.preventDefault());

            tile.addEventListener("drop", () => {
                if (dragged && dragged !== tile) {
                    swapTiles(dragged, tile);
                    dropSound.play();
                    checkCompletion();
                }
            });

            tile.addEventListener("dragend", () => {
                tile.classList.remove("dragging");
            });

            // Mobile touch support
            tile.addEventListener("touchstart", () => {
                touchStartIndex = tiles.indexOf(tile);
            });

            tile.addEventListener("touchend", (e) => {
                const touch = e.changedTouches[0];
                const target = document.elementFromPoint(touch.clientX, touch.clientY);
                if (target && target.classList.contains("tile")) {
                    const endIndex = tiles.indexOf(target);
                    if (touchStartIndex !== null && endIndex !== -1 && endIndex !== touchStartIndex) {
                        swapTiles(tiles[touchStartIndex], tiles[endIndex]);
                        dropSound.play();
                        checkCompletion();
                    }
                }
            });
        });
    }

    function swapTiles(tile1, tile2) {
        const clone1 = tile1.cloneNode(true);
        const clone2 = tile2.cloneNode(true);

        tile1.replaceWith(clone2);
        tile2.replaceWith(clone1);

        bindEvents(); // Rebind events to all tiles
    }

    function checkCompletion() {
        const currentOrder = Array.from(document.querySelectorAll('.tile')).map(tile => parseInt(tile.dataset.order));
        const correctOrder = [...currentOrder].slice().sort((a, b) => a - b);

        if (currentOrder.join() === correctOrder.join()) {
            showSuccessPopup();
        }
    }

    function showSuccessPopup() {
        const popup = document.createElement("div");
        popup.className = "popup";
        popup.style.display = "flex"; // ← add this line
        popup.innerHTML = `
            <div class="popup-content">
                <h2>🎉 You did it!</h2>
                <p>Just like Life 💖 — the final piece clicked into place 💜</p>
            </div>
        `;
        document.body.appendChild(popup);

        setTimeout(() => {
            document.body.classList.add("fade-out");
            setTimeout(() => {
                window.location.href = "/gallery";
            }, 1000);
        }, 2500);
    }

    hintBtn.addEventListener("click", () => {
        hintOverlay.classList.toggle("visible");
    });
});