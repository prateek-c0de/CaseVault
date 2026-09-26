// vanilla-warp.js
// Equivalent to WarpFieldBackground without React dependencies

(function() {
    // Create canvas
    const canvas = document.createElement('canvas');
    canvas.id = 'warp-bg';
    canvas.style.position = 'fixed';
    canvas.style.top = '0';
    canvas.style.left = '0';
    canvas.style.width = '100vw';
    canvas.style.height = '100vh';
    canvas.style.zIndex = '-1';
    canvas.style.pointerEvents = 'none';
    
    // Check if we are inside the authenticated layout so it doesn't break login page readability
    // Or just append it globally. Let's append it globally but adjust opacity.
    document.body.insertBefore(canvas, document.body.firstChild);

    const ctx = canvas.getContext('2d');
    let width, height;
    let stars = [];
    const numStars = 400;
    
    // User configuration
    const speed = 15.0;
    const streakOpacity = 0.60;
    const tileOpacity = 0.90; // Background dimming
    const hue = 0;
    const saturation = 1.0;
    const brightness = 1.0;

    function resize() {
        width = window.innerWidth;
        height = window.innerHeight;
        canvas.width = width;
        canvas.height = height;
    }
    window.addEventListener('resize', resize);
    resize();

    class Star {
        constructor() {
            this.x = (Math.random() - 0.5) * width;
            this.y = (Math.random() - 0.5) * height;
            this.z = Math.random() * width;
            this.pz = this.z;
        }
        update() {
            this.z -= speed;
            if (this.z < 1) {
                this.z = width;
                this.x = (Math.random() - 0.5) * width;
                this.y = (Math.random() - 0.5) * height;
                this.pz = this.z;
            }
        }
        draw() {
            let sx = (this.x / this.z) * width + width / 2;
            let sy = (this.y / this.z) * height + height / 2;
            let px = (this.x / this.pz) * width + width / 2;
            let py = (this.y / this.pz) * height + height / 2;
            this.pz = this.z;

            ctx.beginPath();
            ctx.moveTo(px, py);
            ctx.lineTo(sx, sy);
            
            // Generate color based on HSB/HSL logic.
            // HSB(0, 100%, 100%) is red. 
            // In CSS, HSL(0, 100%, 50%) is equivalent to HSB(0, 100%, 100%).
            // Let's use standard whiteish streaks but tinted with the hue if desired.
            // To make it look like a warp field, we'll keep the streaks bright.
            let hueDeg = hue * 360;
            ctx.strokeStyle = `hsla(${hueDeg}, ${saturation * 100}%, 60%, ${streakOpacity})`;
            ctx.lineWidth = Math.max(1, (width - this.z) / 200);
            ctx.stroke();
        }
    }
    
    for(let i=0; i<numStars; i++) stars.push(new Star());

    function animate() {
        // Base dark background with tileOpacity
        ctx.fillStyle = `rgba(2, 6, 23, ${tileOpacity})`; 
        ctx.fillRect(0, 0, width, height);
        
        stars.forEach(s => {
            s.update();
            s.draw();
        });
        requestAnimationFrame(animate);
    }
    animate();
})();
