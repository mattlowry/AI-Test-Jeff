/**
 * Eleven Labs RAG Widget Integration
 * This script integrates with Eleven Labs' API to provide a RAG-powered conversational AI experience.
 * It handles user queries, retrieves relevant information from site content, and generates responses.
 */

class ElevenLabsRAGWidget {
    constructor(options = {}) {
        // Configuration options with defaults
        this.config = {
            apiKey: options.apiKey || null,
            modelId: options.modelId || 'eleven-beta',
            apiEndpoint: options.apiEndpoint || 'https://api.elevenlabs.io/v1/chat',
            maxTokens: options.maxTokens || 2048,
            temperature: options.temperature || 0.7,
            chatContainerId: options.chatContainerId || 'chat-messages',
            messageInputId: options.messageInputId || 'message-input',
            sendButtonId: options.sendButtonId || 'send-button',
            ...options
        };

        // Elements
        this.chatContainer = document.getElementById(this.config.chatContainerId);
        this.messageInput = document.getElementById(this.config.messageInputId);
        this.sendButton = document.getElementById(this.config.sendButtonId);

        // Chat history
        this.chatHistory = [];

        // Bind events
        this.bindEvents();

        // Initialize - if we have an API key
        if (this.config.apiKey) {
            this.initialized = true;
            console.log('Eleven Labs RAG Widget initialized with API key');
        } else {
            // Demo mode
            this.initialized = false;
            console.log('Eleven Labs RAG Widget initialized in demo mode - no API key provided');
        }
    }

