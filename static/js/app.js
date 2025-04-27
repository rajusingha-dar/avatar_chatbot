// /**
//  * Main application logic for Voice Avatar Chatbot
//  */

// // Import modules
// import { initSpeechRecognition, startSpeechRecognition, stopSpeechRecognition } from './audioProcessor.js';
// import { updateAvatarState } from './avatarController.js';
// import { testAPI, generateText, textToSpeech } from './apiClient.js';

// // Global variables
// let conversationHistory = [
//     { role: "system", content: "You are a helpful, friendly, and concise AI assistant. Always respond in English in a conversational human-like style. Keep your responses brief and engaging." }
// ];
// let debugMode = false;
// window.isProcessingReply = false; // Important flag

// // Cache DOM elements
// const chatContainer = document.getElementById('chatContainer');
// const status = document.getElementById('status');
// const micError = document.getElementById('micError');
// const debugPanel = document.getElementById('debugPanel');
// const debugLog = document.getElementById('debugLog');
// const debugTapArea = document.getElementById('debugTapArea');

// // ----------------------------------
// // Debugging function
// export function debug(message, type = 'info') {
//     const timestamp = new Date().toLocaleTimeString();
//     console.log(`[${timestamp}] [${type}] ${message}`);
    
//     if (debugMode) {
//         const entry = document.createElement('div');
//         entry.className = 'debug-entry';
//         entry.innerHTML = `<strong>[${timestamp}] [${type}]:</strong> ${message}`;
        
//         if (type === 'error') entry.style.color = '#ff5252';
//         else if (type === 'success') entry.style.color = '#69f0ae';
//         else if (type === 'warning') entry.style.color = '#ffb74d';
        
//         debugLog.appendChild(entry);
//         debugPanel.scrollTop = debugPanel.scrollHeight;
//     }
// }

// // ----------------------------------
// // Add chat message
// export function addMessageToChat(sender, text) {
//     debug(`Adding ${sender} message: "${text.substring(0, 30)}..."`, 'info');
//     const messageDiv = document.createElement('div');
//     messageDiv.classList.add('message', sender === 'user' ? 'user-message' : 'bot-message');
//     messageDiv.textContent = text;
//     chatContainer.appendChild(messageDiv);
//     chatContainer.scrollTop = chatContainer.scrollHeight;
// }

// // ----------------------------------
// // Process user input (text from speech)
// export async function processUserInput(userText) {
//     try {
//         debug(`Processing user input: "${userText}"`, 'info');
//         window.isProcessingReply = true;

//         addMessageToChat('user', userText);
//         conversationHistory.push({ role: "user", content: userText });

//         status.textContent = 'Thinking...';
//         updateAvatarState('thinking');

//         const chatResponse = await generateText(conversationHistory);

//         if (chatResponse && chatResponse.choices && chatResponse.choices[0]?.message) {
//             const botResponse = chatResponse.choices[0].message.content.trim();
//             debug(`Bot response: "${botResponse.substring(0, 50)}..."`, 'info');

//             addMessageToChat('bot', botResponse);
//             conversationHistory.push({ role: "assistant", content: botResponse });

//             updateAvatarState('speaking');
            
//             // Speak the response
//             try {
//                 await textToSpeech(botResponse);
//             } catch (speechError) {
//                 debug(`Text-to-speech error: ${speechError.message}`, 'error');
//                 // Continue even if speech fails
//             }
            
//         } else {
//             debug('Invalid AI response.', 'error');
//             addMessageToChat('bot', 'Sorry, something went wrong.');
//         }
//     } catch (error) {
//         debug(`Error: ${error.message}`, 'error');
//         addMessageToChat('bot', 'Sorry, an error occurred.');
//     } finally {
//         updateAvatarState('idle');
//         status.textContent = 'Waiting for your voice...';
//         window.isProcessingReply = false;
        
//         // Ensure speech recognition is restarted
//         setTimeout(() => {
//             startSpeechRecognition();
//         }, 1000);
//     }
// }

// // ----------------------------------
// // Initialize App
// export function initApp() {
//     debug('Initializing application...', 'info');

//     // Set up double-tap to toggle debug mode
//     let lastTapTime = 0;
//     debugTapArea.addEventListener('click', () => {
//         const now = Date.now();
//         if (now - lastTapTime < 300) { // Double-tap
//             debugMode = !debugMode;
//             debugPanel.classList.toggle('visible');
//             debug(`Debug mode ${debugMode ? 'enabled' : 'disabled'}`, 'info');
//         }
//         lastTapTime = now;
//     });

//     // Check for microphone support
//     if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
//         debug('getUserMedia not supported', 'error');
//         micError.style.display = 'block';
//         micError.textContent = 'Microphone access not supported. Please use a modern browser.';
//         return;
//     }

