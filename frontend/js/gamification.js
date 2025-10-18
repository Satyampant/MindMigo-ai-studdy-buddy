const API_BASE = typeof window.API_BASE !== 'undefined' ? window.API_BASE : 'http://localhost:8000';
const STUDENT_ID = sessionStorage.getItem('student_id') || 'student_' + Math.random().toString(36).substr(2, 9);
if (!sessionStorage.getItem('student_id')) sessionStorage.setItem('student_id', STUDENT_ID);

let gamificationState = {profile: null, leaderboard: null, loading: false};

async function fetchGamificationProfile() {
    gamificationState.loading = true;
    try {
        const response = await fetch(`${API_BASE}/gamification/${STUDENT_ID}`);
        if (!response.ok) throw new Error(`API error: ${response.status}`);
        gamificationState.profile = await response.json();
    } catch (error) {
        console.error('Failed to fetch profile:', error);
        gamificationState.profile = {student_id: STUDENT_ID, total_xp: 0, level: 1, current_streak: 0, longest_streak: 0, last_activity_date: null, badges: [], recent_transactions: [], xp_for_next_level: 100, level_progress_percentage: 0};
    }
    gamificationState.loading = false;
    return gamificationState.profile;
}

async function fetchLeaderboard(limit = 5) {
    try {
        const response = await fetch(`${API_BASE}/leaderboard?limit=${limit}&student_id=${STUDENT_ID}`);
        if (!response.ok) throw new Error(`API error: ${response.status}`);
        gamificationState.leaderboard = await response.json();
    } catch (error) {
        console.error('Failed to fetch leaderboard:', error);
        gamificationState.leaderboard = {entries: [], total_students: 0, current_user_rank: null};
    }
    return gamificationState.leaderboard;
}

async function trackDailyLogin() {
    try {
        await fetch(`${API_BASE}/auth/login?student_id=${STUDENT_ID}`, {method: 'POST'});
    } catch (error) {
        console.error('Failed to track login:', error);
    }
}

async function initGamification() {
    await trackDailyLogin();
    await Promise.all([fetchGamificationProfile(), fetchLeaderboard()]);
    renderGamificationUI();
    setInterval(async () => {
        await fetchGamificationProfile();
        await fetchLeaderboard();
        renderGamificationUI();
    }, 5000);
}

function renderXPProgressBar(profile) {
    const container = document.getElementById('xp-progress-container');
    const progress = profile.level_progress_percentage;
    const xpNeeded = profile.xp_for_next_level;
    container.innerHTML = `<div class="xp-header"><span class="level-badge">Level ${profile.level}</span><span class="xp-text">${profile.total_xp} XP</span></div><div class="progress-bar-container"><div class="progress-bar" style="width: ${progress}%"><span class="progress-text">${Math.round(progress)}%</span></div></div><div class="xp-footer"><span>${xpNeeded} XP to Level ${profile.level + 1}</span></div>`;
}

function renderBadgeShowcase(profile) {
    const container = document.getElementById('badge-showcase');
    const allBadges = ['QUIZ_MASTER', 'QUIZ_LEGEND', 'GRAPH_GURU', 'GRAPH_MASTER', 'STREAK_WARRIOR', 'CONSISTENCY_CHAMP', 'PERFECTIONIST', 'KNOWLEDGE_SEEKER', 'ELITE_LEARNER', 'CHAT_ENTHUSIAST'];
    container.innerHTML = allBadges.map(badgeId => {
        const earned = profile.badges.find(b => b.badge_id === badgeId);
        const locked = !earned;
        return `<div class="badge-card ${locked ? 'locked' : 'earned'}" data-tooltip="${earned ? earned.badge_name + ': ' + earned.description : 'Locked'}"><div class="badge-icon">${locked ? '🔒' : '🏆'}</div><div class="badge-name">${earned ? earned.badge_name : badgeId.replace(/_/g, ' ')}</div></div>`;
    }).join('');
}

function renderStreakCounter(profile) {
    const container = document.getElementById('streak-counter');
    const isActive = profile.current_streak > 0;
    container.innerHTML = `<div class="streak-display ${isActive ? 'active' : ''}"><div class="streak-icon">🔥</div><div class="streak-info"><div class="streak-number">${profile.current_streak}</div><div class="streak-label">Day Streak</div></div></div><div class="streak-best">Best: ${profile.longest_streak} days</div>`;
}

