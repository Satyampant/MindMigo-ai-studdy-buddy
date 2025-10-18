// Chat embed helper - Reloads iframe when navigating to chat section
document.addEventListener('DOMContentLoaded', () => {
    const chatIframe = document.getElementById('chat-iframe');
    const observer = new MutationObserver(() => {
        const aiTutorSection = document.getElementById('ai-tutor');
        if (aiTutorSection && aiTutorSection.classList.contains('active') && chatIframe) {
            // Reload iframe to reset chat state when section becomes active
            chatIframe.src = chatIframe.src;
        }
    });
    
    observer.observe(document.body, { attributes: true, subtree: true, attributeFilter: ['class'] });
});
