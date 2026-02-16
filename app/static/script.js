const API_BASE_URL = 'http://localhost:5000';
const chatContainer = document.getElementById('chatContainer');
const messageInput = document.getElementById('messageInput');
const sendButton = document.getElementById('sendButton');
const streamToggle = document.getElementById('streamToggle');
const temperatureSlider = document.getElementById('temperature');
const tempValue = document.getElementById('tempValue');

let conversationHistory = [];

// Update temperature display
temperatureSlider.addEventListener('input', (e) => {
    tempValue.textContent = e.target.value;
});

// Auto-resize textarea
messageInput.addEventListener('input', function() {
    this.style.height = 'auto';
    this.style.height = (this.scrollHeight) + 'px';
});

// Send message on Enter (Shift+Enter for new line)
messageInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});

// Send button click
sendButton.addEventListener('click', sendMessage);

function sendMessage() {
    const message = messageInput.value.trim();
    if (!message) return;

    // Add user message to chat
    addMessage(message, 'user');
    
    // Add to conversation history
    conversationHistory.push({
        role: 'user',
        content: message
    });

    // Clear input
    messageInput.value = '';
    messageInput.style.height = 'auto';

    // Disable input while processing
    setInputState(false);

    // Send to API
    if (streamToggle.checked) {
        sendStreamingMessage();
    } else {
        sendNormalMessage();
    }
}

function addMessage(content, sender, isStreaming = false) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}`;
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    if (isStreaming) {
        contentDiv.classList.add('streaming');
    }
    contentDiv.textContent = content;
    
    messageDiv.appendChild(contentDiv);
    chatContainer.appendChild(messageDiv);
    
    // Scroll to bottom
    chatContainer.scrollTop = chatContainer.scrollHeight;
    
    return contentDiv;
}

function showError(error) {
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message';
    errorDiv.textContent = `Error: ${error}`;
    chatContainer.appendChild(errorDiv);
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

function setInputState(enabled) {
    sendButton.disabled = !enabled;
    messageInput.disabled = !enabled;
}

async function sendNormalMessage() {
    try {
        const response = await fetch(`${API_BASE_URL}/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                messages: conversationHistory,
                temperature: parseFloat(temperatureSlider.value)
            })
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Request failed');
        }

        const data = await response.json();
        
        // Add bot response
        addMessage(data.content, 'bot');
        
        // Add to conversation history
        conversationHistory.push({
            role: 'assistant',
            content: data.content
        });

    } catch (error) {
        showError(error.message);
    } finally {
        setInputState(true);
    }
}

async function sendStreamingMessage() {
    // Create bot message element for streaming
    const botMessageContent = addMessage('', 'bot', true);
    let fullResponse = '';

    try {
        const response = await fetch(`${API_BASE_URL}/chat/stream`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                messages: conversationHistory,
                temperature: parseFloat(temperatureSlider.value)
            })
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Request failed');
        }

        const reader = response.body.getReader();
        const decoder = new TextDecoder();

        while (true) {
            const { done, value } = await reader.read();
            
            if (done) break;

            const chunk = decoder.decode(value);
            const lines = chunk.split('\n');

            for (const line of lines) {
                if (line.startsWith('data: ')) {
                    const content = line.slice(6); // Remove 'data: ' prefix
                    if (content && !content.startsWith('[ERROR')) {
                        fullResponse += content;
                        botMessageContent.textContent = fullResponse;
                        chatContainer.scrollTop = chatContainer.scrollHeight;
                    } else if (content.startsWith('[ERROR')) {
                        throw new Error(content);
                    }
                }
            }
        }

        // Remove streaming indicator
        botMessageContent.classList.remove('streaming');

        // Add to conversation history
        conversationHistory.push({
            role: 'assistant',
            content: fullResponse
        });

    } catch (error) {
        showError(error.message);
        botMessageContent.remove();
    } finally {
        setInputState(true);
    }
}

// Initialize with a welcome message
window.addEventListener('load', () => {
    addMessage('Hello! I\'m your AI assistant. How can I help you today?', 'bot');
});
