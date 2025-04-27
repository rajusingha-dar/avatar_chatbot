import os
import pathlib

def fix_language_issue():
    """Fix the language issue by updating files to ensure English responses"""
    project_dir = os.getcwd()  # Assuming you run from the avatar_project directory
    voice_avatar_dir = os.path.join(project_dir, 'voice-avatar-chatbot')
    
    # 1. Update the chat.py file
    chat_path = os.path.join(voice_avatar_dir, 'modules', 'routes', 'chat.py')
    
    # Read current content
    with open(chat_path, 'r', encoding='utf-8') as f:
        chat_content = f.read()
    
    # Find the section where we process messages
    # We need to add a system message that forces English responses
    if "def add_chat_routes(app: FastAPI):" in chat_content:
        print("Updating chat.py to enforce English language...")
        
        # Split the content to find the right section
        parts = chat_content.split("def generate_text(request: ChatRequest):")
        if len(parts) >= 2:
            # Find where we create the payload
            payload_section = parts[1].split("payload = {")
            if len(payload_section) >= 2:
                # Add a system message
                new_content = (
                    parts[0] + 
                    "def generate_text(request: ChatRequest):" + 
                    payload_section[0] +
                    "# Add a system message to force responses in English\n" +
                    "            system_messages = [{\"role\": \"system\", \"content\": \"You are a helpful AI assistant. Always respond in English.\"}]\n" +
                    "            \n" +
                    "            # Add user messages\n" +
                    "            user_messages = []\n" +
                    "            for msg in request.messages:\n" +
                    "                user_messages.append({\"role\": msg.role, \"content\": msg.content})\n" +
                    "            \n" +
                    "            all_messages = system_messages + user_messages\n" +
                    "            \n" +
                    "            payload = {\n" +
                    "                \"model\": \"gpt-4-turbo-preview\",\n" +
                    "                \"messages\": all_messages,\n" +
                    "                \"max_tokens\": 300\n" +
                    "            }\n"
                )
                
                # Find the rest of the file after payload definition
                rest_of_file = payload_section[1].split("max_tokens")
                if len(rest_of_file) >= 2:
                    rest_of_file = rest_of_file[1].split("}", 1)
                    if len(rest_of_file) >= 2:
                        new_content += rest_of_file[1]
                        
                        # Write the updated content
                        with open(chat_path, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        print("Successfully updated chat.py!")
                    else:
                        print("Could not find the ending of payload section.")
                else:
                    print("Could not find max_tokens in payload section.")
            else:
                print("Could not find payload section in generate_text function.")
        else:
            print("Could not find generate_text function.")
    else:
        print("Could not find add_chat_routes function.")
    
    # 2. Update index.html file with English instructions
    static_dir = os.path.join(voice_avatar_dir, 'static')
    if not os.path.exists(static_dir):
        os.makedirs(static_dir)
        print(f"Created directory: {static_dir}")
    
    index_path = os.path.join(static_dir, 'index.html')
    print(f"Creating new index.html with English setup...")
    
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write("""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Voice Avatar Chatbot</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            background-color: #f8f9fa;
            color: #333;
            padding: 20px;
        }

        .container {
            max-width: 800px;
            margin: 0 auto;
            background-color: white;
            border-radius: 10px;
            box-shadow: 0 0 20px rgba(0, 0, 0, 0.1);
            padding: 30px;
        }

        h1 {
            text-align: center;
            margin-bottom: 20px;
            color: #2c3e50;
            font-size: 2.2rem;
        }

        .subtitle {
            text-align: center;
            color: #7f8c8d;
            margin-bottom: 30px;
            font-size: 1.1rem;
        }

        #avatar-container {
            width: 200px;
            height: 200px;
            margin: 0 auto 30px;
            background-color: #eee;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 24px;
            color: #666;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }

        .avatar-placeholder {
            text-align: center;
            font-weight: bold;
        }

        .avatar-state {
            position: absolute;
            bottom: 10px;
            left: 0;
            right: 0;
            text-align: center;
            font-size: 14px;
            background-color: rgba(0, 0, 0, 0.5);
            color: white;
            padding: 5px;
        }

        .controls {
            display: flex;
            justify-content: center;
            gap: 15px;
            margin-bottom: 30px;
        }

        button {
            padding: 12px 25px;
            background-color: #3498db;
            color: white;
            border: none;
            border-radius: 50px;
            cursor: pointer;
            font-size: 1rem;
            font-weight: 600;
            transition: all 0.2s ease;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        button:hover {
            background-color: #2980b9;
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }

        button:active {
            transform: translateY(0);
        }

        button:disabled {
            background-color: #95a5a6;
            cursor: not-allowed;
            transform: none;
            box-shadow: none;
        }

        button i {
            margin-right: 8px;
        }

        .conversation {
            background-color: #f8f9fa;
            border-radius: 10px;
            padding: 20px;
            max-height: 300px;
            overflow-y: auto;
            margin-bottom: 20px;
        }

        #messages {
            display: flex;
            flex-direction: column;
            gap: 15px;
        }

        .message {
            padding: 12px 15px;
            border-radius: 18px;
            max-width: 80%;
            line-height: 1.4;
            position: relative;
            animation: fadeIn 0.3s ease-in-out;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .user-message {
            align-self: flex-end;
            background-color: #3498db;
            color: white;
            border-bottom-right-radius: 5px;
        }

        .bot-message {
            align-self: flex-start;
            background-color: #e9e9eb;
            color: #333;
            border-bottom-left-radius: 5px;
        }

        .status {
            text-align: center;
            margin: 20px 0;
            font-style: italic;
            color: #7f8c8d;
        }

        .audio-visualizer {
            height: 60px;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 5px;
            margin-bottom: 20px;
            display: none;
        }

        .audio-bar {
            width: 5px;
            height: 20px;
            background-color: #3498db;
            border-radius: 3px;
        }

        /* States for the avatar container */
        #avatar-container.idle {
            background-color: #eee;
        }

        #avatar-container.listening {
            background-color: #a8e6cf;
        }

        #avatar-container.thinking {
            background-color: #ffd3b6;
        }

        #avatar-container.speaking {
            background-color: #d9bbf9;
        }

        footer {
            text-align: center;
            margin-top: 30px;
            color: #95a5a6;
            font-size: 0.9rem;
        }

        /* Icons for buttons */
        .icon-mic, .icon-stop {
            display: inline-block;
            width: 20px;
            height: 20px;
            margin-right: 8px;
            background-size: contain;
            background-repeat: no-repeat;
            background-position: center;
        }

        .icon-mic {
            background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='white'%3E%3Cpath d='M12 14c1.66 0 3-1.34 3-3V5c0-1.66-1.34-3-3-3S9 3.34 9 5v6c0 1.66 1.34 3 3 3zm5.91-3c-.49 0-.9.36-.98.85C16.52 14.2 14.47 16 12 16s-4.52-1.8-4.93-4.15c-.08-.49-.49-.85-.98-.85-.61 0-1.09.54-1 1.14.49 3 2.89 5.35 5.91 5.78V20c0 .55.45 1 1 1s1-.45 1-1v-2.08c3.02-.43 5.42-2.78 5.91-5.78.1-.6-.39-1.14-1-1.14z'/%3E%3C/svg%3E");
        }

        .icon-stop {
            background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='white'%3E%3Cpath d='M6 6h12v12H6z'/%3E%3C/svg%3E");
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Voice Avatar Chatbot</h1>
        <p class="subtitle">Speak to chat with an AI assistant</p>

        <div id="avatar-container" class="idle">
            <div class="avatar-placeholder">AI</div>
            <div class="avatar-state">Idle</div>
        </div>

        <div class="audio-visualizer" id="visualizer">
            <div class="audio-bar"></div>
            <div class="audio-bar"></div>
            <div class="audio-bar"></div>
            <div class="audio-bar"></div>
            <div class="audio-bar"></div>
        </div>

        <div class="controls">
            <button id="start-recording">
                <span class="icon-mic"></span>Start Recording
            </button>
            <button id="stop-recording" disabled>
                <span class="icon-stop"></span>Stop Recording
            </button>
        </div>

        <p class="status" id="status">Ready to chat! Click "Start Recording" to begin.</p>

        <div class="conversation">
            <div id="messages">
                <div class="message bot-message">
                    Hello! I'm your AI assistant. How can I help you today?
                </div>
            </div>
        </div>

        <footer>
            Voice Avatar Chatbot &copy; 2025
        </footer>
    </div>

    <script>
        // Main app functionality
        document.addEventListener('DOMContentLoaded', function() {
            // DOM elements
            const startRecordingButton = document.getElementById('start-recording');
            const stopRecordingButton = document.getElementById('stop-recording');
            const messagesContainer = document.getElementById('messages');
            const avatarContainer = document.getElementById('avatar-container');
            const statusElement = document.getElementById('status');
            const visualizer = document.getElementById('visualizer');
            const avatarState = avatarContainer.querySelector('.avatar-state');

            // Audio processing variables
            let mediaRecorder = null;
            let audioChunks = [];
            let stream = null;

            // Update avatar state
            function updateAvatarState(state) {
                // Remove all state classes
                avatarContainer.classList.remove('idle', 'listening', 'thinking', 'speaking');
                // Add the new state class
                avatarContainer.classList.add(state);
                // Update the text
                avatarState.textContent = state.charAt(0).toUpperCase() + state.slice(1);
            }

            // Add a message to the conversation
            function addMessage(type, content) {
                const messageElement = document.createElement('div');
                messageElement.classList.add('message', `${type}-message`);
                messageElement.textContent = content;
                messagesContainer.appendChild(messageElement);
                messageElement.scrollIntoView({ behavior: 'smooth' });
                return messageElement;
            }

            // Update a message's content
            function updateMessage(messageElement, content) {
                if (messageElement) {
                    messageElement.textContent = content;
                }
            }

            // Start recording audio
            async function startRecording() {
                try {
                    audioChunks = [];
                    stream = await navigator.mediaDevices.getUserMedia({ audio: true });
                    mediaRecorder = new MediaRecorder(stream);
                    
                    mediaRecorder.ondataavailable = (event) => {
                        audioChunks.push(event.data);
                    };
                    
                    mediaRecorder.start();
                    
                    // Show the audio visualizer
                    visualizer.style.display = 'flex';
                    animateVisualizer();
                    
                    return true;
                } catch (error) {
                    console.error('Error starting recording:', error);
                    statusElement.textContent = 'Error: Could not access microphone';
                    return false;
                }
            }

            // Stop recording audio
            function stopRecording() {
                return new Promise((resolve) => {
                    mediaRecorder.onstop = () => {
                        const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
                        stream.getTracks().forEach(track => track.stop());
                        
                        // Hide the audio visualizer
                        visualizer.style.display = 'none';
                        
                        resolve(audioBlob);
                    };
                    
                    mediaRecorder.stop();
                });
            }

            // Animate the audio visualizer
            function animateVisualizer() {
                if (visualizer.style.display === 'flex') {
                    const bars = visualizer.querySelectorAll('.audio-bar');
                    bars.forEach(bar => {
                        const height = Math.floor(Math.random() * 40) + 10;
                        bar.style.height = `${height}px`;
                    });
                    
                    setTimeout(animateVisualizer, 150);
                }
            }

            // Send audio to the server for speech-to-text conversion
            async function speechToText(audioBlob) {
                const formData = new FormData();
                formData.append('audio_file', audioBlob);
                
                try {
                    const response = await fetch('/api/speech-to-text', {
                        method: 'POST',
                        body: formData
                    });
                    
                    if (!response.ok) {
                        throw new Error('Speech to text conversion failed');
                    }
                    
                    const data = await response.json();
                    return data.text;
                } catch (error) {
                    console.error('Error in speech-to-text:', error);
                    return null;
                }
            }

            // Send text to the server for chat response
            async function sendChat(text) {
                try {
                    const response = await fetch('/api/generate-text', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({
                            messages: [
                                { role: "system", content: "You are a helpful, friendly AI assistant. Always respond in English." },
                                { role: "user", content: text }
                            ]
                        })
                    });
                    
                    if (!response.ok) {
                        throw new Error('Chat request failed');
                    }
                    
                    const data = await response.json();
                    return data.choices[0].message.content;
                } catch (error) {
                    console.error('Error in chat:', error);
                    return 'Sorry, I encountered an error processing your request.';
                }
            }

            // Send text to the server for text-to-speech conversion
            async function textToSpeech(text) {
                try {
                    const response = await fetch('/api/text-to-speech', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({
                            text: text,
                            voice_id: '21m00Tcm4TlvDq8ikWAM' // Default ElevenLabs voice ID
                        })
                    });
                    
                    if (!response.ok) {
                        throw new Error('Text to speech conversion failed');
                    }
                    
                    const blob = await response.blob();
                    return URL.createObjectURL(blob);
                } catch (error) {
                    console.error('Error in text-to-speech:', error);
                    return null;
                }
            }

            // Play audio
            function playAudio(audioUrl, onEnded) {
                if (!audioUrl) {
                    if (onEnded) onEnded();
                    return;
                }
                
                const audio = new Audio(audioUrl);
                audio.onended = onEnded;
                audio.play();
            }

            // Button event listeners
            startRecordingButton.addEventListener('click', async () => {
                startRecordingButton.disabled = true;
                stopRecordingButton.disabled = false;
                statusElement.textContent = 'Listening...';
                updateAvatarState('listening');
                
                const success = await startRecording();
                if (!success) {
                    startRecordingButton.disabled = false;
                    stopRecordingButton.disabled = true;
                    updateAvatarState('idle');
                }
            });
            
            stopRecordingButton.addEventListener('click', async () => {
                startRecordingButton.disabled = false;
                stopRecordingButton.disabled = true;
                statusElement.textContent = 'Processing...';
                
                // Get the audio recording
                const audioBlob = await stopRecording();
                
                // Add a placeholder user message
                const userMessageElement = addMessage('user', 'Processing your request...');
                
                // Process the recording (speech-to-text)
                updateAvatarState('thinking');
                const transcription = await speechToText(audioBlob);
                
                if (transcription) {
                    // Update the user message with the transcription
                    updateMessage(userMessageElement, transcription);
                    
                    // Get the chat response
                    const response = await sendChat(transcription);
                    
                    // Add the bot response
                    addMessage('bot', response);
                    
                    // Convert the response to speech and play it
                    updateAvatarState('speaking');
                    const audioUrl = await textToSpeech(response);
                    
                    playAudio(audioUrl, () => {
                        updateAvatarState('idle');
                        statusElement.textContent = 'Ready to chat! Click "Start Recording" to begin.';
                    });
                } else {
                    // Handle speech-to-text failure
                    updateMessage(userMessageElement, 'Sorry, I could not understand what you said.');
                    addMessage('bot', 'Please try again.');
                    updateAvatarState('idle');
                    statusElement.textContent = 'Ready to chat! Click "Start Recording" to begin.';
                }
            });

            // Initialize
            updateAvatarState('idle');
        });

        // Fallback for testing without APIs
        function simulateConversation() {
            const startRecordingButton = document.getElementById('start-recording');
            const stopRecordingButton = document.getElementById('stop-recording');
            const messagesContainer = document.getElementById('messages');
            const avatarContainer = document.getElementById('avatar-container');
            const statusElement = document.getElementById('status');
            const visualizer = document.getElementById('visualizer');
            const avatarState = avatarContainer.querySelector('.avatar-state');

            // Test responses (English only)
            const testResponses = [
                { user: "Hi there, how are you?", bot: "I'm doing well, thank you for asking! How can I assist you today?" },
                { user: "What's the weather like?", bot: "I don't have access to real-time weather data, but I'd be happy to discuss weather patterns or help you find a weather service." },
                { user: "Tell me a joke", bot: "Why don't scientists trust atoms? Because they make up everything!" },
                { user: "What can you help me with?", bot: "I can assist with answering questions, providing information, having conversations, writing content, and much more. Just let me know what you need!" }
            ];

            // Update avatar state
            function updateAvatarState(state) {
                avatarContainer.classList.remove('idle', 'listening', 'thinking', 'speaking');
                avatarContainer.classList.add(state);
                avatarState.textContent = state.charAt(0).toUpperCase() + state.slice(1);
            }

            // Add a message to the conversation
            function addMessage(type, content) {
                const messageElement = document.createElement('div');
                messageElement.classList.add('message', `${type}-message`);
                messageElement.textContent = content;
                messagesContainer.appendChild(messageElement);
                messageElement.scrollIntoView({ behavior: 'smooth' });
            }

            // Button event listeners for testing
            startRecordingButton.addEventListener('click', () => {
                startRecordingButton.disabled = true;
                stopRecordingButton.disabled = false;
                statusElement.textContent = 'Listening...';
                updateAvatarState('listening');
                
                visualizer.style.display = 'flex';
                animateVisualizer();
            });
            
            stopRecordingButton.addEventListener('click', () => {
                startRecordingButton.disabled = false;
                stopRecordingButton.disabled = true;
                statusElement.textContent = 'Processing...';
                visualizer.style.display = 'none';
                
                // Get a random test response
                const testResponse = testResponses[Math.floor(Math.random() * testResponses.length)];
                
                // Simulate the processing
                updateAvatarState('thinking');
                setTimeout(() => {
                    // Add user message
                    addMessage('user', testResponse.user);
                    
                    // Simulate thinking
                    setTimeout(() => {
                        // Add bot response
                        addMessage('bot', testResponse.bot);
                        
                        // Simulate speaking
                        updateAvatarState('speaking');
                        setTimeout(() => {
                            updateAvatarState('idle');
                            statusElement.textContent = 'Ready to chat! Click "Start Recording" to begin.';
                        }, 3000);
                    }, 1000);
                }, 1500);
            });

            // Animate the audio visualizer
            function animateVisualizer() {
                if (visualizer.style.display === 'flex') {
                    const bars = visualizer.querySelectorAll('.audio-bar');
                    bars.forEach(bar => {
                        const height = Math.floor(Math.random() * 40) + 10;
                        bar.style.height = `${height}px`;
                    });
                    
                    setTimeout(animateVisualizer, 150);
                }
            }
        }
        
        // Uncomment this line for testing without API calls
        simulateConversation();
    </script>
</body>
</html>""")
    
    print("Successfully created index.html with English instructions!")
    print("\nYour Voice Avatar Chatbot should now respond in English. Please restart your server for the changes to take effect.")

if __name__ == "__main__":
    fix_language_issue()