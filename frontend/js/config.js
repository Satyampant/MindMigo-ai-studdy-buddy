// Configuration file for API endpoints and app settings
const CONFIG = {
    API_BASE_URL: 'http://localhost:8000',
    ENDPOINTS: {
        QUIZ_GENERATE: '/quiz/generate',
        KNOWLEDGE_GRAPH_GENERATE: '/knowledge-graph/generate',
        KNOWLEDGE_GRAPH_RENDER: '/knowledge-graph/render',
        DAILY_PROBLEM: '/daily-problem'
    },
    TOAST_DURATION: 5000,
    STORAGE_KEYS: {
        DAILY_STREAK: 'studdy_buddy_daily_streak',
        PROBLEMS_SOLVED: 'studdy_buddy_problems_solved',
        ACCURACY: 'studdy_buddy_accuracy',
        LAST_PROBLEM_DATE: 'studdy_buddy_last_problem_date',
        SELECTED_ANSWERS: 'studdy_buddy_selected_answers'
    }
};
