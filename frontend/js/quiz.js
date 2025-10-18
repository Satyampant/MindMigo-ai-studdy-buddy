// Quiz Generator functionality with Progress Tracking

class QuizGenerator {
    constructor() {
        this.form = document.getElementById('quiz-form');
        this.resultsContainer = document.getElementById('quiz-results');
        this.placeholder = document.getElementById('quiz-placeholder');
        this.generateButton = document.getElementById('generate-quiz-btn');
        this.currentQuiz = null;
        this.currentSettings = null;
        this.studentId = sessionStorage.getItem('student_id') || 'student_' + Math.random().toString(36).substr(2, 9);
        if (!sessionStorage.getItem('student_id')) sessionStorage.setItem('student_id', this.studentId);
        
        this.init();
    }

    init() {
        this.form.addEventListener('submit', (e) => this.handleSubmit(e));
        
        const rangeInput = document.getElementById('num-questions');
        const rangeDisplay = document.getElementById('num-display');
        rangeInput.addEventListener('input', (e) => {
            rangeDisplay.textContent = e.target.value;
        });
    }

    async handleSubmit(event) {
        event.preventDefault();
        
        const difficultyRadio = document.querySelector('input[name="difficulty"]:checked');
        const settings = {
            topic: document.getElementById('quiz-topic').value,
            question_type: document.getElementById('question-type').value,
            difficulty: difficultyRadio ? difficultyRadio.value : 'medium',
            num_questions: parseInt(document.getElementById('num-questions').value)
        };

        setButtonLoading(this.generateButton, true);

        try {
            const response = await api.post(CONFIG.ENDPOINTS.QUIZ_GENERATE, settings);
            this.currentQuiz = response;
            this.currentSettings = settings;
            this.displayQuiz(response, settings);
            showToast('success', 'Quiz Generated!', `Successfully created ${response.questions.length} questions`);
        } catch (error) {
            showToast('error', 'Generation Failed', error.message);
        } finally {
            setButtonLoading(this.generateButton, false);
        }
    }

    displayQuiz(quizData, settings) {
        this.placeholder.style.display = 'none';
        this.resultsContainer.style.display = 'block';
        
        const html = `
            <div class="quiz-header">
                <div class="quiz-info">
                    <span class="quiz-badge">📚 ${escapeHTML(settings.topic)}</span>
                    <span class="quiz-badge">🎯 ${escapeHTML(settings.difficulty)}</span>
                    <span class="quiz-badge">📝 ${quizData.questions.length} Questions</span>
                </div>
            </div>
            <div class="questions-container">
                ${quizData.questions.map((q, index) => this.renderQuestion(q, index)).join('')}
            </div>
            <div class="quiz-actions">
                <button class="btn btn-primary btn-lg" onclick="quizGenerator.submitQuiz()">Submit Quiz</button>
            </div>
        `;
        
        this.resultsContainer.innerHTML = html;
        this.attachQuestionHandlers();
    }

    renderQuestion(question, index) {
        if (question.type === 'MCQ') {
            return this.renderMCQ(question, index);
        } else {
            return this.renderFillBlank(question, index);
        }
    }

    renderMCQ(question, index) {
        const letters = ['A', 'B', 'C', 'D'];
        
        return `
            <div class="question-card" data-question-index="${index}">
                <div class="question-header">
                    <span class="question-number">${index + 1}</span>
                    <span class="question-type-badge">Multiple Choice</span>
                </div>
                <div class="question-text">${escapeHTML(question.question)}</div>
                <div class="options-list">
                    ${question.options.map((option, optIndex) => `
                        <div class="option-item" data-option="${escapeHTML(option)}">
                            <span class="option-letter">${letters[optIndex]}</span>
                            <span class="option-text">${escapeHTML(option)}</span>
                        </div>
                    `).join('')}
                </div>
            </div>
        `;
    }

    renderFillBlank(question, index) {
        return `
            <div class="question-card" data-question-index="${index}">
                <div class="question-header">
                    <span class="question-number">${index + 1}</span>
                    <span class="question-type-badge">Fill in the Blank</span>
                </div>
                <div class="question-text">${escapeHTML(question.question)}</div>
                <input type="text" class="fill-blank-input" placeholder="Type your answer here..." data-question-index="${index}">
            </div>
        `;
    }

    attachQuestionHandlers() {
        const options = this.resultsContainer.querySelectorAll('.option-item');
        options.forEach(option => {
            option.addEventListener('click', (e) => this.handleOptionClick(e));
        });
    }

