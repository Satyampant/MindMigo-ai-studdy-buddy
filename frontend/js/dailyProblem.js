// Daily Problem functionality

class DailyProblem {
    constructor() {
        this.loadingState = document.getElementById('daily-problem-loading');
        this.contentContainer = document.getElementById('daily-problem-content');
        this.currentProblem = null;
        this.selectedAnswer = null;
        
        this.init();
    }

    init() {
        this.loadDailyProblem();
        this.updateStats();
    }

    async loadDailyProblem() {
        try {
            this.loadingState.style.display = 'flex';
            this.contentContainer.style.display = 'none';
            
            const response = await api.get(CONFIG.ENDPOINTS.DAILY_PROBLEM);
            this.currentProblem = response;
            this.displayProblem(response);
        } catch (error) {
            showToast('error', 'Loading Failed', error.message);
            this.contentContainer.innerHTML = `
                <div class="problem-card">
                    <div class="error-message">
                        <h3>😞 Oops!</h3>
                        <p>Failed to load today's challenge. Please try again later.</p>
                        <button class="btn btn-primary" onclick="dailyProblem.loadDailyProblem()">
                            Retry
                        </button>
                    </div>
                </div>
            `;
            this.contentContainer.style.display = 'block';
        } finally {
            this.loadingState.style.display = 'none';
        }
    }

    displayProblem(problem) {
        const lastDate = getFromStorage(CONFIG.STORAGE_KEYS.LAST_PROBLEM_DATE);
        const alreadySolved = isToday(lastDate);
        
        const html = `
            <div class="problem-card">
                <div class="problem-header">
                    <h3 class="problem-title">Today's Challenge</h3>
                    <span class="problem-difficulty">${escapeHTML(problem.difficulty)}</span>
                </div>
                
                <div class="problem-meta">
                    <span class="quiz-badge">📚 ${escapeHTML(problem.topic)}</span>
                    <span class="quiz-badge">📝 ${escapeHTML(problem.question_type)}</span>
                </div>
                
                <div class="problem-question">
                    ${escapeHTML(problem.question)}
                </div>
                
                <div class="problem-options" id="daily-problem-options">
                    ${problem.options.map((option, index) => `
                        <div class="option-item" data-option="${escapeHTML(option)}" data-index="${index}">
                            <span class="option-letter">${String.fromCharCode(65 + index)}</span>
                            <span class="option-text">${escapeHTML(option)}</span>
                        </div>
                    `).join('')}
                </div>
                
                <div class="problem-actions">
                    <button class="btn btn-primary" id="submit-answer-btn" ${alreadySolved ? 'disabled' : ''}>
                        ${alreadySolved ? '✅ Already Solved Today' : 'Submit Answer'}
                    </button>
                    <button class="btn btn-secondary" id="show-answer-btn">
                        Show Answer
                    </button>
                </div>
                
                <div id="answer-feedback" style="display: none; margin-top: 1.5rem;"></div>
            </div>
        `;
        
        this.contentContainer.innerHTML = html;
        this.contentContainer.style.display = 'block';
        
        this.attachProblemHandlers(alreadySolved);
    }

    attachProblemHandlers(alreadySolved) {
        // Option selection
        const options = document.querySelectorAll('#daily-problem-options .option-item');
        options.forEach(option => {
            option.addEventListener('click', (e) => {
                if (!alreadySolved) {
                    this.handleOptionSelect(e);
                }
            });
        });
        
        // Submit button
        const submitBtn = document.getElementById('submit-answer-btn');
        if (submitBtn && !alreadySolved) {
            submitBtn.addEventListener('click', () => this.handleSubmit());
        }
        
        // Show answer button
        const showAnswerBtn = document.getElementById('show-answer-btn');
        if (showAnswerBtn) {
            showAnswerBtn.addEventListener('click', () => this.showAnswer());
        }
    }

    handleOptionSelect(event) {
        const optionElement = event.currentTarget;
        const allOptions = document.querySelectorAll('#daily-problem-options .option-item');
        
        // Remove previous selection
        allOptions.forEach(opt => opt.classList.remove('selected'));
        
        // Add selection to clicked option
        optionElement.classList.add('selected');
        this.selectedAnswer = optionElement.dataset.option;
    }

    async handleSubmit() {
        if (!this.selectedAnswer) {
            showToast('warning', 'No Selection', 'Please select an answer before submitting');
            return;
        }
        
        const isCorrect = this.selectedAnswer === this.currentProblem.correct_answer;
        const studentId = sessionStorage.getItem('student_id');
        
        try {
            const url = `${CONFIG.ENDPOINTS.DAILY_PROBLEM_SUBMIT}?student_id=${studentId}&is_correct=${isCorrect}`;
            await api.post(url, {});
            if (typeof refreshGamification === 'function') {
                await refreshGamification();
            }
        } catch (error) {
            console.error('Failed to submit daily problem:', error);
        }
        
        this.updateProblemStats(isCorrect);
        this.showFeedback(isCorrect);
        document.getElementById('submit-answer-btn').disabled = true;
        document.getElementById('submit-answer-btn').innerHTML = '✅ Already Solved Today';
        saveToStorage(CONFIG.STORAGE_KEYS.LAST_PROBLEM_DATE, getTodayString());
        this.updateStats();
    }

