import os
import streamlit as st
import pandas as pd
from src.generator.question_generator import QuestionGenerator

def rerun():
    st.session_state['rerun_trigger'] = not st.session_state.get('rerun_trigger', False)

class QuizManager:
    def __init__(self):
        self.questions = []
        self.user_answers = []
        self.results = []

    def generate_questions(self, generator:QuestionGenerator, topic:str, question_type:str, difficulty:str, num_questions:int):
        self.questions = []
        try:
            for _ in range(num_questions):
                if question_type == 'MCQ':
                    question = generator.generate_mcq(topic, difficulty)
                else:
                    question = generator.generate_fill_blank(topic, difficulty)
                self.questions.append(question)
        except Exception as e:
            st.error(f"Error generating questions: {e}")
            return False
        return True
    
    def attempt_quiz(self):
        self.user_answers = []
        for idx, question in enumerate(self.questions):
            st.markdown(f"### Question {idx + 1}")
            st.markdown(question.question)
            if hasattr(question, 'options'):
                options = question.options
                user_answer = st.radio("Select an option:", options, key=f"q{idx}")
            else:
                user_answer = st.text_input("Your answer:", key=f"q{idx}")
            self.user_answers.append(user_answer)
            st.markdown("---")

    def evaluate_quiz(self):
        self.results = []
        score = 0
        for question, user_answer in zip(self.questions, self.user_answers):
            correct = False
            if hasattr(question, 'correct_option'):
                correct = (user_answer == question.correct_option)
            else:
                correct = (user_answer.strip().lower() == question.answer.strip().lower())
            self.results.append((question, user_answer, correct))
            if correct:
                score += 1
        return score
    
    def generate_report(self):
        if not self.results:
            st.warning("No results to generate report.")
            return None
        report_data = []
        for idx, (question, user_answer, correct) in enumerate(self.results):
            report_data.append({
                "Question": question.question,
                "Your Answer": user_answer,
                "Correct Answer": getattr(question, 'correct_option', question.answer),
                "Result": "Correct" if correct else "Incorrect"
            })
        df = pd.DataFrame(report_data)
        return df
    
    def save_report(self, filename_prefix:str="quiz_report"):
        df = self.generate_report()

        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{filename_prefix}_{timestamp}.csv"

        os.makedirs("results", exist_ok=True)
        full_path = os.path.join("results", filename)
        try:
            df.to_csv(full_path, index=False)
            st.success(f"Report saved as {filename}")
            return full_path
        except Exception as e:
            st.error(f"Error saving report: {e}")
            return None
