from flask import Flask, render_template, request, redirect, url_for
from utils import send_notification_email  # ← Import the email sender function

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', error=None)  # no error at first

@app.route('/verify_code', methods=['POST'])
def verify_code():
    entered_code = request.form.get('code', '').strip()

    her_name = "Shanthi"
    her_birth_date = "26"
    star_sign = "Sagittarius"

    expected_code = (
        her_name[:4].capitalize() +  # First 4 letters, first letter uppercase
        her_birth_date +
        star_sign[0].upper()
    ) 
    if entered_code == expected_code:
        send_notification_email(
            subject="✅ Mon Amour - Login - Code Accepted",
            body=f"The correct code was entered by her '{entered_code}'. Proceeding to next step."
        )
        return redirect(url_for('success'))
    else:
        send_notification_email(
            subject="❌ Mon Amour - Login - Incorrect Code Attempted",
            body=f"An incorrect code '{entered_code}' was entered."
        )
        return render_template('index.html', error="Incorrect code. Please try again.", wrong_code=True)

@app.route('/success')
def success():
    return "<h1>Welcome! The code was correct. Next steps here...</h1>"

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")