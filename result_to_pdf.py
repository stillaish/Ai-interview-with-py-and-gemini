from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os
from datetime import datetime

def save_result_to_pdf(job_role, results, accuracy):
    filename = f"quiz_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    filepath = os.path.join(os.getcwd(), filename)

    c = canvas.Canvas(filepath, pagesize=letter)
    width, height = letter
    y = height - 50

    # Title
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y, f"AI Interview Quiz Results - {job_role}")
    y -= 30

    # Accuracy
    c.setFont("Helvetica", 12)
    c.drawString(50, y, f"Accuracy: {accuracy}%")
    y -= 20
    c.drawString(50, y, f"Total Questions: {len(results)}")
    y -= 30

    for idx, r in enumerate(results, start=1):
        if y < 100:
            c.showPage()
            y = height - 50
            c.setFont("Helvetica", 12)

        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y, f"Q{idx}: {r['question']}")
        y -= 20

        c.setFont("Helvetica", 11)
        c.drawString(70, y, f"Your Answer: {r['your_answer']}")
        y -= 15
        c.drawString(70, y, f"Correct Answer: {r['correct_answer']}")
        y -= 15
        c.drawString(70, y, f"Result: {r['result']}")
        y -= 25

    c.save()
    return filepath