    showFeedback(isCorrect) {
        const feedbackContainer = document.getElementById('answer-feedback');
        const options = document.querySelectorAll('#daily-problem-options .option-item');
        
        // Highlight correct and wrong answers
        options.forEach(option => {
            if (option.dataset.option === this.currentProblem.correct_answer) {
                option.classList.add('correct');
            } else if (option.classList.contains('selected') && !isCorrect) {
                option.classList.add('wrong');
            }
            option.style.pointerEvents = 'none';
        });
        
        // Show feedback message
        feedbackContainer.style.display = 'block';
        feedbackContainer.innerHTML = `
            <div class="answer-section">
                <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 1rem;">
                    <span style="font-size: 2rem;">${isCorrect ? '🎉' : '😔'}</span>
                    <div>
                        <div style="font-size: 1.25rem; font-weight: 700; color: ${isCorrect ? 'var(--success-color)' : 'var(--error-color)'};">
                            ${isCorrect ? 'Correct!' : 'Incorrect'}
                        </div>
                        <div style="color: var(--text-secondary);">
                            ${isCorrect ? 'Great job! Keep up the streak!' : 'Don\'t worry, try again tomorrow!'}
                        </div>
                    </div>
                </div>
                <div class="answer-label">Correct Answer:</div>
                <div class="answer-text">${escapeHTML(this.currentProblem.correct_answer)}</div>
            </div>
        `;
        
        // Show toast
        if (isCorrect) {
            showToast('success', 'Correct Answer!', 'You solved today\'s challenge!');
        } else {
            showToast('error', 'Incorrect', 'Better luck next time!');
        }
    }

    showAnswer() {
        const feedbackContainer = document.getElementById('answer-feedback');
        const options = document.querySelectorAll('#daily-problem-options .option-item');
        
        // Highlight correct answer
        options.forEach(option => {
            if (option.dataset.option === this.currentProblem.correct_answer) {
                option.classList.add('correct');
            }
        });
        
        feedbackContainer.style.display = 'block';
        feedbackContainer.innerHTML = `
            <div class="answer-section">
                <div class="answer-label">Correct Answer:</div>
                <div class="answer-text">${escapeHTML(this.currentProblem.correct_answer)}</div>
            </div>
        `;
        
        showToast('info', 'Answer Revealed', 'The correct answer is now highlighted');
    }

    updateProblemStats(isCorrect) {
        // Get current stats
        let streak = getFromStorage(CONFIG.STORAGE_KEYS.DAILY_STREAK, 0);
        let solved = getFromStorage(CONFIG.STORAGE_KEYS.PROBLEMS_SOLVED, 0);
        let accuracy = getFromStorage(CONFIG.STORAGE_KEYS.ACCURACY, { correct: 0, total: 0 });
        
        // Update solved count
        solved++;
        
        // Update streak
        const lastDate = getFromStorage(CONFIG.STORAGE_KEYS.LAST_PROBLEM_DATE);
        const yesterday = new Date();
        yesterday.setDate(yesterday.getDate() - 1);
        const yesterdayString = yesterday.toISOString().split('T')[0];
        
        if (isCorrect) {
            if (lastDate === yesterdayString) {
                streak++;
            } else if (!isToday(lastDate)) {
                streak = 1;
            }
        } else {
            streak = 0;
        }
        
        // Update accuracy
        accuracy.total++;
        if (isCorrect) {
            accuracy.correct++;
        }
        
        // Save updated stats
        saveToStorage(CONFIG.STORAGE_KEYS.DAILY_STREAK, streak);
        saveToStorage(CONFIG.STORAGE_KEYS.PROBLEMS_SOLVED, solved);
        saveToStorage(CONFIG.STORAGE_KEYS.ACCURACY, accuracy);
    }

    updateStats() {
        const streak = getFromStorage(CONFIG.STORAGE_KEYS.DAILY_STREAK, 0);
        const solved = getFromStorage(CONFIG.STORAGE_KEYS.PROBLEMS_SOLVED, 0);
        const accuracy = getFromStorage(CONFIG.STORAGE_KEYS.ACCURACY, { correct: 0, total: 0 });
        
        const accuracyRate = accuracy.total > 0 
            ? Math.round((accuracy.correct / accuracy.total) * 100) 
            : 0;
        
        document.getElementById('streak-count').textContent = streak;
        document.getElementById('solved-count').textContent = solved;
        document.getElementById('accuracy-rate').textContent = `${accuracyRate}%`;
    }
}

// Initialize daily problem when DOM is loaded
let dailyProblem;
document.addEventListener('DOMContentLoaded', () => {
    dailyProblem = new DailyProblem();
});
