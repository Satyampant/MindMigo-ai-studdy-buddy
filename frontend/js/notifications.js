// Real-Time Notification System with Animations
const NotificationPreferences = {
    sound: localStorage.getItem('notif_sound') !== 'false',
    animations: localStorage.getItem('notif_animations') !== 'false',
    
    toggle(key) {
        this[key] = !this[key];
        localStorage.setItem(`notif_${key}`, this[key]);
    }
};

// Toast Notification
function showToast(message, type = 'info', duration = 3000) {
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.innerHTML = `<span>${message}</span>`;
    document.body.appendChild(toast);
    setTimeout(() => toast.classList.add('show'), 10);
    setTimeout(() => { toast.classList.remove('show'); setTimeout(() => toast.remove(), 300); }, duration);
}

// Floating XP Animation
function showXPGain(amount, element = document.body) {
    const xpFloat = document.createElement('div');
    xpFloat.className = 'xp-float';
    xpFloat.textContent = `+${amount} XP`;
    xpFloat.style.left = `${Math.random() * 80 + 10}%`;
    element.appendChild(xpFloat);
    if (NotificationPreferences.sound) playSound('xp');
    setTimeout(() => xpFloat.remove(), 2000);
}

// Level Up Modal
function showLevelUpModal(newLevel) {
    const modal = document.createElement('div');
    modal.className = 'notif-modal level-up-modal';
    modal.innerHTML = `
        <div class="modal-backdrop"></div>
        <div class="modal-card">
            <div class="level-icon">⭐</div>
            <h1 class="level-title">LEVEL UP!</h1>
            <p class="level-number">Level ${newLevel}</p>
            <button onclick="this.closest('.notif-modal').remove()" class="modal-btn">Awesome!</button>
        </div>
    `;
    document.body.appendChild(modal);
    if (NotificationPreferences.sound) playSound('levelup');
    if (NotificationPreferences.animations) triggerConfetti();
}

// Badge Unlock Modal
function showBadgeUnlockModal(badge) {
    const modal = document.createElement('div');
    modal.className = 'notif-modal badge-unlock-modal';
    modal.innerHTML = `
        <div class="modal-backdrop"></div>
        <div class="modal-card">
            <div class="badge-icon-large">🏆</div>
            <h2 class="badge-title">Badge Unlocked!</h2>
            <p class="badge-name">${badge.badge_name}</p>
            <p class="badge-desc">${badge.description}</p>
            <button onclick="this.closest('.notif-modal').remove()" class="modal-btn">Collect</button>
        </div>
    `;
    document.body.appendChild(modal);
    if (NotificationPreferences.sound) playSound('badge');
    if (NotificationPreferences.animations) triggerConfetti();
}

// Confetti Effect
function triggerConfetti() {
    const duration = 3000, colors = ['#667eea', '#764ba2', '#ffeaa7', '#fdcb6e', '#ff6b6b'];
    const end = Date.now() + duration;
    (function frame() {
        if (Date.now() < end) {
            const x = Math.random(), y = Math.random() * 0.5;
            createConfettiPiece(x, y, colors[Math.floor(Math.random() * colors.length)]);
            requestAnimationFrame(frame);
        }
    })();
}

function createConfettiPiece(x, y, color) {
    const piece = document.createElement('div');
    piece.className = 'confetti';
    piece.style.left = `${x * 100}%`;
    piece.style.top = `${y * 100}%`;
    piece.style.background = color;
    document.body.appendChild(piece);
    setTimeout(() => piece.remove(), 3000);
}

// Sound Effects
const sounds = { xp: 440, levelup: [523, 659, 784], badge: [659, 784, 880, 1047] };
function playSound(type) {
    const ctx = new (window.AudioContext || window.webkitAudioContext)();
    const frequencies = Array.isArray(sounds[type]) ? sounds[type] : [sounds[type]];
    frequencies.forEach((freq, i) => {
        const osc = ctx.createOscillator(), gain = ctx.createGain();
        osc.connect(gain); gain.connect(ctx.destination);
        osc.frequency.value = freq; osc.type = 'sine';
        gain.gain.setValueAtTime(0.1, ctx.currentTime + i * 0.1);
        gain.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + i * 0.1 + 0.3);
        osc.start(ctx.currentTime + i * 0.1); osc.stop(ctx.currentTime + i * 0.1 + 0.3);
    });
}

// Notification Preferences Toggle UI
function createPreferencesToggle() {
    const toggle = document.createElement('div');
    toggle.className = 'notif-preferences';
    toggle.innerHTML = `
        <button onclick="NotificationPreferences.toggle('sound'); this.textContent = NotificationPreferences.sound ? '🔊' : '🔇'" 
                title="Toggle sound">${NotificationPreferences.sound ? '🔊' : '🔇'}</button>
        <button onclick="NotificationPreferences.toggle('animations'); this.textContent = NotificationPreferences.animations ? '✨' : '⭕'" 
                title="Toggle animations">${NotificationPreferences.animations ? '✨' : '⭕'}</button>
    `;
    document.body.appendChild(toggle);
}

// Auto-detect and trigger notifications from gamification events
function initNotificationSystem() {
    createPreferencesToggle();
    
    // Listen for custom events
    window.addEventListener('xp-gained', (e) => showXPGain(e.detail.amount));
    window.addEventListener('level-up', (e) => showLevelUpModal(e.detail.level));
    window.addEventListener('badge-unlocked', (e) => showBadgeUnlockModal(e.detail.badge));
}

// Trigger custom events (call these from your app)
function notifyXPGain(amount) { window.dispatchEvent(new CustomEvent('xp-gained', { detail: { amount } })); }
function notifyLevelUp(level) { window.dispatchEvent(new CustomEvent('level-up', { detail: { level } })); }
function notifyBadgeUnlock(badge) { window.dispatchEvent(new CustomEvent('badge-unlocked', { detail: { badge } })); }
