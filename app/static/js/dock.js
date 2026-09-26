// dock-proximity.js
// Mimics AnimatedTopDock proximity scaling with spring physics
(function() {
    const nav = document.getElementById('dock-nav');
    if (!nav) return;

    const PROXIMITY = 122;   // px range of influence
    const SPRING    = 0.19;  // spring stiffness
    const DAMPING   = 0.70;  // velocity damping
    const MAX_SCALE = 1.25;  // max scale factor
    const DROP      = 6;     // translateX shift on hover in px

    const items = nav.querySelectorAll('.dock-item');

    // Each item tracks its animated state independently
    const state = Array.from(items).map(() => ({
        currentScale: 1, currentX: 0,
        targetScale: 1,  targetX: 0,
        velScale: 0, velX: 0
    }));

    function getCenter(el) {
        const r = el.getBoundingClientRect();
        return r.top + r.height / 2;
    }

    let mouseY = -9999;

    nav.addEventListener('mousemove', function(e) {
        mouseY = e.clientY;
        updateTargets();
        ensureRunning();
    });

    nav.addEventListener('mouseleave', function() {
        items.forEach((_, i) => {
            state[i].targetScale = 1;
            state[i].targetX = 0;
        });
        ensureRunning();
    });

    function updateTargets() {
        items.forEach((item, i) => {
            const center = getCenter(item);
            const dist = Math.abs(mouseY - center);

            if (dist < PROXIMITY) {
                const factor = 1 - (dist / PROXIMITY);
                const eased = factor * factor;
                state[i].targetScale = 1 + (MAX_SCALE - 1) * eased;
                state[i].targetX = DROP * eased;
            } else {
                state[i].targetScale = 1;
                state[i].targetX = 0;
            }
        });
    }

    let running = false;
    function animate() {
        let needsFrame = false;
        items.forEach((item, i) => {
            const s = state[i];

            s.velScale += SPRING * (s.targetScale - s.currentScale);
            s.velX     += SPRING * (s.targetX - s.currentX);

            s.velScale *= DAMPING;
            s.velX     *= DAMPING;

            s.currentScale += s.velScale;
            s.currentX     += s.velX;

            item.style.transform = 'scale(' + s.currentScale.toFixed(4) + ') translateX(' + s.currentX.toFixed(2) + 'px)';

            if (Math.abs(s.velScale) > 0.0001 || Math.abs(s.velX) > 0.001 ||
                Math.abs(s.targetScale - s.currentScale) > 0.001 || Math.abs(s.targetX - s.currentX) > 0.1) {
                needsFrame = true;
            }
        });

        if (needsFrame) {
            requestAnimationFrame(animate);
        } else {
            running = false;
        }
    }

    function ensureRunning() {
        if (!running) {
            running = true;
            requestAnimationFrame(animate);
        }
    }
})();
