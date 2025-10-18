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
    const navBrand = document.querySelector('.nav-brand');
    if (navBrand) {
        navBrand.addEventListener('click', () => {
            navigateToSection('home');
        });
    }
    
    // Hero section CTA buttons
    const heroAITutorBtn = document.getElementById('hero-ai-tutor-btn');
    const heroQuizBtn = document.getElementById('hero-quiz-btn');
    
    if (heroAITutorBtn) {
        heroAITutorBtn.addEventListener('click', () => navigateToSection('ai-tutor'));
    }
    
    if (heroQuizBtn) {
        heroQuizBtn.addEventListener('click', () => navigateToSection('quiz'));
    }
    
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
            const data = await response.json();
            console.log('Backend:', data.message);
        } else {
            console.warn('⚠️ Backend responded with error:', response.status);
            showToast('warning', 'Backend Warning', 'Backend may not be fully functional');
        }
    } catch (error) {
        console.error('❌ Failed to connect to backend:', error);
        showToast('error', 'Backend Not Connected', 'Please start the backend server: uvicorn main:app --reload');
    }
}

// Check connection when page loads
document.addEventListener('DOMContentLoaded', () => {
    setTimeout(() => {
        checkBackendConnection();
    }, 500);
});

// Expose navigation function globally for use in HTML
window.navigateToSection = navigateToSection;
