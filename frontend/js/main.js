// Main application JavaScript - Navigation and initialization

// Navigation management
function navigateToSection(sectionId) {
    // Remove active class from all sections and nav links
    document.querySelectorAll('.section').forEach(section => {
        section.classList.remove('active');
    });
    document.querySelectorAll('.nav-link').forEach(link => {
        link.classList.remove('active');
    });
    
    // Add active class to target section
    const targetSection = document.getElementById(sectionId);
    if (targetSection) {
        targetSection.classList.add('active');
    }
    
    // Add active class to corresponding nav link
    const targetLink = document.querySelector(`.nav-link[data-section="${sectionId}"]`);
    if (targetLink) {
        targetLink.classList.add('active');
    }
    
    // Update URL hash without scrolling
    history.pushState(null, null, `#${sectionId}`);
}

// Initialize navigation
document.addEventListener('DOMContentLoaded', () => {
    // Set up navigation click handlers
    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const sectionId = link.dataset.section;
            navigateToSection(sectionId);
        });
    });
    
    // Brand logo click - navigate to home
    document.querySelector('.nav-brand').addEventListener('click', () => {
        navigateToSection('home');
    });
    
    // Handle initial navigation based on URL hash
    const hash = window.location.hash.substring(1);
    if (hash && document.getElementById(hash)) {
        navigateToSection(hash);
    } else {
        navigateToSection('home');
    }
    
    // Handle browser back/forward buttons
    window.addEventListener('popstate', () => {
        const hash = window.location.hash.substring(1) || 'home';
        navigateToSection(hash);
    });
});

// Check backend connection on load
async function checkBackendConnection() {
    try {
        const response = await fetch(`${CONFIG.API_BASE_URL}/`);
        if (response.ok) {
            console.log('✅ Connected to backend successfully');
        } else {
            console.warn('⚠️ Backend responded with error');
            showToast('warning', 'Backend Warning', 'Backend may not be fully functional');
        }
    } catch (error) {
        console.error('❌ Failed to connect to backend:', error);
        showToast('error', 'Connection Error', 'Cannot connect to backend. Please ensure the server is running.');
    }
}

// Check connection when page loads
document.addEventListener('DOMContentLoaded', () => {
    checkBackendConnection();
});

// Expose navigation function globally for use in HTML
window.navigateToSection = navigateToSection;
