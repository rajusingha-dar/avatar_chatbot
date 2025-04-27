// /**
//  * Smart Auto-Listening Audio Processor using Web Speech API
//  */

// import { debug, processUserInput } from './app.js';
// import { updateAvatarState, startVisualizer, stopVisualizer } from './avatarController.js';

// // Global variables
// let recognition = null;
// let isListening = false;
// let restartTimer = null;
// let silenceTimer = null;
// const SILENCE_TIMEOUT = 5000; // 5 seconds of silence triggers processing
// const RESTART_DELAY = 1000; // 1 second delay before restarting recognition

// /**
//  * Initialize speech recognition
//  */
// export function initSpeechRecognition() {
//     try {
//         const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

//         if (!SpeechRecognition) {
//             debug('Web Speech API is not supported in this browser.', 'error');
//             return;
//         }

//         // Create new recognition instance
//         recognition = new SpeechRecognition();
//         recognition.lang = 'en-US';
//         recognition.continuous = false; // Changed to false to avoid overlapping sessions
//         recognition.interimResults = true;
//         recognition.maxAlternatives = 1;

//         // Event: Start listening
//         recognition.onstart = () => {
//             debug('Speech recognition started.', 'success');
//             isListening = true;
//             updateAvatarState('listening');
//             startVisualizer();
//             resetSilenceTimer();
//         };

//         // Event: User spoke (interim results)
//         recognition.onresult = (event) => {
//             // Reset silence timer when user speaks
//             resetSilenceTimer();
            
//             const lastResult = event.results[event.results.length - 1];
            
//             // Only process final results (not interim)
//             if (lastResult.isFinal) {
//                 const transcript = lastResult[0].transcript.trim();
                
//                 if (transcript) {
//                     debug(`User said: "${transcript}"`, 'info');
//                     processSpeech(transcript);
//                 }
//             }
//         };

//         // Event: Speech recognition ended
//         recognition.onend = () => {
//             debug('Speech recognition ended.', 'warning');
//             isListening = false;
//             stopVisualizer();
            
//             // Clear any pending timers
//             clearTimeout(restartTimer);
//             clearTimeout(silenceTimer);

//             // Auto-restart if not processing a reply
//             if (!window.isProcessingReply) {
//                 debug('Auto-restarting recognition...', 'info');
//                 restartTimer = setTimeout(() => {
//                     startSpeechRecognition();
//                 }, RESTART_DELAY);
//             } else {
//                 debug('Not restarting recognition - processing reply', 'info');
//             }
//         };

//         // Event: Error
//         recognition.onerror = (event) => {
//             debug(`Speech recognition error: ${event.error}`, 'error');
            
//             // Only react to critical errors
//             if (event.error === 'not-allowed' || event.error === 'service-not-allowed') {
//                 updateAvatarState('idle');
//                 stopVisualizer();
//             } else if (event.error === 'aborted') {
//                 // This is normal when we stop it ourselves
//                 debug('Recognition aborted - this is normal during processing', 'info');
//             } else if (event.error === 'no-speech') {
//                 // No speech detected - restart
//                 debug('No speech detected - restarting', 'info');
//             } else {
//                 // For other errors, just restart
//                 debug(`Unexpected error: ${event.error} - restarting`, 'error');
//             }
            
//             // For non-critical errors, restart
//             if (event.error !== 'not-allowed' && event.error !== 'service-not-allowed') {
//                 restartTimer = setTimeout(() => {
//                     if (!window.isProcessingReply) {
//                         startSpeechRecognition();
//                     }
//                 }, RESTART_DELAY);
//             }
//         };

//         debug('Speech recognition initialized.', 'success');
//     } catch (error) {
//         debug(`Error initializing speech recognition: ${error.message}`, 'error');
//     }
// }

// /**
//  * Reset the silence detection timer
//  */
// function resetSilenceTimer() {
//     clearTimeout(silenceTimer);
    
//     // Set a new silence timer
//     silenceTimer = setTimeout(() => {
//         if (isListening && !window.isProcessingReply) {
//             debug('Silence detected, stopping and restarting recognition', 'info');
//             try {
//                 stopSpeechRecognition();
//             } catch (e) {
//                 debug('Error stopping recognition on silence', 'error');
//             }
//         }
//     }, SILENCE_TIMEOUT);
// }

// /**
//  * Process speech from the user
//  */
// async function processSpeech(transcript) {
//     try {
//         // Stop recognition during processing
//         stopSpeechRecognition();
//         stopVisualizer();
        
//         // Set flag to prevent auto-restart during processing
//         window.isProcessingReply = true;
        
//         updateAvatarState('thinking');
        
//         // Process the user's input
//         await processUserInput(transcript);
        
