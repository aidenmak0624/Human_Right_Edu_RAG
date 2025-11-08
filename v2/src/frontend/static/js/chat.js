// ============================================
// CONVERSATION HISTORY IMPLEMENTATION
// ============================================

// Global state
let conversationHistory = [];

// Display user message
function displayUserMessage(message) {
    const userDiv = document.createElement('div');
    userDiv.className = 'message user-message';
    userDiv.innerHTML = `
        <div class="message-content">${escapeHtml(message)}</div>
        <div class="message-time">${getCurrentTime()}</div>
    `;
    chatContainer.appendChild(userDiv);
    
    // Store in history
    conversationHistory.push({
        role: 'user',
        content: message,
        timestamp: new Date()
    });
    
    scrollToBottom();
}

// Display AI message
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
    
    // Store in history
    conversationHistory.push({
        role: 'assistant',
        content: answer,
        sources: sources,
        timestamp: new Date()
    });
    
    scrollToBottom();
}

// Display loading indicator
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

// Utility functions
function scrollToBottom() {
    chatContainer.scrollTop = chatContainer.scrollHeight;
    // Smooth scroll
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
    // Convert newlines to <br>, preserve paragraphs
    return answer
        .split('\n\n')
        .map(p => `<p>${p.replace(/\n/g, '<br>')}</p>`)
        .join('');
}

// Clear conversation
function clearConversation() {
    if (confirm('Clear conversation history?')) {
        conversationHistory = [];
        chatContainer.innerHTML = `
            <div class="welcome-message">
                Welcome! Ask me anything about ${currentTopic}.
            </div>
        `;
    }
}

// ============================================
// COPY FUNCTIONALITY
// ============================================

function copyToClipboard(button) {
    // Get the answer content (not sources)
    const messageDiv = button.closest('.ai-message');
    const contentDiv = messageDiv.querySelector('.message-content');
    const text = contentDiv.innerText;
    
    // Copy to clipboard
    navigator.clipboard.writeText(text).then(() => {
        // Visual feedback
        const icon = button.querySelector('.icon');
        const originalText = button.innerHTML;
        
        button.innerHTML = '<span class="icon">✅</span> Copied!';
        button.classList.add('copied');
        
        setTimeout(() => {
            button.innerHTML = originalText;
            button.classList.remove('copied');
        }, 2000);
    }).catch(err => {
        console.error('Failed to copy:', err);
        alert('Failed to copy to clipboard');
    });
}

// ============================================
// ENHANCED SOURCE DISPLAY
// ============================================

function createSourcesHTML(sources) {
    if (!sources || sources.length === 0) {
        return '';
    }
    
    const sourceBadges = sources.map(source => {
        // Parse "filename.txt (score=0.234)"
        const match = source.match(/(.+?)\s*\(score=([\d.]+)\)/);
        
        if (match) {
            const [_, filename, scoreStr] = match;
            const score = parseFloat(scoreStr);
            
            // Convert distance to relevance percentage
            // Lower distance = higher relevance
            const relevancePercent = Math.max(0, Math.min(100, (1 - score) * 100)).toFixed(0);
            
            // Color based on relevance
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
    if (percent >= 80) return '#28a745'; // Green
    if (percent >= 60) return '#17a2b8'; // Blue
    if (percent >= 40) return '#ffc107'; // Yellow
    return '#dc3545'; // Red
}

// ============================================
// ERROR HANDLING
// ============================================

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

// Update your API call error handling:
async function sendMessage(query, topic) {
    try {
        displayUserMessage(query);
        showLoadingIndicator();
        
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ query, topic, difficulty: 'intermediate' })
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
        displayError(
            'Failed to get response. Please check your connection and try again.'
        );
    }
}

// ============================================
// KEYBOARD SHORTCUTS
// ============================================

// Add to your input field initialization:
const messageInput = document.getElementById('message-input');

messageInput.addEventListener('keydown', (e) => {
    // Enter to send (Shift+Enter for new line)
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        const sendBtn = document.getElementById('send-btn');
        if (sendBtn) sendBtn.click();
    }
});

// Focus input when page loads
window.addEventListener('load', () => {
    messageInput.focus();
});

// Re-focus input after sending message
function sendMessageAndRefocus() {
    // ... your send logic ...
    messageInput.value = '';
    messageInput.focus();
}