function renderMiniLeaderboard(leaderboard) {
    const container = document.getElementById('mini-leaderboard');
    if (!leaderboard.entries || leaderboard.entries.length === 0) {
        container.innerHTML = `<div class="leaderboard-header"><h3>🏆 Top Students</h3></div><p style="text-align:center;color:#999;padding:20px;">No leaderboard data yet. Complete activities to appear!</p>`;
        return;
    }
    container.innerHTML = `<div class="leaderboard-header"><h3>🏆 Top Students</h3><button onclick="showFullLeaderboard()" class="view-all-btn">View All</button></div><div class="leaderboard-list">${leaderboard.entries.map(entry => `<div class="leaderboard-entry ${entry.is_current_user ? 'current-user' : ''}"><span class="rank">#${entry.rank}</span><span class="name">${entry.display_name}</span><span class="xp">${entry.total_xp} XP</span><span class="level">L${entry.level}</span></div>`).join('')}</div>${leaderboard.current_user_rank ? `<div class="your-rank">Your Rank: #${leaderboard.current_user_rank}</div>` : ''}`;
}

function renderGamificationUI() {
    if (!gamificationState.profile || !gamificationState.leaderboard) return;
    if (gamificationState.profile) renderXPProgressBar(gamificationState.profile);
    if (gamificationState.profile) renderBadgeShowcase(gamificationState.profile);
    if (gamificationState.profile) renderStreakCounter(gamificationState.profile);
    if (gamificationState.leaderboard) renderMiniLeaderboard(gamificationState.leaderboard);
}

async function showFullLeaderboard() {
    try {
        const response = await fetch(`${API_BASE}/leaderboard?limit=50&student_id=${STUDENT_ID}`);
        if (!response.ok) throw new Error(`API error: ${response.status}`);
        const fullLeaderboard = await response.json();
        const modal = document.createElement('div');
        modal.className = 'modal-overlay';
        modal.innerHTML = `<div class="modal-content leaderboard-modal"><div class="modal-header"><h2>🏆 Full Leaderboard</h2><button onclick="this.closest('.modal-overlay').remove()" class="close-btn">✕</button></div><div class="modal-body">${fullLeaderboard.entries.map(entry => `<div class="leaderboard-entry ${entry.is_current_user ? 'current-user' : ''}"><span class="rank">#${entry.rank}</span><span class="name">${entry.display_name}</span><span class="badges">${entry.badge_count} 🏆</span><span class="xp">${entry.total_xp} XP</span><span class="level">Level ${entry.level}</span></div>`).join('')}</div></div>`;
        document.body.appendChild(modal);
    } catch (error) {
        console.error('Failed to load leaderboard:', error);
        if (typeof showToast === 'function') showToast('Failed to load leaderboard', 'error');
    }
}

function showLevelUpAnimation(newLevel) {
    const animation = document.createElement('div');
    animation.className = 'level-up-animation';
    animation.innerHTML = `<div class="level-up-content"><div class="level-up-icon">⭐</div><h1>LEVEL UP!</h1><p>You've reached Level ${newLevel}</p></div>`;
    document.body.appendChild(animation);
    setTimeout(() => animation.remove(), 3000);
}

function showBadgeUnlockAnimation(badge) {
    const animation = document.createElement('div');
    animation.className = 'badge-unlock-animation';
    animation.innerHTML = `<div class="badge-unlock-content"><div class="badge-unlock-icon">🏆</div><h2>Badge Unlocked!</h2><p>${badge.badge_name}</p><small>${badge.description}</small></div>`;
    document.body.appendChild(animation);
    setTimeout(() => animation.remove(), 3000);
}

async function refreshGamification() {
    const oldProfile = gamificationState.profile;
    const oldXP = oldProfile ? oldProfile.total_xp : 0;
    await fetchGamificationProfile();
    await fetchLeaderboard();
    if (oldProfile && gamificationState.profile.total_xp > oldXP) {
        const xpGained = gamificationState.profile.total_xp - oldXP;
        if (typeof notifyXPGain === 'function') notifyXPGain(xpGained);
    }
    if (oldProfile && gamificationState.profile.level > oldProfile.level) {
        if (typeof notifyLevelUp === 'function') notifyLevelUp(gamificationState.profile.level);
        else showLevelUpAnimation(gamificationState.profile.level);
    }
    if (oldProfile) {
        const oldBadges = new Set(oldProfile.badges.map(b => b.badge_id));
        const newBadges = gamificationState.profile.badges.filter(b => !oldBadges.has(b.badge_id));
        newBadges.forEach(badge => {
            if (typeof notifyBadgeUnlock === 'function') notifyBadgeUnlock(badge);
            else showBadgeUnlockAnimation(badge);
        });
    }
    renderGamificationUI();
}
