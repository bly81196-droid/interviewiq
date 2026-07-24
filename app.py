from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# 1. صفحة البداية (السلايد الأول)
@app.route('/')
def home():
    return render_template('index.html')

# 2. صفحة رفع الملف واختيار التخصص (السلايد الثاني)
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        return redirect(url_for('interview'))
    return render_template('upload.html')

# 3. صفحة الأسئلة الثلاثة (السلايد الثالث)
@app.route('/interview', methods=['GET', 'POST'])
def interview():
    if request.method == 'POST':
        return redirect(url_for('results'))
    return render_template('interview.html')

# 4. صفحة النتائج (السلايد الرابع والأخير)
@app.route('/results')
def results():
    return render_template('results.html')

if __name__ == '__main__':
    app.run(debug=True)