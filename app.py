from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        return redirect(url_for('interview'))
    return render_template('index.html')

@app.route('/interview', methods=['GET', 'POST'])
def interview():
    if request.method == 'POST':
        return redirect(url_for('question'))
    return render_template('interview.html')

@app.route('/question', methods=['GET', 'POST'])
def question():
    if request.method == 'POST':
        # ناخذ الإجابة اللي كتبها المستخدم ونحسب عدد الكلمات كمثال ذكي لتقييم الأداء
        user_answer = request.form.get('answer', '')
        word_count = len(user_answer.split())
        
        # حساب الدرجة ديناميكياً بناءً على طول الإجابة
        if word_count > 10:
            calculated_score = 90
        elif word_count > 5:
            calculated_score = 75
        else:
            calculated_score = 60
            
        # نخزنها أو نمررها لصفحة النتائج
        return render_template('results.html', score=calculated_score)
        
    return render_template('question.html')

@app.route('/results', methods=['GET', 'POST'])
def results():
    return render_template('results.html', score=70)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)