//     // Check TTS support
//     if (!window.speechSynthesis) {
//         debug('Speech synthesis not supported', 'warning');
//         // Continue anyway, we'll handle this in the API client
//     }

//     // Request microphone permission
//     navigator.mediaDevices.getUserMedia({ audio: true })
//         .then(stream => {
//             debug('Microphone permission granted', 'success');
//             // Stop the stream immediately, we don't need it yet
//             stream.getTracks().forEach(track => track.stop());
            
//             // Check backend connection
//             testAPI()
//                 .then(success => {
//                     if (success) {
//                         debug('API test successful', 'success');
//                         // Initialize and start speech recognition
//                         initSpeechRecognition();
//                         startSpeechRecognition();
//                     } else {
//                         debug('API test returned failure status', 'error');
//                         status.textContent = 'Server error. Please check backend.';
//                     }
//                 })
//                 .catch(error => {
//                     debug(`API test failed: ${error.message}`, 'error');
//                     status.textContent = 'Server error. Please check backend.';
//                 });
//         })
//         .catch(error => {
//             debug(`Microphone permission denied: ${error.message}`, 'error');
//             micError.style.display = 'block';
//             micError.textContent = 'Microphone access denied. Please allow microphone access to use voice features.';
//         });

//     debug('Initialization complete.', 'success');
// }

// // DOMContentLoaded
// document.addEventListener('DOMContentLoaded', initApp);

// app.js - Main application logic for Voice Avatar Chatbot

// Application state
const appState = {
    isListening: false,
    isProcessingReply: false,
    avatarState: 'idle', // idle, listening, thinking, speaking
    messages: []
};

// DOM elements
let avatarElement;
let avatarStatusElement;
let messagesContainer;
let stopButtonElement;

// Initialize the application
async function initApp() {
    try {
        log('info', 'Initializing application...');
        
        // Get DOM elements
        avatarElement = document.getElementById('avatar');
        avatarStatusElement = document.getElementById('avatar-status');
        messagesContainer = document.getElementById('chat-messages');
        stopButtonElement = document.getElementById('stopButton');
        
        // Initialize components
        await initSpeechSynthesis();
        await initAPI();
        await initSpeechRecognition();
        
        // Initialize the stop button
        initStopButton();
        
        // Initialize speech event listeners
        initSpeechEvents();
        
        log('success', 'Initialization complete.');
        
        // Start with the avatar in listening mode
        setAvatarState('listening');
        startSpeechRecognition();
    } catch (error) {
        log('error', `Initialization failed: ${error.message}`);
    }
}

// Initialize the API connection
async function initAPI() {
    try {
        const isConnected = await testAPI();
        if (isConnected) {
            log('success', 'API test successful');
        } else {
            log('error', 'API test failed');
        }
    } catch (error) {
        log('error', `API initialization error: ${error.message}`);
    }
}

// Initialize the speech recognition
async function initSpeechRecognition() {
    try {
        const isInitialized = await setupSpeechRecognition(handleUserSpeech);
        if (isInitialized) {
            log('success', 'Speech recognition initialized.');
        } else {
            log('error', 'Failed to initialize speech recognition');
        }
    } catch (error) {
        log('error', `Speech recognition error: ${error.message}`);
    }
}

// Initialize the stop button functionality
function initStopButton() {
    if (stopButtonElement) {
        stopButtonElement.addEventListener('click', () => {
            log('success', 'Stop button clicked');
            
            // Stop the current speech
            if (typeof stopSpeech === 'function') {
                stopSpeech();
            }
        });
        
        // Initially disable the button
        stopButtonElement.disabled = true;
    } else {
        log('error', 'Stop button not found in the DOM');
    }
}

// Initialize speech event listeners
function initSpeechEvents() {
    // Listen for speech started event
    document.addEventListener('speechStarted', () => {
        log('info', 'Avatar state changed to: speaking');
        setAvatarState('speaking');
    });
    
    // Listen for speech ended event
    document.addEventListener('speechEnded', () => {
        log('info', 'Avatar state changed to: idle');
        setAvatarState('idle');
        
        // Start listening again after speech ends
        startSpeechRecognition();
    });
    
    // Listen for speech manually stopped event
    document.addEventListener('speechStopped', () => {
        log('info', 'Speech manually stopped');
        log('info', 'Avatar state changed to: idle');
        setAvatarState('idle');
        
        // Start listening immediately after speech is stopped
        startSpeechRecognition();
    });
}

// Handle user speech input
function handleUserSpeech(text) {
    if (!text || text.trim() === '') {
        return;
    }
    
    log('info', `User said: "${text}"`);
    
    // Stop listening while processing
    stopSpeechRecognition();
    
    // Process the user input
    processUserInput(text);
}

