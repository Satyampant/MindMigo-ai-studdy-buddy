// Diagnostic Test Script for Studdy Buddy AI
// Run this in the browser console to check all systems

console.log('🔍 Starting Studdy Buddy AI Diagnostics...\n');

// Test 1: Check if CONFIG is defined
console.log('1️⃣ Testing CONFIG...');
if (typeof CONFIG !== 'undefined') {
    console.log('✅ CONFIG found:', CONFIG);
} else {
    console.error('❌ CONFIG not found! Check if config.js is loaded');
}

// Test 2: Check API connectivity
console.log('\n2️⃣ Testing API connectivity...');
if (typeof api !== 'undefined') {
    console.log('✅ API object found');
    api.get('/')
        .then(data => console.log('✅ Backend connected:', data))
        .catch(err => console.error('❌ Backend connection failed:', err));
} else {
    console.error('❌ API object not found! Check if api.js is loaded');
}

// Test 3: Check utility functions
console.log('\n3️⃣ Testing utility functions...');
const utilFunctions = ['showToast', 'setButtonLoading', 'escapeHTML', 'getTodayString'];
utilFunctions.forEach(fn => {
    if (typeof window[fn] === 'function') {
        console.log(`✅ ${fn} available`);
    } else {
        console.error(`❌ ${fn} not available`);
    }
});

// Test 4: Check feature modules
console.log('\n4️⃣ Testing feature modules...');
const modules = {
    'quizGenerator': 'Quiz Generator',
    'dailyProblem': 'Daily Problem',
    'gamificationState': 'Gamification',
};

Object.entries(modules).forEach(([obj, name]) => {
    if (typeof window[obj] !== 'undefined') {
        console.log(`✅ ${name} module loaded`);
    } else {
        console.error(`❌ ${name} module not loaded`);
    }
});

// Test 5: Check gamification functions
console.log('\n5️⃣ Testing gamification functions...');
const gamFunctions = ['initGamification', 'fetchGamificationProfile', 'renderGamificationUI'];
gamFunctions.forEach(fn => {
    if (typeof window[fn] === 'function') {
        console.log(`✅ ${fn} available`);
    } else {
        console.error(`❌ ${fn} not available`);
    }
});

// Test 6: Check notification functions
console.log('\n6️⃣ Testing notification functions...');
const notifFunctions = ['initNotificationSystem', 'showToast', 'notifyXPGain'];
notifFunctions.forEach(fn => {
    if (typeof window[fn] === 'function') {
        console.log(`✅ ${fn} available`);
    } else {
        console.error(`❌ ${fn} not available`);
    }
});

// Test 7: Check DOM elements
console.log('\n7️⃣ Testing critical DOM elements...');
const elements = [
    'quiz-form',
    'daily-problem-loading',
    'progress-dashboard',
    'xp-progress-container',
    'toast-container'
];

elements.forEach(id => {
    if (document.getElementById(id)) {
        console.log(`✅ Element #${id} found`);
    } else {
        console.error(`❌ Element #${id} not found`);
    }
});

// Test 8: Test each endpoint
console.log('\n8️⃣ Testing API endpoints...');
const endpoints = [
    { name: 'Root', path: '/' },
    { name: 'Daily Problem', path: '/daily-problem' },
    { name: 'Gamification Profile', path: '/gamification/student_123' },
    { name: 'Leaderboard', path: '/leaderboard' }
];

endpoints.forEach(async ({ name, path }) => {
    try {
        const response = await fetch(CONFIG.API_BASE_URL + path);
        if (response.ok) {
            console.log(`✅ ${name} endpoint working`);
        } else {
            console.warn(`⚠️ ${name} endpoint returned ${response.status}`);
        }
    } catch (error) {
        console.error(`❌ ${name} endpoint failed:`, error.message);
    }
});

console.log('\n✅ Diagnostics complete! Check results above.');
