// avatarController.js - Controls the avatar animations and states

// Avatar animation properties
const avatarAnimations = {
    idle: {
        frames: 1,
        fps: 1
    },
    listening: {
        frames: 3,
        fps: 2
    },
    thinking: {
        frames: 2,
        fps: 1
    },
    speaking: {
        frames: 4,
        fps: 3
    }
};

// Current animation
let currentAnimation = null;
let animationInterval = null;
let currentFrame = 0;

// Start animating the avatar based on state
function startAvatarAnimation(state) {
    // Stop any existing animation
    stopAvatarAnimation();
    
    // Get animation properties
    const animation = avatarAnimations[state];
    if (!animation) {
        console.error(`Unknown animation state: ${state}`);
        return;
    }
    
    // Set current animation
    currentAnimation = state;
    currentFrame = 0;
    
    // Start the animation interval
    if (animation.frames > 1) {
        const frameTime = 1000 / animation.fps;
        animationInterval = setInterval(() => {
            currentFrame = (currentFrame + 1) % animation.frames;
            updateAvatarFrame();
        }, frameTime);
    }
    
    // Set initial frame
    updateAvatarFrame();
}

// Stop the avatar animation
function stopAvatarAnimation() {
    if (animationInterval) {
        clearInterval(animationInterval);
        animationInterval = null;
    }
    currentAnimation = null;
}

// Update the avatar frame
function updateAvatarFrame() {
    const avatarElement = document.getElementById('avatar');
    if (!avatarElement || !currentAnimation) {
        return;
    }
    
    // For now, we're just using CSS classes for animation
    // In the future, this could update actual images or 3D models
}

// Export functions to the global scope
window.startAvatarAnimation = startAvatarAnimation;
window.stopAvatarAnimation = stopAvatarAnimation;