/**
 * Avatar visualization and animations
 */

import { debug } from './app.js';

// DOM elements
const avatarContainer = document.getElementById('avatar-container');
const avatarState = avatarContainer.querySelector('.avatar-state');
const visualizer = document.getElementById('audioVisualizer');
const visualizerBars = document.querySelectorAll('.visualizer-bar');

let visualizerInterval;

/**
 * Start visualizer animation (random bars)
 */
export function startVisualizer() {
    stopVisualizer(); // clear previous
    visualizer.style.display = 'flex';
    visualizerInterval = setInterval(() => {
        visualizerBars.forEach(bar => {
            bar.style.height = `${Math.random() * 40 + 5}px`;
        });
    }, 100);
}

/**
 * Stop visualizer animation
 */
export function stopVisualizer() {
    if (visualizerInterval) {
        clearInterval(visualizerInterval);
        visualizerInterval = null;
    }
    visualizer.style.display = 'none';
    visualizerBars.forEach(bar => {
        bar.style.height = '10px';
    });
}

/**
 * Update avatar state with color/animation
 */
export function updateAvatarState(state) {
    avatarContainer.className = 'idle'; // Reset class
    avatarContainer.classList.remove('idle', 'listening', 'thinking', 'speaking');

    if (state === 'listening') {
        avatarContainer.classList.add('listening');
        avatarState.textContent = 'Listening...';
    } else if (state === 'thinking') {
        avatarContainer.classList.add('thinking');
        avatarState.textContent = 'Thinking...';
    } else if (state === 'speaking') {
        avatarContainer.classList.add('speaking');
        avatarState.textContent = 'Speaking...';
    } else {
        avatarContainer.classList.add('idle');
        avatarState.textContent = 'Waiting for your voice...';
    }

    debug(`Avatar state changed to: ${state}`, 'info');
}
