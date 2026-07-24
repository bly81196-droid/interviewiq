from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key_here' # ضروري جداً لتخزين النتائج المؤقتة في الـ Session

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

        # ==========================================
        # 2. ضعي كود الـ API الخاص بكِ هنا لإرسال الإجابات 
        # واستقبال التحليل (الدرجة، نقاط القوة، التحسينات)
        # ==========================================
        # مثال لتوضيح كيف تضعين النتيجة القادمة من الـ API:
        # api_result = call_your_ai_api(answers, job_position)
        
        # تخزين النتائج الحقيقية القادمة من الـ API في الـ Session لعرضها بالنتائج:
        session['score'] = 85  # <--- الدرجة الحقيقية القادمة من الـ API
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

        return redirect(url_for('results'))
        
    return render_template('interview.html')

@app.route('/results')
def results():
    # جلب النتائج الحقيقية التي خزناها بعد رد الـ API
    score = session.get('score', 70)
    strengths = session.get('strengths', [])
    improvements = session.get('improvements', [])
    
    return render_template('results.html', score=score, strengths=strengths, improvements=improvements)

if __name__ == '__main__':
    app.run(debug=True)