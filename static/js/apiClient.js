// static/js/apiClient.js

// Function to send user's message to backend and receive AI response
export async function generateText(userMessages) {
    try {
        // Convert the conversation history to the format expected by the API
        const messages = userMessages.map(msg => ({
            role: msg.role,
            content: msg.content
        }));
        
        const response = await fetch("/api/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                messages: messages
            })
        });

        if (!response.ok) {
            const errorData = await response.json().catch(() => null);
            throw new Error(`Failed to generate text: ${response.statusText}${errorData ? ' - ' + JSON.stringify(errorData) : ''}`);
        }

        const data = await response.json();
        console.log("[info] AI response received:", data);

        // Return the AI's message content
        return data;
    } catch (error) {
        console.error("[error] Error: Failed to generate text", error);
        return {
            choices: [{
                message: {
                    content: "Sorry, something went wrong. Please try again in a moment."
                }
            }]
        };
    }
}

// Function to perform a direct search (for testing)
export async function performSearch(query) {
    try {
        const response = await fetch("/api/search", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                query: query
            })
        });

        if (!response.ok) {
            throw new Error("Search failed");
        }

        const data = await response.json();
        console.log("[info] Search Response:", data);
        return data;
    } catch (error) {
        console.error("[error] Search failed:", error.message);
        return null;
    }
}

// Health check function (API test)
export async function testAPI() {
    try {
        const response = await fetch("/api/test");
        if (!response.ok) {
            throw new Error("API not reachable");
        }
        const data = await response.json();
        console.log("[info] API Test Response:", data);
        return true;
    } catch (error) {
        console.error("[error] API test failed:", error.message);
        return false;
    }
}

// Implemented Text-to-Speech function using Web Speech API
export async function textToSpeech(text) {
    return new Promise((resolve, reject) => {
        console.log("[info] textToSpeech called with text:", text);
        
        // Check if speech synthesis is available
        if (!window.speechSynthesis) {
            console.error("[error] Speech synthesis not supported");
            reject(new Error("Speech synthesis not supported in this browser"));
            return;
        }
        
        // Create utterance
        const utterance = new SpeechSynthesisUtterance(text);
        
        // Configure voice settings
        utterance.lang = 'en-US';
        utterance.rate = 1.0;  // Speed: 0.1 to 10
        utterance.pitch = 1.0; // Pitch: 0 to 2
        utterance.volume = 1.0; // Volume: 0 to 1
        
        // Try to use a more natural voice if available
        const voices = window.speechSynthesis.getVoices();
        console.log("[info] Available voices:", voices.length);
        
        // Look for higher quality voices (prefer neural/enhanced voices)
        let preferredVoice = null;
        
        // Try to find a good voice
        for (const voice of voices) {
            // Prefer newer, higher quality voices
            if (voice.lang.includes('en') && 
                (voice.name.includes('Neural') || 
                 voice.name.includes('Enhanced') || 
                 voice.name.includes('Premium'))) {
                preferredVoice = voice;
                break;
            }
        }
        
        // Fallback to any English voice if no premium voice found
        if (!preferredVoice) {
            preferredVoice = voices.find(voice => voice.lang.includes('en'));
        }
        
        if (preferredVoice) {
            console.log("[info] Using voice:", preferredVoice.name);
            utterance.voice = preferredVoice;
        }
        
        // Handle events
        utterance.onstart = () => {
            console.log("[info] Speech started");
        };
        
        utterance.onend = () => {
            console.log("[info] Speech ended");
            resolve();
        };
        
        utterance.onerror = (event) => {
            console.error("[error] Speech synthesis error:", event.error);
            reject(new Error(`Speech synthesis error: ${event.error}`));
        };
        
        // Start speaking
        window.speechSynthesis.speak(utterance);
    });
}

// Force load voices earlier (some browsers need this)
function loadVoices() {
    // This is needed in some browsers to get the voice list
    if (window.speechSynthesis) {
        window.speechSynthesis.getVoices();
    }
}

// Try to load voices on page load
loadVoices();

// Browsers sometimes need an event to load voices
if (window.speechSynthesis && window.speechSynthesis.onvoiceschanged !== undefined) {
    window.speechSynthesis.onvoiceschanged = loadVoices;
}