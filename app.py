from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # استقبال الأسئلة الثلاثة من النموذج
        q1 = request.form.get('question1')
        q2 = request.form.get('question2')
        q3 = request.form.get('question3')
        
        # تمرير الأسئلة لصفحة العرض (أو تعديلها حسب صفحة النتائج عندك)
        return render_template('result.html', question1=q1, question2=q2, question3=q3)
        
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)