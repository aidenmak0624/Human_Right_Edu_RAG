// API Configuration
const API_BASE = 'http://localhost:5050';

// State
let currentTopic = null;

// Elements
const topicSelection = document.getElementById('topic-selection');
const chatSection = document.getElementById('chat-section');
const topicsGrid = document.getElementById('topics-grid');
const chatContainer = document.getElementById('chat-container');
const userInput = document.getElementById('user-input');
const sendBtn = document.getElementById('send-btn');
const backBtn = document.getElementById('back-btn');
const currentTopicEl = document.getElementById('current-topic');

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    loadTopics();
    setupEventListeners();
});

// Load topics from API
async function loadTopics() {
    try {
        const response = await fetch(`${API_BASE}/api/topics`);
        const data = await response.json();
        
        topicsGrid.innerHTML = '';
        
        data.topics.forEach(topic => {
            const card = createTopicCard(topic);
            topicsGrid.appendChild(card);
        });
        
    } catch (error) {
        console.error('Error loading topics:', error);
        topicsGrid.innerHTML = '<p>Error loading topics. Please refresh.</p>';
    }
}

// Create topic card
function createTopicCard(topic) {
    const card = document.createElement('div');
    card.className = 'topic-card';
    card.innerHTML = `
        <div class="icon">${topic.icon}</div>
        <h3>${topic.name}</h3>
        <p>${topic.description}</p>
    `;
    
    card.addEventListener('click', () => selectTopic(topic));
    
    return card;
}

// Select topic
function selectTopic(topic) {
    currentTopic = topic;
    currentTopicEl.textContent = topic.name;
    
    // Switch views
    topicSelection.classList.add('hidden');
    chatSection.classList.remove('hidden');
    
    // Clear chat
    chatContainer.innerHTML = '';
    
    // Add welcome message
    addBotMessage(`Welcome! Ask me anything about ${topic.name}.`);
    
    // Focus input
    userInput.focus();
}

// Setup event listeners
function setupEventListeners() {
    sendBtn.addEventListener('click', sendMessage);
    
    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });
    
    backBtn.addEventListener('click', () => {
        topicSelection.classList.remove('hidden');
        chatSection.classList.add('hidden');
        currentTopic = null;
    });
}

// Send message
async function sendMessage() {
    const query = userInput.value.trim();
    
    if (!query) return;
    
    // Add user message
    addUserMessage(query);
    
    // Clear input
    userInput.value = '';
    
    // Show loading
    const loadingId = addLoadingMessage();
    
    try {
        // Call API
        const response = await fetch(`${API_BASE}/api/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                query: query,
                topic: currentTopic.id
            })
        });
        
        const data = await response.json();
        
        // Remove loading
        removeMessage(loadingId);
        
        if (response.ok) {
            // Add bot response
            addBotMessage(data.answer, data.sources);
        } else {
            addBotMessage(`Error: ${data.error || 'Something went wrong'}`);
        }
        
    } catch (error) {
        removeMessage(loadingId);
        addBotMessage('Sorry, I encountered an error. Please try again.');
        console.error('Error:', error);
    }
}

// Add user message
function addUserMessage(text) {
    const message = document.createElement('div');
    message.className = 'message user';
    message.innerHTML = `
        <div class="message-content">${escapeHtml(text)}</div>
    `;
    chatContainer.appendChild(message);
    scrollToBottom();
}

// Add bot message
function addBotMessage(text, sources = []) {
    const message = document.createElement('div');
    message.className = 'message bot';
    
    let html = `<div class="message-content">${escapeHtml(text)}`;
    
    if (sources && sources.length > 0) {
        html += `<div class="sources">📚 Sources: ${sources.join(', ')}</div>`;
    }
    
    html += '</div>';
    
    message.innerHTML = html;
    chatContainer.appendChild(message);
    scrollToBottom();
}

// Add loading message
function addLoadingMessage() {
    const id = 'loading-' + Date.now();
    const message = document.createElement('div');
    message.id = id;
    message.className = 'message bot';
    message.innerHTML = '<div class="message-content loading">Thinking</div>';
    chatContainer.appendChild(message);
    scrollToBottom();
    return id;
}

// Remove message
function removeMessage(id) {
    const message = document.getElementById(id);
    if (message) {
        message.remove();
    }
}

// Scroll to bottom
function scrollToBottom() {
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

// Escape HTML
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}
