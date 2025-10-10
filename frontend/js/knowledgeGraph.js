// Knowledge Graph Generator functionality

class KnowledgeGraphGenerator {
    constructor() {
        this.form = document.getElementById('kg-form');
        this.resultsContainer = document.getElementById('kg-results');
        this.placeholder = document.getElementById('kg-placeholder');
        this.generateButton = document.getElementById('generate-kg-btn');
        this.iframeContainer = document.getElementById('kg-iframe-container');
        this.currentInputType = 'topic';
        
        this.init();
    }

    init() {
        // Form submission handler
        this.form.addEventListener('submit', (e) => this.handleSubmit(e));
        
        // Toggle between topic and text input
        const toggleButtons = document.querySelectorAll('.toggle-btn');
        toggleButtons.forEach(btn => {
            btn.addEventListener('click', (e) => this.handleToggle(e));
        });
    }

    handleToggle(event) {
        const button = event.currentTarget;
        const type = button.dataset.type;
        
        // Update active state
        document.querySelectorAll('.toggle-btn').forEach(btn => {
            btn.classList.remove('active');
        });
        button.classList.add('active');
        
        // Show/hide input groups
        if (type === 'topic') {
            document.getElementById('topic-input-group').style.display = 'flex';
            document.getElementById('text-input-group').style.display = 'none';
            this.currentInputType = 'topic';
        } else {
            document.getElementById('topic-input-group').style.display = 'none';
            document.getElementById('text-input-group').style.display = 'flex';
            this.currentInputType = 'text';
        }
    }

    async handleSubmit(event) {
        event.preventDefault();
        
        const requestData = {};
        
        if (this.currentInputType === 'topic') {
            const topic = document.getElementById('kg-topic').value.trim();
            if (!topic) {
                showToast('warning', 'Input Required', 'Please enter a topic');
                return;
            }
            requestData.topic = topic;
        } else {
            const text = document.getElementById('kg-text').value.trim();
            if (!text) {
                showToast('warning', 'Input Required', 'Please enter some text');
                return;
            }
            requestData.text = text;
        }

        setButtonLoading(this.generateButton, true);

        try {
            const response = await api.post(CONFIG.ENDPOINTS.KNOWLEDGE_GRAPH_GENERATE, requestData);
            this.displayGraph(response);
            showToast('success', 'Graph Generated!', 'Knowledge graph created successfully');
        } catch (error) {
            showToast('error', 'Generation Failed', error.message);
            console.error('Knowledge Graph Error:', error);
        } finally {
            setButtonLoading(this.generateButton, false);
        }
    }

    displayGraph(response) {
        this.placeholder.style.display = 'none';
        this.resultsContainer.style.display = 'block';
        
        // Clear previous content
        this.iframeContainer.innerHTML = '';
        
        // Decode base64 HTML if needed
        let htmlContent = response.html_content;
        
        if (response.encoding === 'base64') {
            htmlContent = decodeBase64HTML(htmlContent);
            if (!htmlContent) {
                showToast('error', 'Display Error', 'Failed to decode graph content');
                return;
            }
        }
        
        // Create and append iframe
        const iframe = createIframe(htmlContent);
        this.iframeContainer.appendChild(iframe);
    }
}

// Global function for fullscreen modal
function openGraphFullscreen() {
    const modal = document.getElementById('graph-modal');
    const modalContent = document.getElementById('graph-modal-content');
    const iframeContainer = document.getElementById('kg-iframe-container');
    
    // Clone the iframe to the modal
    const iframe = iframeContainer.querySelector('iframe');
    if (iframe) {
        const clonedIframe = iframe.cloneNode(true);
        modalContent.innerHTML = '';
        modalContent.appendChild(clonedIframe);
        modal.classList.add('active');
    }
}

function closeGraphModal() {
    const modal = document.getElementById('graph-modal');
    modal.classList.remove('active');
}

// Close modal on outside click
window.addEventListener('click', (event) => {
    const modal = document.getElementById('graph-modal');
    if (event.target === modal) {
        closeGraphModal();
    }
});

// Initialize knowledge graph generator when DOM is loaded
let kgGenerator;
document.addEventListener('DOMContentLoaded', () => {
    kgGenerator = new KnowledgeGraphGenerator();
});
