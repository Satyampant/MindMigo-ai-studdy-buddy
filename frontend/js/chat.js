// Chat functionality for AI Tutor
const API_BASE_URL = window.API_CONFIG?.BASE_URL || 'http://localhost:8000';
const STUDENT_ID = 'student_' + Math.random().toString(36).substr(2, 9);

let conversationId = null;
let isWaitingForResponse = false;

// DOM Elements
const chatMessages = document.getElementById('chatMessages');
const chatForm = document.getElementById('chatForm');
const messageInput = document.getElementById('messageInput');
const sendBtn = document.getElementById('sendBtn');

// Initialize chat
document.addEventListener('DOMContentLoaded', () => {
    chatForm.addEventListener('submit', handleSendMessage);
    messageInput.focus();
});

// Send message handler
async function handleSendMessage(e) {
    e.preventDefault();
    
    const message = messageInput.value.trim();
    if (!message || isWaitingForResponse) return;
    
    // Clear input and disable form
    messageInput.value = '';
    isWaitingForResponse = true;
    sendBtn.disabled = true;
    
    // Display student message
    addMessage('student', message);
    
    // Show typing indicator
    const typingId = showTypingIndicator();
    
    try {
        const response = await fetch(`${API_BASE_URL}/chat/message`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                student_id: STUDENT_ID,
                message: message,
                conversation_id: conversationId
            })
        });
        
        if (!response.ok) throw new Error('Failed to get response');
        
        const data = await response.json();
        conversationId = data.conversation_id;
        
        // Remove typing indicator and show tutor response
        removeTypingIndicator(typingId);
        addMessage('tutor', data.reply);
        
    } catch (error) {
        removeTypingIndicator(typingId);
        addMessage('tutor', '❌ Sorry, I encountered an error. Please try again.');
        console.error('Chat error:', error);
    } finally {
        isWaitingForResponse = false;
        sendBtn.disabled = false;
        messageInput.focus();
    }
}

// Add message to chat
function addMessage(role, content) {
    const welcomeMsg = chatMessages.querySelector('.welcome-message');
    if (welcomeMsg) welcomeMsg.remove();
    
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${role}`;
    
    const avatar = role === 'student' ? '👤' : '🤖';
    const time = new Date().toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' });
    
    messageDiv.innerHTML = `
        <div class="message-avatar">${avatar}</div>
        <div class="message-content">
            <div class="message-bubble">${escapeHtml(content)}</div>
            <div class="message-time">${time}</div>
        </div>
    `;
    
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Show typing indicator
function showTypingIndicator() {
    const typingDiv = document.createElement('div');
    const typingId = 'typing_' + Date.now();
    typingDiv.id = typingId;
    typingDiv.className = 'message tutor';
    typingDiv.innerHTML = `
        <div class="message-avatar">🤖</div>
        <div class="message-content">
            <div class="message-bubble">
                <div class="typing-indicator">
                    <div class="typing-dot"></div>
                    <div class="typing-dot"></div>
                    <div class="typing-dot"></div>
                </div>
            </div>
        </div>
    `;
    chatMessages.appendChild(typingDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
    return typingId;
}

// Remove typing indicator
function removeTypingIndicator(typingId) {
    const typingDiv = document.getElementById(typingId);
    if (typingDiv) typingDiv.remove();
}

// Clear chat and start new conversation
function clearChat() {
    conversationId = null;
    chatMessages.innerHTML = `
        <div class="welcome-message">
            <span class="welcome-icon">👋</span>
            <h3>Welcome to AI Tutor!</h3>
            <p>Ask me anything about your studies. I'm here to help explain concepts, solve problems, and guide your learning journey.</p>
        </div>
    `;
    messageInput.value = '';
    messageInput.focus();
}

// Escape HTML to prevent XSS
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Handle enter key
messageInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        chatForm.dispatchEvent(new Event('submit'));
    }
});
