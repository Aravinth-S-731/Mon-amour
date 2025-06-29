from flask import Flask, render_template, request, redirect, url_for, session
from datetime import timedelta
from utils import send_notification_email  # ← Import the email sender function

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Replace with a secure key

# ⏳ Set session timeout to 30 minutes
app.permanent_session_lifetime = timedelta(minutes=30)

@app.route('/')
def index():
    # If already authenticated, redirect to success page
    if session.get('authenticated'):
        return redirect(url_for('success'))
    return render_template('index.html', error=None)

@app.route('/verify_code', methods=['POST'])
def verify_code():
    entered_code = request.form.get('code', '').strip()

    her_name = "Shanthi"
    her_birth_date = "26"
    star_sign = "Sagittarius"

    expected_code = (
        her_name[:4].capitalize() +
        her_birth_date +
        star_sign[0].upper()
    )

    if entered_code == expected_code:
        session.permanent = True
        session['authenticated'] = True

        send_notification_email(
            subject="✅ Mon Amour - Login - Code Accepted",
            body=f"The correct code was entered by her '{entered_code}'. Proceeding to puzzle."
        )
        return redirect(url_for('puzzle'))  # ✅ Redirect to puzzle
    else:
        send_notification_email(
            subject="❌ Mon Amour - Login - Incorrect Code Attempted",
            body=f"An incorrect code '{entered_code}' was entered."
        )
        return render_template('index.html', error="Incorrect code. Please try again.", wrong_code=True)

@app.route('/puzzle')
def puzzle():
    if not session.get('authenticated'):
        return redirect(url_for('index'))
    return render_template('puzzle.html')

@app.route('/gallery')
def gallery():
    if not session.get('authenticated'):
        return redirect(url_for('index'))
    return render_template('gallery.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")