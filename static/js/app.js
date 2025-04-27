/**
 * Main application logic for Voice Avatar Chatbot
 */

// Import modules
import { initSpeechRecognition, startSpeechRecognition, stopSpeechRecognition } from './audioProcessor.js';
import { updateAvatarState } from './avatarController.js';
import { testAPI, generateText, textToSpeech } from './apiClient.js';

// Global variables
let conversationHistory = [
    { role: "system", content: "You are a helpful, friendly, and concise AI assistant. Always respond in English in a conversational human-like style. Keep your responses brief and engaging." }
];
let debugMode = false;
window.isProcessingReply = false; // Important flag

// Cache DOM elements
const chatContainer = document.getElementById('chatContainer');
const status = document.getElementById('status');
const micError = document.getElementById('micError');
const debugPanel = document.getElementById('debugPanel');
const debugLog = document.getElementById('debugLog');
const debugTapArea = document.getElementById('debugTapArea');

// ----------------------------------
// Debugging function
export function debug(message, type = 'info') {
    const timestamp = new Date().toLocaleTimeString();
    console.log(`[${timestamp}] [${type}] ${message}`);
    
    if (debugMode) {
        const entry = document.createElement('div');
        entry.className = 'debug-entry';
        entry.innerHTML = `<strong>[${timestamp}] [${type}]:</strong> ${message}`;
        
        if (type === 'error') entry.style.color = '#ff5252';
        else if (type === 'success') entry.style.color = '#69f0ae';
        else if (type === 'warning') entry.style.color = '#ffb74d';
        
        debugLog.appendChild(entry);
        debugPanel.scrollTop = debugPanel.scrollHeight;
    }
}

// ----------------------------------
// Add chat message
export function addMessageToChat(sender, text) {
    debug(`Adding ${sender} message: "${text.substring(0, 30)}..."`, 'info');
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message', sender === 'user' ? 'user-message' : 'bot-message');
    messageDiv.textContent = text;
    chatContainer.appendChild(messageDiv);
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

// ----------------------------------
// Process user input (text from speech)
export async function processUserInput(userText) {
    try {
        debug(`Processing user input: "${userText}"`, 'info');
        window.isProcessingReply = true;

        addMessageToChat('user', userText);
        conversationHistory.push({ role: "user", content: userText });

        status.textContent = 'Thinking...';
        updateAvatarState('thinking');

        const chatResponse = await generateText(conversationHistory);

        if (chatResponse && chatResponse.choices && chatResponse.choices[0]?.message) {
            const botResponse = chatResponse.choices[0].message.content.trim();
            debug(`Bot response: "${botResponse.substring(0, 50)}..."`, 'info');

            addMessageToChat('bot', botResponse);
            conversationHistory.push({ role: "assistant", content: botResponse });

            updateAvatarState('speaking');
            
            // Speak the response
            try {
                await textToSpeech(botResponse);
            } catch (speechError) {
                debug(`Text-to-speech error: ${speechError.message}`, 'error');
                // Continue even if speech fails
            }
            
        } else {
            debug('Invalid AI response.', 'error');
            addMessageToChat('bot', 'Sorry, something went wrong.');
        }
    } catch (error) {
        debug(`Error: ${error.message}`, 'error');
        addMessageToChat('bot', 'Sorry, an error occurred.');
    } finally {
        updateAvatarState('idle');
        status.textContent = 'Waiting for your voice...';
        window.isProcessingReply = false;
        
        // Ensure speech recognition is restarted
        setTimeout(() => {
            startSpeechRecognition();
        }, 1000);
    }
}

// ----------------------------------
// Initialize App
export function initApp() {
    debug('Initializing application...', 'info');

    // Set up double-tap to toggle debug mode
    let lastTapTime = 0;
    debugTapArea.addEventListener('click', () => {
        const now = Date.now();
        if (now - lastTapTime < 300) { // Double-tap
            debugMode = !debugMode;
            debugPanel.classList.toggle('visible');
            debug(`Debug mode ${debugMode ? 'enabled' : 'disabled'}`, 'info');
        }
        lastTapTime = now;
    });

    // Check for microphone support
    if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
        debug('getUserMedia not supported', 'error');
        micError.style.display = 'block';
        micError.textContent = 'Microphone access not supported. Please use a modern browser.';
        return;
    }

    // Check TTS support
    if (!window.speechSynthesis) {
        debug('Speech synthesis not supported', 'warning');
        // Continue anyway, we'll handle this in the API client
    }

    // Request microphone permission
    navigator.mediaDevices.getUserMedia({ audio: true })
        .then(stream => {
            debug('Microphone permission granted', 'success');
            // Stop the stream immediately, we don't need it yet
            stream.getTracks().forEach(track => track.stop());
            
            // Check backend connection
            testAPI()
                .then(success => {
                    if (success) {
                        debug('API test successful', 'success');
                        // Initialize and start speech recognition
                        initSpeechRecognition();
                        startSpeechRecognition();
                    } else {
                        debug('API test returned failure status', 'error');
                        status.textContent = 'Server error. Please check backend.';
                    }
                })
                .catch(error => {
                    debug(`API test failed: ${error.message}`, 'error');
                    status.textContent = 'Server error. Please check backend.';
                });
        })
        .catch(error => {
            debug(`Microphone permission denied: ${error.message}`, 'error');
            micError.style.display = 'block';
            micError.textContent = 'Microphone access denied. Please allow microphone access to use voice features.';
        });

    debug('Initialization complete.', 'success');
}

// DOMContentLoaded
document.addEventListener('DOMContentLoaded', initApp);