//         // After processing, reset flag and restart recognition
//         window.isProcessingReply = false;
//         startSpeechRecognition();
        
//     } catch (error) {
//         debug(`Error processing speech: ${error.message}`, 'error');
//         window.isProcessingReply = false;
//         startSpeechRecognition();
//     }
// }

// /**
//  * Start speech recognition
//  */
// export function startSpeechRecognition() {
//     if (!recognition) {
//         debug('Recognition not initialized', 'error');
//         return;
//     }
    
//     if (isListening) {
//         debug('Already listening', 'warning');
//         return;
//     }
    
//     if (window.isProcessingReply) {
//         debug('Cannot start listening while processing reply', 'warning');
//         return;
//     }
    
//     try {
//         recognition.start();
//         debug('Recognition started successfully', 'success');
//     } catch (error) {
//         debug(`Error starting recognition: ${error.message}`, 'error');
        
//         // If we fail with "already started" error, stop and try again
//         if (error.message.includes('already started')) {
//             try {
//                 recognition.stop();
//                 // Try to restart after a delay
//                 setTimeout(() => {
//                     if (!window.isProcessingReply) {
//                         recognition.start();
//                     }
//                 }, 500);
//             } catch (e) {
//                 debug('Error stopping after failed start', 'error');
//             }
//         }
//     }
// }

// /**
//  * Stop speech recognition
//  */
// export function stopSpeechRecognition() {
//     if (recognition && isListening) {
//         try {
//             debug('Stopping recognition', 'info');
//             recognition.stop();
//         } catch (error) {
//             debug(`Error stopping recognition: ${error.message}`, 'error');
//         }
//     }
// }

// audioProcessor.js - Handles speech recognition

// Speech recognition variables
let recognition;
let recognitionCallback;
let isRecognitionSupported = false;

// Initialize speech recognition
function setupSpeechRecognition(callback) {
    return new Promise((resolve) => {
        try {
            // Check if the browser supports speech recognition
            if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
                console.error('Speech recognition not supported in this browser');
                resolve(false);
                return;
            }
            
            // Create a new SpeechRecognition instance
            const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
            recognition = new SpeechRecognition();
            
            // Configure speech recognition
            recognition.continuous = false;
            recognition.interimResults = false;
            recognition.lang = 'en-US';
            
            // Set up event handlers
            recognition.onstart = () => {
                console.info('Recognition started');
                document.dispatchEvent(new CustomEvent('recognitionStarted'));
            };
            
            recognition.onresult = (event) => {
                const transcript = event.results[0][0].transcript;
                if (recognitionCallback) {
                    recognitionCallback(transcript);
                }
            };
            
            recognition.onerror = (event) => {
                console.error('Recognition error:', event.error);
                document.dispatchEvent(new CustomEvent('recognitionError', { detail: event.error }));
                
                // Restart recognition on certain errors
                if (event.error === 'no-speech') {
                    setTimeout(() => {
                        startRecognition();
                    }, 1000);
                }
            };
            
            recognition.onend = () => {
                console.warn('Speech recognition ended.');
                document.dispatchEvent(new CustomEvent('recognitionEnded'));
            };
            
            // Store the callback
            recognitionCallback = callback;
            isRecognitionSupported = true;
            
            // Request microphone permission
            navigator.mediaDevices.getUserMedia({ audio: true })
                .then(() => {
                    console.log('Microphone permission granted');
                    resolve(true);
                })
                .catch((error) => {
                    console.error('Microphone permission denied:', error);
                    resolve(false);
                });
            
        } catch (error) {
            console.error('Error setting up speech recognition:', error);
            resolve(false);
        }
    });
}

// Start speech recognition
function startRecognition() {
    return new Promise((resolve) => {
        if (!isRecognitionSupported || !recognition) {
            resolve(false);
            return;
        }
        
        try {
            recognition.start();
            console.log('Recognition started successfully');
            resolve(true);
        } catch (error) {
            console.error('Error starting recognition:', error);
            resolve(false);
        }
    });
}

// Stop speech recognition
function stopRecognition() {
    if (!isRecognitionSupported || !recognition) {
        return;
    }
    
    try {
        recognition.stop();
    } catch (error) {
        console.error('Error stopping recognition:', error);
    }
}

// Check if auto-restart is needed and handle it
function autoRestartRecognition() {
    document.addEventListener('recognitionEnded', () => {
        // Auto restart in some cases, unless currently processing a reply
        if (!window.appState || !window.appState.isProcessingReply) {
            console.info('Auto-restarting recognition');
            setTimeout(startRecognition, 500);
        }
    });
}

// Export functions to the global scope
window.setupSpeechRecognition = setupSpeechRecognition;
window.startRecognition = startRecognition;
window.stopRecognition = stopRecognition;