import os
import streamlit as st
from dotenv import load_dotenv
from src.utils.helpers import *
from src.generator.question_generator import QuestionGenerator
load_dotenv()

def main():
    st.set_page_config(page_title="AI Quiz Generator", layout="centered", page_icon="🤖")

    if 'quiz_manager' not in st.session_state:
        st.session_state.quiz_manager = QuizManager()

    if 'question_generated' not in st.session_state:
        st.session_state.question_generated = False

    if 'quiz_submitted' not in st.session_state:
        st.session_state.quiz_submitted = False

    if 'rerun_trigger' not in st.session_state:
        st.session_state.rerun_trigger = False

    st.title("🤖 Studdy Buddy AI")

    st.sidebar.header("Quiz Configuration")
    topic = st.sidebar.text_input("Enter the topic for the quiz:", value="Python programming")
    question_type = st.sidebar.selectbox("Select question type:", options=["MCQ", "Fill in the Blank"])
    difficulty = st.sidebar.selectbox("Select difficulty level:", options=["easy", "medium", "hard"])
    num_questions = st.sidebar.slider("Number of questions:", min_value=1, max_value=10, value=5)

    if st.sidebar.button("Generate Quiz"):
        st.session_state.quiz_submitted = False
        generator = QuestionGenerator()
        success = st.session_state.quiz_manager.generate_questions(generator, topic, question_type, difficulty, num_questions)
        if success:
            st.session_state.question_generated = True
            rerun()
        else:
            st.session_state.question_generated = False
            st.error("Failed to generate quiz. Please try again.")

    if st.session_state.question_generated and st.session_state.quiz_manager.questions:
        st.header("Quiz")
        st.session_state.quiz_manager.attempt_quiz()

        if st.button("Submit Quiz"):
            st.session_state.quiz_manager.evaluate_quiz()
            st.session_state.quiz_submitted = True
            rerun()

    if st.session_state.quiz_submitted:
        st.header("Results")
        results_df = st.seesion_state.quiz_manager.get_results_dataframe()
        if not results_df.empty:
            correct_count = results_df['Correct'].sum()
            total_questions = len(results_df)
            score_percentage = (correct_count / total_questions) * 100
            st.subheader(f"Your Score: {correct_count} out of {total_questions} ({score_percentage:.2f}%)")
            # st.session_state.quiz_manager.plot_results()

            for _, result in results_df.iterrows():
                st.markdown(f"**Q:** {result['Question']}")
                st.markdown(f"- Your Answer: {result['Your Answer']}")
                st.markdown(f"- Correct Answer: {result['Correct Answer']}")
                st.markdown(f"- Result: {'✅ Correct' if result['Correct'] else '❌ Incorrect'}")
                st.markdown("---")

            if st.button("Download Report as CSV"):
                csv_data = st.session_state.quiz_manager.generate_report()
                if csv_data:
                    with open(csv_data, 'r') as file:
                        
                        st.download_button(
                            label="Download CSV",
                            data=f.read(),
                            file_name=os.path.basename(csv_data),
                            mime='text/csv'
                        )
            else:
                st.warning("No results to display.")

if __name__ == "__main__":
    main()