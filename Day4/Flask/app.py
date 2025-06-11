from datetime import datetime
from flask import Flask, request, render_template

app = Flask(__name__)

# Store submissions in memory (for demo - use database in production)
submissions = []

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get form data
        new_submission = {
            'name': request.form.get('name'),
            'email': request.form.get('email'),
            'message': request.form.get('message'),
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        submissions.append(new_submission)
    
    return render_template('index.html', submissions=submissions)

if __name__ == '__main__':
    app.run(debug=True)