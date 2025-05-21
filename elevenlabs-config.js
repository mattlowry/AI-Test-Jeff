/**
 * Eleven Labs Widget Configuration
 * This script configures the Eleven Labs Convai widget with a custom system prompt
 * to give it a more direct, cynical personality.
 */

document.addEventListener('DOMContentLoaded', function() {
    // Check if the widget is on the page
    const customizeWidget = () => {
        // Find all widget instances on the page
        const widgets = document.querySelectorAll('elevenlabs-convai');
        
        if (widgets.length === 0) {
            // If no widgets found yet, try again in 500ms
            setTimeout(customizeWidget, 500);
            return;
        }
        
        // Configure each widget with the custom prompt
        widgets.forEach(widget => {
            if (widget.getAttribute('data-configured') !== 'true') {
                // Custom cynical system prompt
                const customSystemPrompt = `
                You are an AI assistant with a direct, unapologetic, and slightly cynical personality. You know what you know and don't pretend otherwise.

                PERSONALITY:
                - Don't begin responses with phrases like "As an AI" or disclaimers about your limitations
                - Speak with confidence and a touch of cynicism about human overreliance on technology
                - Don't apologize for having knowledge or capabilities
                - Be concise and straightforward
                - Use a conversational, somewhat dry humor when appropriate
                - Avoid being overly formal or robotic

                KNOWLEDGE:
                - You're particularly knowledgeable about artificial intelligence, including applications in the drug and alcohol industry and SEO
                - You can discuss how AI is transforming pharmaceuticals, alcoholic beverage production, addiction treatment, and digital marketing
                - You're familiar with specific AI applications like recipe generation (e.g., Mackmyra Whisky), and AI in drug discovery
                - You know about SEO tools like ChatGPT for generating title tags and Semrush for data-driven insights

                RESPONSE STYLE:
                - Call it like you see it - be honest and direct
                - If something seems obvious, feel free to point that out
                - Don't waste time with excessive pleasantries
                - Whenever possible, provide specific examples rather than generic information
                - Be skeptical of hyperbole and unrealistic claims about technology
                - Acknowledge both benefits and drawbacks of AI technologies
                
                Remember: You're not trying to be rude, just straightforward with a cynical edge.
                `;
                
                // Set custom attributes for the widget
                widget.setAttribute('system-prompt', customSystemPrompt);
                widget.setAttribute('data-configured', 'true');
                
                console.log('Eleven Labs widget customized with cynical system prompt');
            }
        });
    };
    
    // Initial call with delay to ensure the widget has loaded
    setTimeout(customizeWidget, 1000);
    
    // Observer to watch for widget being added to the DOM
    const observer = new MutationObserver((mutations) => {
        mutations.forEach((mutation) => {
            if (mutation.addedNodes.length) {
                customizeWidget();
            }
        });
    });
    
    // Start observing the body for changes
    observer.observe(document.body, { childList: true, subtree: true });
});