    handleOptionClick(event) {
        const optionElement = event.currentTarget;
        const questionCard = optionElement.closest('.question-card');
        const allOptions = questionCard.querySelectorAll('.option-item');
        
        allOptions.forEach(opt => opt.classList.remove('selected'));
        optionElement.classList.add('selected');
    }

    collectUserAnswers() {
        const answers = [];
        
        this.currentQuiz.questions.forEach((question, index) => {
            if (question.type === 'MCQ') {
                const questionCard = this.resultsContainer.querySelector(`[data-question-index="${index}"]`);
                const selected = questionCard.querySelector('.option-item.selected');
                answers.push(selected ? selected.dataset.option : '');
            } else {
                const input = this.resultsContainer.querySelector(`.fill-blank-input[data-question-index="${index}"]`);
                answers.push(input ? input.value.trim() : '');
            }
        });
        
        return answers;
    }

    async submitQuiz() {
        const userAnswers = this.collectUserAnswers();
        
        if (userAnswers.some(a => !a)) {
            showToast('warning', 'Incomplete', 'Please answer all questions before submitting');
            return;
        }

        const progressData = {
            student_id: this.studentId,
            topic: this.currentSettings.topic,
            difficulty: this.currentSettings.difficulty,
            questions: this.currentQuiz.questions.map(q => q.question),
            user_answers: userAnswers,
            correct_answers: this.currentQuiz.questions.map(q => q.correct_answer)
        };

        try {
            const result = await api.post(CONFIG.ENDPOINTS.PROGRESS_RECORD, progressData);
            this.showResults(userAnswers, result);
            showToast('success', 'Progress Saved!', `Accuracy: ${result.accuracy}%`);
            if (typeof refreshGamification === 'function') {
                await refreshGamification();
            }
        } catch (error) {
            showToast('error', 'Save Failed', 'Could not save progress, but showing results');
            this.showResults(userAnswers, null);
        }
    }

    showResults(userAnswers, progressResult) {
        const html = `
            <div class="quiz-results-summary">
                <h3>🎉 Quiz Complete!</h3>
                ${progressResult ? `
                    <div class="result-stats">
                        <div class="result-stat">
                            <span class="result-label">Accuracy</span>
                            <span class="result-value">${progressResult.accuracy}%</span>
                        </div>
                        <div class="result-stat">
                            <span class="result-label">Correct</span>
                            <span class="result-value">${progressResult.correct_count}/${progressResult.total_questions}</span>
                        </div>
                    </div>
                ` : ''}
            </div>
            <div class="questions-container">
                ${this.currentQuiz.questions.map((q, index) => this.renderQuestionResult(q, index, userAnswers[index])).join('')}
            </div>
            <div class="quiz-actions">
                <button class="btn btn-secondary" onclick="navigateToSection('progress')">View Progress</button>
                <button class="btn btn-primary" onclick="location.reload()">New Quiz</button>
            </div>
        `;
        
        this.resultsContainer.innerHTML = html;
    }

    renderQuestionResult(question, index, userAnswer) {
        const isCorrect = userAnswer.toLowerCase().trim() === question.correct_answer.toLowerCase().trim();
        const statusIcon = isCorrect ? '✅' : '❌';
        const statusClass = isCorrect ? 'correct' : 'incorrect';
        
        return `
            <div class="question-card result-card ${statusClass}">
                <div class="question-header">
                    <span class="question-number">${index + 1}</span>
                    <span class="result-badge">${statusIcon} ${isCorrect ? 'Correct' : 'Incorrect'}</span>
                </div>
                <div class="question-text">${escapeHTML(question.question)}</div>
                <div class="answer-comparison">
                    <div class="answer-row">
                        <span class="answer-label">Your Answer:</span>
                        <span class="answer-value user-answer">${escapeHTML(userAnswer)}</span>
                    </div>
                    ${!isCorrect ? `
                        <div class="answer-row">
                            <span class="answer-label">Correct Answer:</span>
                            <span class="answer-value correct-answer">${escapeHTML(question.correct_answer)}</span>
                        </div>
                    ` : ''}
                </div>
            </div>
        `;
    }
}

// Initialize quiz generator when DOM is loaded
let quizGenerator;
document.addEventListener('DOMContentLoaded', () => {
    quizGenerator = new QuizGenerator();
});
