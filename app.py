from flask import Flask, render_template
from face import run_face_verification
import webbrowser

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/face-verification')
def face_verification():
    result = run_face_verification()
    return render_template('result.html', message=result)

if __name__ == '__main__':
    app.run(debug=True, port=5500)