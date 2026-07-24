from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# 1. صفحة البداية (رفع السيرة الذاتية واختيار التخصص)
@app.route('/')
def home():
    return render_template('index.html')

# 2. صفحة المقابلة والأسئلة الثلاثة
@app.route('/interview', methods=['GET', 'POST'])
def interview():
    if request.method == 'POST':
        # استقبال إجابات الأسئلة الثلاثة هنا إذا احتجت لحفظها أو تقييمها
        answer1 = request.form.get('answer1')
        answer2 = request.form.get('answer2')
        answer3 = request.form.get('answer3')
        
        # بعد استقبال الإجابات، نحول المستخدم لصفحة النتائج
        return redirect(url_for('results'))
        
    return render_template('interview.html')

# 3. صفحة النتائج (التقييم ونقاط القوة والتطوير)
@app.route('/results')
def results():
    return render_template('results.html')

if __name__ == '__main__':
    app.run(debug=True)