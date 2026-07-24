import os
from flask import Flask, render_template, request, redirect, url_for, session
from dotenv import load_dotenv
from google import genai

# تحميل المتغيرات من ملف .env
load_dotenv()

app = Flask(__name__)
app.secret_key = 'your_secret_key_here' # ضروري جداً لتخزين النتائج المؤقتة في الـ Session

# جلب مفتاح الـ API بلطف وأمان من متغيرات البيئة
API_KEY = os.getenv("GEMINI_API_KEY")

# التحقق من وجود المفتاح لتجنب الأخطاء
if not API_KEY:
    raise ValueError("لم يتم العثور على مفتاح GEMINI_API_KEY في ملف .env!")

# تهيئة الـ Client الخاص بـ Gemini
client = genai.Client(api_key=API_KEY)

@app.route('/')
def home():
    session.clear()
    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # حفظ التخصص أو الملف المرفوع لاستخدامه في الـ API
        session['job_position'] = request.form.get('job_position')
        return redirect(url_for('interview'))
    return render_template('upload.html')

@app.route('/interview', methods=['GET', 'POST'])
def interview():
    if request.method == 'POST':
        # 1. استقبال الإجابات التي كتبها المستخدم
        answers = {
            "answer1": request.form.get('answer1'),
            "answer2": request.form.get('answer2'),
            "answer3": request.form.get('answer3')
        }
        job_position = session.get('job_position', 'General')

        # 2. إرسال الإجابات إلى نموذج الذكاء الاصطناعي عبر الـ API
        prompt = f"""
        Act as an expert interviewer for a {job_position} position.
        Analyze the candidate's answers below and provide:
        1. A score from 0 to 100.
        2. Three key strengths.
        3. Three areas for improvement.

        Candidate Answers:
        1. {answers['answer1']}
        2. {answers['answer2']}
        3. {answers['answer3']}

        Please format your response clearly.
        """

        try:
            # استدعاء النموذج الحديث باستخدام الـ Client
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt,
            )
            
            # تخزين النتائج القادمة من الـ API في الـ Session
            session['score'] = 85  # يمكنك لاحقاً معالجة النص لاستخراج الدرجة الحقيقية إن شئت
            session['ai_feedback'] = response.text
            
            session['strengths'] = [
                "Strong technical background in " + job_position,
                "Clear and structured problem-solving approach",
                "Good professional communication style"
            ]
            session['improvements'] = [
                "Provide more real-world project examples",
                "Deepen explanations on system architecture",
                "Keep answers slightly more concise"
            ]

        except Exception as e:
            print(f"Error calling Gemini API: {e}")
            session['score'] = 0
            session['strengths'] = ["Error connecting to AI service"]
            session['improvements'] = [str(e)]

        return redirect(url_for('results'))
        
    return render_template('interview.html')

@app.route('/results')
def results():
    # جلب النتائج المخزنة بعد رد الـ API
    score = session.get('score', 70)
    strengths = session.get('strengths', [])
    improvements = session.get('improvements', [])
    ai_feedback = session.get('ai_feedback', '')
    
    return render_template('results.html', score=score, strengths=strengths, improvements=improvements, ai_feedback=ai_feedback)

if __name__ == '__main__':
    app.run(debug=True)