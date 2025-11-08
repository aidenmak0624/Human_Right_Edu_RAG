// API Configuration
const API_BASE = 'http://localhost:5050';

// State
let currentTopic = null;
let currentDifficulty = 'intermediate';
let conversationHistory = [];

// Elements
const topicSelection = document.getElementById('topic-selection');
const chatSection = document.getElementById('chat-section');
const topicsGrid = document.getElementById('topics-grid');
const chatContainer = document.getElementById('chat-container');
const userInput = document.getElementById('user-input');
const sendBtn = document.getElementById('send-btn');
const backBtn = document.getElementById('back-btn');
const currentTopicEl = document.getElementById('current-topic');

// ============================================
// INITIALIZATION
// ============================================

document.addEventListener('DOMContentLoaded', () => {
    loadTopics();
    setupEventListeners();
});

// ============================================
// TOPICS
// ============================================

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

function selectTopic(topic) {
    currentTopic = topic;
    currentTopicEl.textContent = topic.name;
    
    // Switch views
    topicSelection.classList.add('hidden');
    chatSection.classList.remove('hidden');
    
    // Clear chat
    chatContainer.innerHTML = '';
    conversationHistory = [];
    
    // Add welcome message
    const welcomeDiv = document.createElement('div');
    welcomeDiv.className = 'message ai-message';
    welcomeDiv.innerHTML = `
        <div class="message-content">
            Welcome! Ask me anything about ${topic.name}.
        </div>
    `;
    chatContainer.appendChild(welcomeDiv);
    
    // Focus input
    userInput.focus();
}

// ============================================
// EVENT LISTENERS
// ============================================

function setupEventListeners() {
    sendBtn.addEventListener('click', sendMessage);
    
    userInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });
    
    backBtn.addEventListener('click', () => {
        topicSelection.classList.remove('hidden');
        chatSection.classList.add('hidden');
        currentTopic = null;
        conversationHistory = [];
    });
}

// ============================================
// DIFFICULTY
// ============================================

function updateDifficulty(level) {
    currentDifficulty = level;
    
    const hints = {
        'beginner': 'Simple explanations with examples',
        'intermediate': 'Balanced detail and accessibility',
        'advanced': 'Comprehensive legal analysis'
    };
    
    document.getElementById('difficulty-hint').textContent = hints[level];
}

// ============================================
// MESSAGING
// ============================================

