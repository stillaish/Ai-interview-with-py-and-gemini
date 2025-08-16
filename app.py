import streamlit as st
import json
from generator import generate_quiz
from result_to_pdf import save_result_to_pdf

st.set_page_config(page_title="AI Interview Quiz", layout="wide")

st.title("🤖 AI Interview Question Generator by Aish")

# Sidebar
st.sidebar.header("Settings")
job_role = st.sidebar.text_input("Enter Job Role", "Software Engineer")
num_tech = st.sidebar.slider("Number of Technical Questions", 3, 10, 5)
num_hr = st.sidebar.slider("Number of HR Questions", 1, 5, 3)

if st.sidebar.button("Generate Quiz"):
    st.session_state.quiz = generate_quiz(job_role, num_tech, num_hr)
    st.session_state.answers = {}

quiz = st.session_state.get("quiz", {})

# Extract questions properly
questions = []
if isinstance(quiz, dict) and "questions" in quiz:
    questions = quiz["questions"]
elif isinstance(quiz, list):
    questions = quiz

if not questions:
    st.warning("⚠️ No questions yet. Enter a role and click 'Generate Quiz'.")
    st.stop()

# Show questions
st.subheader(f"📋 Quiz for {job_role}")
for idx, q in enumerate(questions):
    st.markdown(f"**Q{idx+1}. {q['question']}**")
    selected = st.radio(
        f"Select your answer for Q{idx+1}",
        q["options"],
        key=f"q{idx}"
    )
    st.session_state.answers[idx] = selected

# Submit
if st.button("Submit Quiz"):
    correct = 0
    detailed_results = []

    for idx, q in enumerate(questions):
        user_ans = st.session_state.answers.get(idx)
        correct_ans = q["answer"]

        is_correct = user_ans == correct_ans
        if is_correct:
            correct += 1

        detailed_results.append({
            "question": q["question"],
            "your_answer": user_ans,
            "correct_answer": correct_ans,
            "result": "✅ Correct" if is_correct else "❌ Wrong"
        })

    total = len(questions)
    accuracy = round((correct / total) * 100, 2)

    st.success(f"🎉 You got {correct}/{total} correct ({accuracy}%)")

    # Show detailed results
    for r in detailed_results:
        st.write(f"**Q:** {r['question']}")
        st.write(f"👉 Your Answer: {r['your_answer']}")
        st.write(f"✅ Correct Answer: {r['correct_answer']}")
        st.write(f"Result: {r['result']}")
        st.markdown("---")

    # Save PDF
    pdf_path = save_result_to_pdf(job_role, detailed_results, accuracy)
    with open(pdf_path, "rb") as pdf_file:
        st.download_button("📥 Download Results as PDF", pdf_file, file_name="quiz_results.pdf")
