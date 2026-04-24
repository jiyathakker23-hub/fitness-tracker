from flask import Flask, render_template, Response
from fitness import generate_frames

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video/<exercise>')
def video(exercise):
    return Response(generate_frames(exercise),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(debug=True)