async function sendMessage() {
    const query = userInput.value.trim();
    
    if (!query || !currentTopic) return;
    
    // Add user message
    displayUserMessage(query);
    
    // Clear input
    userInput.value = '';
    
    // Show loading
    showLoadingIndicator();
    
    try {
        const response = await fetch(`${API_BASE}/api/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                query: query,
                topic: currentTopic.id,
                difficulty: currentDifficulty
            })
        });
        
        removeLoadingIndicator();
        
        if (!response.ok) {
            throw new Error(`Server error: ${response.status}`);
        }
        
        const data = await response.json();
        
        if (data.error) {
            throw new Error(data.error);
        }
        
        displayAIMessage(data.answer, data.sources);
        
    } catch (error) {
        removeLoadingIndicator();
        console.error('Error:', error);
        displayError('Failed to get response. Please check your connection and try again.');
    }
}

// ============================================
// DISPLAY FUNCTIONS
// ============================================

function displayUserMessage(message) {
    const userDiv = document.createElement('div');
    userDiv.className = 'message user-message';
    userDiv.innerHTML = `
        <div class="message-content">${escapeHtml(message)}</div>
        <div class="message-time">${getCurrentTime()}</div>
    `;
    chatContainer.appendChild(userDiv);
    
    conversationHistory.push({
        role: 'user',
        content: message,
        timestamp: new Date()
    });
    
    scrollToBottom();
}

function displayAIMessage(answer, sources) {
    const aiDiv = document.createElement('div');
    aiDiv.className = 'message ai-message';
    aiDiv.innerHTML = `
        <div class="message-content">${formatAnswer(answer)}</div>
        ${createSourcesHTML(sources)}
        <div class="message-actions">
            <button class="copy-btn" onclick="copyToClipboard(this)">
                <span class="icon">📋</span> Copy
            </button>
        </div>
        <div class="message-time">${getCurrentTime()}</div>
    `;
    chatContainer.appendChild(aiDiv);
    
    conversationHistory.push({
        role: 'assistant',
        content: answer,
        sources: sources,
        timestamp: new Date()
    });
    
    scrollToBottom();
}

function showLoadingIndicator() {
    const loadingDiv = document.createElement('div');
    loadingDiv.className = 'message ai-message loading-message';
    loadingDiv.id = 'loading-indicator';
    loadingDiv.innerHTML = `
        <div class="typing-indicator">
            <span></span>
            <span></span>
            <span></span>
        </div>
    `;
    chatContainer.appendChild(loadingDiv);
    scrollToBottom();
}

function removeLoadingIndicator() {
    const loading = document.getElementById('loading-indicator');
    if (loading) loading.remove();
}

function displayError(message) {
    const errorDiv = document.createElement('div');
    errorDiv.className = 'message error-message';
    errorDiv.innerHTML = `
        <div class="error-icon">⚠️</div>
        <div class="error-content">
            <strong>Oops! Something went wrong</strong>
            <p>${escapeHtml(message)}</p>
        </div>
        <button class="dismiss-btn" onclick="this.closest('.error-message').remove()">
            Dismiss
        </button>
    `;
    chatContainer.appendChild(errorDiv);
    scrollToBottom();
}

// ============================================
// SOURCE DISPLAY
// ============================================

function createSourcesHTML(sources) {
    if (!sources || sources.length === 0) {
        return '';
    }
    
    const sourceBadges = sources.map(source => {
        const match = source.match(/(.+?)\s*\(score=([\d.]+)\)/);
        
        if (match) {
            const [_, filename, scoreStr] = match;
            const score = parseFloat(scoreStr);
            const relevancePercent = Math.max(0, Math.min(100, (1 - score) * 100)).toFixed(0);
            const color = getRelevanceColor(relevancePercent);
            
            return `
                <span class="source-badge" style="border-color: ${color}">
                    <span class="source-icon">📄</span>
                    <span class="source-name">${escapeHtml(filename)}</span>
                    <span class="source-relevance" style="color: ${color}">
                        ${relevancePercent}%
                    </span>
                </span>
            `;
        }
        
        return `
            <span class="source-badge">
                <span class="source-icon">📄</span>
                <span class="source-name">${escapeHtml(source)}</span>
            </span>
        `;
    }).join('');
    
    return `
        <div class="sources-section">
            <div class="sources-header">
                <span class="sources-icon">📚</span>
                <strong>Sources</strong>
            </div>
            <div class="sources-list">
                ${sourceBadges}
            </div>
        </div>
    `;
}

function getRelevanceColor(percent) {
    if (percent >= 80) return '#28a745';
    if (percent >= 60) return '#17a2b8';
    if (percent >= 40) return '#ffc107';
    return '#dc3545';
}

// ============================================
// COPY FUNCTIONALITY
// ============================================

function copyToClipboard(button) {
    const messageDiv = button.closest('.ai-message');
    const contentDiv = messageDiv.querySelector('.message-content');
    const text = contentDiv.innerText;
    
    navigator.clipboard.writeText(text).then(() => {
        const originalHTML = button.innerHTML;
        button.innerHTML = '<span class="icon">✅</span> Copied!';
        button.classList.add('copied');
        
        setTimeout(() => {
            button.innerHTML = originalHTML;
            button.classList.remove('copied');
        }, 2000);
    }).catch(err => {
        console.error('Failed to copy:', err);
        alert('Failed to copy to clipboard');
    });
}

// ============================================
// UTILITY FUNCTIONS
// ============================================

function clearConversation() {
    if (confirm('Clear conversation history?')) {
        conversationHistory = [];
        chatContainer.innerHTML = `
            <div class="message ai-message">
                <div class="message-content">
                    Welcome! Ask me anything about ${currentTopic.name}.
                </div>
            </div>
        `;
    }
}

function scrollToBottom() {
    chatContainer.scrollTo({
        top: chatContainer.scrollHeight,
        behavior: 'smooth'
    });
}

function getCurrentTime() {
    const now = new Date();
    return now.toLocaleTimeString('en-US', { 
        hour: '2-digit', 
        minute: '2-digit' 
    });
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function formatAnswer(answer) {
    return answer
        .split('\n\n')
        .map(p => `<p>${p.replace(/\n/g, '<br>')}</p>`)
        .join('');
}