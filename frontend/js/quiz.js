// Quiz Generator functionality

class QuizGenerator {
    constructor() {
        this.form = document.getElementById('quiz-form');
        this.resultsContainer = document.getElementById('quiz-results');
        this.placeholder = document.getElementById('quiz-placeholder');
        this.generateButton = document.getElementById('generate-quiz-btn');
        this.currentQuiz = null;
        
        this.init();
    }

    init() {
        // Form submission handler
        this.form.addEventListener('submit', (e) => this.handleSubmit(e));
        
        // Range slider update
        const rangeInput = document.getElementById('num-questions');
        const rangeDisplay = document.getElementById('num-display');
        rangeInput.addEventListener('input', (e) => {
            rangeDisplay.textContent = e.target.value;
        });
    }

    async handleSubmit(event) {
        event.preventDefault();
        
        const formData = new FormData(this.form);
        const settings = {
            topic: formData.get('topic') || document.getElementById('quiz-topic').value,
            question_type: document.getElementById('question-type').value,
            difficulty: formData.get('difficulty'),
            num_questions: parseInt(document.getElementById('num-questions').value)
        };

        setButtonLoading(this.generateButton, true);

        try {
            const response = await api.post(CONFIG.ENDPOINTS.QUIZ_GENERATE, settings);
            this.currentQuiz = response;
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
                <div class="answer-section">
                    <div class="answer-label">Correct Answer:</div>
                    <div class="answer-text">${escapeHTML(question.correct_answer)}</div>
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
                <input type="text" class="fill-blank-input" placeholder="Type your answer here...">
                <div class="answer-section">
                    <div class="answer-label">Correct Answer:</div>
                    <div class="answer-text">${escapeHTML(question.correct_answer)}</div>
                </div>
            </div>
        `;
    }

    attachQuestionHandlers() {
        // Add click handlers for MCQ options
        const options = this.resultsContainer.querySelectorAll('.option-item');
        options.forEach(option => {
            option.addEventListener('click', (e) => this.handleOptionClick(e));
        });
    }

    handleOptionClick(event) {
        const optionElement = event.currentTarget;
        const questionCard = optionElement.closest('.question-card');
        const allOptions = questionCard.querySelectorAll('.option-item');
        
        // Remove previous selection
        allOptions.forEach(opt => opt.classList.remove('selected'));
        
        // Add selection to clicked option
        optionElement.classList.add('selected');
    }
}

// Initialize quiz generator when DOM is loaded
let quizGenerator;
document.addEventListener('DOMContentLoaded', () => {
    quizGenerator = new QuizGenerator();
});
