// Progress Dashboard functionality

let weeklyChart = null;
let radarChart = null;

async function loadProgressDashboard() {
    const studentId = document.getElementById('student-id').value.trim();
    if (!studentId) {
        showToast('error', 'Error', 'Please enter a student ID');
        return;
    }

    const loading = document.getElementById('progress-loading');
    const dashboard = document.getElementById('progress-dashboard');
    
    loading.style.display = 'flex';
    dashboard.style.display = 'none';

    try {
        const response = await api.get(`${CONFIG.ENDPOINTS.PROGRESS_ANALYTICS_AI}/${studentId}/ai`);
        displayAnalytics(response);
        dashboard.style.display = 'block';
        showToast('success', 'Success', 'AI-powered insights loaded!');
    } catch (error) {
        showToast('error', 'Error', error.message || 'Failed to load progress');
    } finally {
        loading.style.display = 'none';
    }
}

function displayAnalytics(data) {
    document.getElementById('overall-accuracy').textContent = `${data.overall_accuracy}%`;
    document.getElementById('total-attempts').textContent = `${data.total_attempts} quizzes taken`;
    document.getElementById('strongest-topic').textContent = data.strongest_topic;
    document.getElementById('weakest-topic').textContent = data.weakest_topic;
    
    generateFeedback(data);
    renderWeeklyChart(data.weekly_trend);
    renderRadarChart(data.topics);
    renderDifficultyBars(data.difficulty_distribution);
}

function generateFeedback(data) {
    const strengthFeedback = data.ai_strength_feedback || 
        (data.strongest_topic !== 'N/A' 
            ? `You're excelling in ${data.strongest_topic}! Your strong performance shows great understanding. Keep up the excellent work and consider helping peers in this area.`
            : 'Complete some quizzes to see your strengths!');
    
    const weaknessFeedback = data.ai_weakness_feedback ||
        (data.weakest_topic !== 'N/A'
            ? `Focus on ${data.weakest_topic} to improve your overall performance. Try reviewing fundamental concepts and practicing with easier questions first before advancing.`
            : 'Your progress data will appear here after completing quizzes.');
    
    document.getElementById('strength-feedback').textContent = strengthFeedback;
    document.getElementById('weakness-feedback').textContent = weaknessFeedback;
}

function renderWeeklyChart(weeklyData) {
    const ctx = document.getElementById('weeklyTrendChart');
    if (weeklyChart) weeklyChart.destroy();
    
    const labels = weeklyData.map(d => new Date(d.date).toLocaleDateString('en-US', {month: 'short', day: 'numeric'}));
    const accuracies = weeklyData.map(d => d.accuracy);
    
    weeklyChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Accuracy %',
                data: accuracies,
                borderColor: '#667eea',
                backgroundColor: 'rgba(102, 126, 234, 0.1)',
                tension: 0.4,
                fill: true,
                pointRadius: 5,
                pointHoverRadius: 7
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {display: false},
                tooltip: {
                    callbacks: {
                        label: (context) => `Accuracy: ${context.parsed.y}%`
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100,
                    ticks: {callback: (value) => value + '%'}
                }
            }
        }
    });
}

function renderRadarChart(topics) {
    const ctx = document.getElementById('topicRadarChart');
    if (radarChart) radarChart.destroy();
    
    const labels = topics.map(t => t.topic);
    const accuracies = topics.map(t => t.accuracy);
    
    radarChart = new Chart(ctx, {
        type: 'radar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Accuracy',
                data: accuracies,
                backgroundColor: 'rgba(102, 126, 234, 0.2)',
                borderColor: '#667eea',
                pointBackgroundColor: '#667eea',
                pointBorderColor: '#fff',
                pointHoverBackgroundColor: '#fff',
                pointHoverBorderColor: '#667eea'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            scales: {
                r: {
                    beginAtZero: true,
                    max: 100,
                    ticks: {callback: (value) => value + '%'}
                }
            },
            plugins: {
                legend: {display: false}
            }
        }
    });
}

function renderDifficultyBars(distribution) {
    const container = document.getElementById('difficulty-bars');
    const total = Object.values(distribution).reduce((a, b) => a + b, 0) || 1;
    
    const levels = [
        {name: 'easy', label: 'Easy', color: 'easy'},
        {name: 'medium', label: 'Medium', color: 'medium'},
        {name: 'hard', label: 'Hard', color: 'hard'}
    ];
    
    container.innerHTML = levels.map(level => {
        const count = distribution[level.name] || 0;
        const percentage = (count / total * 100).toFixed(1);
        
        return `
            <div class="difficulty-bar">
                <div class="difficulty-bar-header">
                    <span class="difficulty-name">${level.label}</span>
                    <span class="difficulty-count">${count} quizzes</span>
                </div>
                <div class="difficulty-bar-fill-container">
                    <div class="difficulty-bar-fill ${level.color}" style="width: ${percentage}%"></div>
                </div>
            </div>
        `;
    }).join('');
}
