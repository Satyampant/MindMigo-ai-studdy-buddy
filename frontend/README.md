# Studdy Buddy AI - Frontend

A modern, responsive web application for AI-powered learning assistance.

## Features

- **Quiz Generator**: Create custom quizzes on any topic with multiple difficulty levels
- **Knowledge Graph**: Visualize complex topics as interactive network graphs
- **Daily Challenge**: Test your skills with a new challenging problem every day
- **Progress Tracking**: Track your learning streak, accuracy, and problems solved

## Getting Started

### Prerequisites

- A modern web browser (Chrome, Firefox, Safari, or Edge)
- Backend server running (see main project README)

### Installation

1. Ensure the backend server is running on `http://localhost:8000`
2. Open `index.html` in your web browser, or serve it using a local server:

```bash
# Using Python 3
cd frontend
python -m http.server 8080

# Using Node.js (http-server)
npx http-server frontend -p 8080
```

3. Access the application at `http://localhost:8080`

### Configuration

Edit `js/config.js` to change the backend API URL:

```javascript
const CONFIG = {
    API_BASE_URL: 'http://localhost:8000',  // Change this if your backend runs elsewhere
    ...
};
```

## Project Structure

```
frontend/
├── index.html              # Main HTML file
├── css/
│   └── styles.css         # All styles (minified)
└── js/
    ├── config.js          # Configuration and constants
    ├── api.js             # API communication layer
    ├── utils.js           # Utility functions
    ├── quiz.js            # Quiz generator logic
    ├── knowledgeGraph.js  # Knowledge graph logic
    ├── dailyProblem.js    # Daily challenge logic
    └── main.js            # Main app and navigation
```

## Usage

### Quiz Generator

1. Navigate to the "Quiz Generator" section
2. Enter a topic (e.g., "Python programming")
3. Select question type (Multiple Choice or Fill in the Blank)
4. Choose difficulty level (Easy, Medium, Hard)
5. Adjust number of questions (1-10)
6. Click "Generate Quiz"

### Knowledge Graph

1. Navigate to the "Knowledge Graph" section
2. Choose input type:
   - **Topic**: Enter a topic and the AI will generate content
   - **Custom Text**: Paste your own text to visualize
3. Click "Generate Knowledge Graph"
4. Use "View Fullscreen" for better visualization

### Daily Challenge

1. Navigate to the "Daily Challenge" section
2. Read today's problem
3. Select your answer
4. Click "Submit Answer" to check if you're correct
5. Track your progress with the stats cards below

## Features in Detail

### Local Storage

The app uses browser local storage to track:
- Daily problem streak
- Total problems solved
- Accuracy rate
- Last problem completion date

### Responsive Design

The application is fully responsive and works on:
- Desktop computers
- Tablets
- Mobile phones

### Toast Notifications

Real-time feedback for all actions:
- Success messages (green)
- Error messages (red)
- Warnings (yellow)
- Info messages (blue)

## Browser Support

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## Troubleshooting

### "Cannot connect to backend" error

- Ensure the backend server is running
- Check that the API URL in `config.js` matches your backend URL
- Verify CORS is enabled on the backend (it should be by default)

### Knowledge graph not displaying

- Check browser console for errors
- Ensure the backend returned valid HTML content
- Try refreshing the page

### Local storage issues

- Ensure your browser allows local storage
- Clear browser cache if stats aren't updating
- Check browser privacy settings

## Development

### Making Changes

1. Edit HTML in `index.html`
2. Edit styles in `css/styles.css`
3. Edit JavaScript in the appropriate `js/*.js` file
4. Refresh browser to see changes

### Adding New Features

1. Add HTML structure in `index.html`
2. Add styles in `css/styles.css`
3. Create new JS file in `js/` directory
4. Import the new JS file in `index.html`

## License

This project is part of the Studdy Buddy AI application.