    bindEvents() {
        // Send button click event
        this.sendButton.addEventListener('click', () => this.sendMessage());

        // Enter key press event
        this.messageInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });

        // Auto-resize textarea
        this.messageInput.addEventListener('input', function() {
            this.style.height = 'auto';
            this.style.height = (this.scrollHeight) + 'px';
        });
    }

    async sendMessage() {
        const message = this.messageInput.value.trim();
        if (message === '') return;

        // Add user message to UI
        this.addUserMessage(message);
        this.messageInput.value = '';
        this.messageInput.style.height = 'auto';

        // Add to history
        this.chatHistory.push({
            role: 'user',
            content: message
        });

        // Show typing indicator
        const typingIndicator = this.showTypingIndicator();

        try {
            if (this.initialized) {
                // Real API call
                const response = await this.callElevenLabsAPI(message);
                typingIndicator.remove();
                this.addBotMessage(response);
            } else {
                // Demo mode - simulate response
                setTimeout(() => {
                    typingIndicator.remove();
                    const demoResponse = this.getDemoResponse(message);
                    this.addBotMessage(demoResponse);
                }, Math.random() * 2000 + 1000);
            }
        } catch (error) {
            typingIndicator.remove();
            this.addErrorMessage("I apologize, but I'm having trouble generating a response. Please try again later.");
            console.error('Eleven Labs API Error:', error);
        }
    }

    async callElevenLabsAPI(message) {
        // This would be the actual API call in production
        const response = await fetch(this.config.apiEndpoint, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'xi-api-key': this.config.apiKey
            },
            body: JSON.stringify({
                model_id: this.config.modelId,
                messages: this.chatHistory,
                max_tokens: this.config.maxTokens,
                temperature: this.config.temperature
            })
        });

        if (!response.ok) {
            throw new Error(`API call failed with status: ${response.status}`);
        }

        const data = await response.json();
        const botResponse = data.message.content;

        // Add to history
        this.chatHistory.push({
            role: 'assistant',
            content: botResponse
        });

        return botResponse;
    }

    getDemoResponse(message) {
        // Demo responses based on website content
        const responses = [
            "Based on our forecast, AI will achieve human-level performance across most cognitive tasks by 2029-2030. This includes abstract reasoning, creative production, strategic planning, and social understanding.",
            "According to Elon Musk, AGI could emerge as soon as 2025, fundamentally altering the balance of power between humans and machines. This existential risk concern is shared by several experts in the field.",
            "By 2026, AI tutoring systems will become mainstream supplementary education tools, with evidence showing significant improvements in learning outcomes across diverse student populations.",
            "Industry transformation due to AI will be particularly profound in healthcare, with AI being responsible for primary diagnosis in at least 30% of radiological exams by 2027.",
            "According to our timeline, cross-domain synthesis will be a major capability development by 2028, allowing AI to transfer knowledge between domains and solve complex interdisciplinary problems.",
            "In the creative industries, by 2026, most commercial digital content will involve AI at some stage of production, with new roles emerging for 'AI directors' who specialize in guiding creative AI systems.",
            "The Model3 architecture, as detailed on our models page, integrates specialized attention mechanisms with sparse computation, significantly enhancing both capabilities and computational efficiency.",
            "Privacy experts like Edward Snowden warn that by 2025, AI-powered surveillance could make privacy essentially obsolete, with every move logged, analyzed, and potentially judged.",
            "According to our forecasts, by 2028, knowledge workers across industries will spend more time directing and refining AI outputs than creating content from scratch, fundamentally changing productivity benchmarks.",
            "The AgentSGEN system uses a dual-agent architecture with Evaluator and Editor roles to create more reliable and safe AI outputs, particularly important for mission-critical applications."
        ];

        // Find a somewhat relevant response by checking for keywords
        const lowerMessage = message.toLowerCase();
        const keywordMap = {
            'timeline': [0, 4],
            'future': [0, 4, 8],
            'risk': [1, 7],
            'musk': [1],
            'elon': [1],
            'education': [2],
            'tutor': [2],
            'learn': [2],
            'health': [3],
            'medical': [3],
            'doctor': [3],
            'cross-domain': [4],
            'synthesis': [4],
            'creative': [5],
            'content': [5],
            'design': [5],
            'model': [6],
            'architecture': [6],
            'privacy': [7],
            'surveillance': [7],
            'snowden': [7],
            'worker': [8],
            'job': [8],
            'work': [8],
            'agent': [9],
            'agentsgen': [9],
            'safety': [9]
        };

        // Check for matching keywords
        let possibleResponses = [];
        for (const [keyword, indices] of Object.entries(keywordMap)) {
            if (lowerMessage.includes(keyword)) {
                possibleResponses = [...possibleResponses, ...indices];
            }
        }

        // If we found matches, use them, otherwise pick random
        let responseIndex;
        if (possibleResponses.length > 0) {
            responseIndex = possibleResponses[Math.floor(Math.random() * possibleResponses.length)];
        } else {
            responseIndex = Math.floor(Math.random() * responses.length);
        }

        const response = responses[responseIndex];

        // Add to history for context (in a real implementation)
        this.chatHistory.push({
            role: 'assistant',
            content: response
        });

        return response;
    }

    addUserMessage(message) {
        const messageElement = document.createElement('div');
        messageElement.classList.add('message', 'user-message');
        
        // Process message for markdown-like formatting
        let formattedMessage = this.formatMessage(message);
        messageElement.innerHTML = formattedMessage;
        
        this.chatContainer.appendChild(messageElement);
        this.scrollToBottom();
    }

    addBotMessage(message) {
        const messageElement = document.createElement('div');
        messageElement.classList.add('message', 'bot-message');
        
        // Process message for markdown-like formatting
        let formattedMessage = this.formatMessage(message);
        messageElement.innerHTML = formattedMessage;
        
        this.chatContainer.appendChild(messageElement);
        this.scrollToBottom();
    }

    addErrorMessage(message) {
        const messageElement = document.createElement('div');
        messageElement.classList.add('message', 'bot-message', 'error-message');
        messageElement.textContent = message;
        this.chatContainer.appendChild(messageElement);
        this.scrollToBottom();
    }

    formatMessage(message) {
        // Basic markdown-like formatting
        // Code blocks
        message = message.replace(/```([\s\S]*?)```/g, '<pre>$1</pre>');
        
        // Inline code
        message = message.replace(/`([^`]+)`/g, '<code>$1</code>');
        
        // Bold
        message = message.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
        
        // Italic
        message = message.replace(/\*([^*]+)\*/g, '<em>$1</em>');
        
        // Line breaks
        message = message.replace(/\n/g, '<br>');
        
        return message;
    }

    showTypingIndicator() {
        const indicator = document.createElement('div');
        indicator.classList.add('typing-indicator');
        indicator.innerHTML = '<div class="typing-dot"></div><div class="typing-dot"></div><div class="typing-dot"></div>';
        this.chatContainer.appendChild(indicator);
        this.scrollToBottom();
        return indicator;
    }

    scrollToBottom() {
        this.chatContainer.scrollTop = this.chatContainer.scrollHeight;
    }

    // Method to set API key at runtime
    setApiKey(apiKey) {
        this.config.apiKey = apiKey;
        this.initialized = true;
        console.log('API key set, switching to live mode');
    }
}

// Initialize on DOM ready
document.addEventListener('DOMContentLoaded', function() {
    // Create global instance
    window.elevenLabsWidget = new ElevenLabsRAGWidget({
        // Configuration options
        // apiKey would be set in production: apiKey: 'YOUR_API_KEY'
        temperature: 0.8,
        maxTokens: 2048
    });
});