// Process user input and get AI response
async function processUserInput(text) {
    try {
        log('info', `Processing user input: "${text}"`);
        
        // Set avatar state to thinking
        setAvatarState('thinking');
        
        // Add user message to the state and UI
        addUserMessage(text);
        
        // Set the processing flag
        appState.isProcessingReply = true;
        
        // Prepare messages array for the API
        const messages = [
            {
                role: 'system',
                content: 'You are a helpful, friendly, and intelligent AI assistant. Always respond in English. Be polite, conversational, and informative.'
            },
            ...appState.messages
        ];
        
        // Get bot response
        const botResponse = await sendMessage(messages);
        log('info', `Bot response: "${botResponse.substring(0, 30)}..."`);
        
        // Process the response
        await processBotResponse(botResponse);
        
    } catch (error) {
        log('error', `Error processing input: ${error.message}`);
        
        // Add a fallback message
        addBotMessage("I'm sorry, I couldn't process your request. Please try again.");
        
        // Reset state
        setAvatarState('idle');
        appState.isProcessingReply = false;
        
        // Start listening again
        startSpeechRecognition();
    }
}

// Process the bot's response
async function processBotResponse(response) {
    try {
        // Add the bot message to UI and state
        addBotMessage(response);
        
        // Set avatar to speaking state
        setAvatarState('speaking');
        
        // Enable the stop button before starting speech
        if (stopButtonElement) {
            stopButtonElement.disabled = false;
        }
        
        // Speak the response
        await textToSpeech(response);
        
        // Note: We don't need to set avatar to idle or start listening here
        // as that's now handled by the speech event listeners
        
    } catch (error) {
        log('error', `Error processing bot response: ${error.message}`);
        
        // Set avatar back to idle state
        setAvatarState('idle');
        
        // Start listening again even if there was an error
        startSpeechRecognition();
    } finally {
        // Reset processing flag
        appState.isProcessingReply = false;
    }
}

// Add a user message to the state and UI
function addUserMessage(text) {
    // Add to state
    appState.messages.push({
        role: 'user',
        content: text
    });
    
    // Add to UI
    const messageElement = document.createElement('div');
    messageElement.className = 'message user';
    messageElement.innerHTML = `<div class="message-content">${text}</div>`;
    messagesContainer.appendChild(messageElement);
    
    // Scroll to the bottom
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
    
    log('info', `Adding user message: "${text.substring(0, 30)}..."`);
}

// Add a bot message to the state and UI
function addBotMessage(text) {
    // Add to state
    appState.messages.push({
        role: 'assistant',
        content: text
    });
    
    // Add to UI
    const messageElement = document.createElement('div');
    messageElement.className = 'message assistant';
    messageElement.innerHTML = `<div class="message-content">${text}</div>`;
    messagesContainer.appendChild(messageElement);
    
    // Scroll to the bottom
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
    
    log('info', `Adding bot message: "${text.substring(0, 30)}..."`);
}

// Start speech recognition
function startSpeechRecognition() {
    if (appState.isProcessingReply) {
        log('info', 'Not starting recognition - processing reply');
        return;
    }
    
    if (appState.isListening) {
        log('warning', 'Already listening');
        return;
    }
    
    // Start recognition
    startRecognition().then(success => {
        if (success) {
            log('success', 'Speech recognition started.');
            appState.isListening = true;
            setAvatarState('listening');
        } else {
            log('error', 'Failed to start speech recognition');
            setAvatarState('idle');
        }
    });
}

// Stop speech recognition
function stopSpeechRecognition() {
    if (!appState.isListening) {
        return;
    }
    
    log('info', 'Stopping recognition');
    stopRecognition();
    appState.isListening = false;
}

// Set the avatar state
function setAvatarState(state) {
    // Valid states: idle, listening, thinking, speaking
    if (appState.avatarState === state) {
        return;
    }
    
    appState.avatarState = state;
    log('info', `Avatar state changed to: ${state}`);
    
    // Update the avatar UI
    updateAvatarUI(state);
}

// Update the avatar UI based on the state
function updateAvatarUI(state) {
    if (!avatarElement || !avatarStatusElement) {
        return;
    }
    
    // Remove all state classes
    avatarElement.classList.remove('idle', 'listening', 'thinking', 'speaking');
    
    // Add the current state class
    avatarElement.classList.add(state);
    
    // Update the status text
    let statusText = 'Idle';
    
    switch (state) {
        case 'listening':
            statusText = 'Listening...';
            break;
        case 'thinking':
            statusText = 'Thinking...';
            break;
        case 'speaking':
            statusText = 'Speaking...';
            break;
    }
    
    avatarStatusElement.textContent = statusText;
}

// Log messages with type and timestamp
function log(type, message) {
    const timestamp = new Date().toLocaleTimeString();
    console[type === 'error' ? 'error' : type === 'warning' ? 'warn' : 'log'](`[${timestamp}] [${type}] ${message}`);
}

// Initialize when the page is loaded
document.addEventListener('DOMContentLoaded', initApp);