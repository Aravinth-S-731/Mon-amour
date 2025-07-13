from flask import Flask, render_template, request, redirect, url_for, session
from datetime import timedelta
from utils import send_notification_email  # ← Import the email sender function
from progress_manager import get_progress, set_progress, reset_progress # ← Import the file handling function

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Replace with a secure key

# ⏳ Set session timeout to 30 minutes
app.permanent_session_lifetime = timedelta(minutes=60)

@app.route('/')
def index():
    # If already authenticated, redirect to success page
    if session.get('authenticated'):
        return redirect(url_for('ask_continue'))
    return render_template('index.html', error=None)

@app.route('/verify_code', methods=['POST'])
def verify_code():
    entered_code = request.form.get('code', '').strip()

    her_name = "Shanthi"
    her_birth_date = "26"
    star_sign = "Sagittarius"

    expected_code = (
        her_name[:4].capitalize() +  # "Shan"
        her_birth_date +
        star_sign[0].upper()
    )

    if entered_code == expected_code:
        progress = get_progress()

        if progress.get("started"):
            session.permanent = True
            session["authenticated"] = True
            return redirect(url_for('ask_continue'))
        else:
            set_progress("started", True)
            session.permanent = True
            session["authenticated"] = True
            send_notification_email(
                "She cracked the code 🗝️",
                "She entered the correct code and started the journey."
            )
            return redirect(url_for('puzzle'))

    else:
        # 📨 Send email for wrong attempt
        send_notification_email(
            "Wrong code attempt ❌",
            f"She entered an incorrect code: '{entered_code}'"
        )
        return render_template("index.html", wrong_code=True, error="Incorrect code 🥲")

@app.route('/ask_continue')
def ask_continue():
    if not session.get("authenticated"):
        return redirect(url_for("index"))
    return render_template("continue_or_reset.html")

@app.route('/continue_journey')
def continue_journey():
    if not session.get("authenticated"):
        return redirect(url_for("index"))
    progress = get_progress()
    last_page = progress.get("last_page", {}).get("value", "puzzle")
    send_notification_email("She continued the journey 🌸", f"She chose to continue from where she left off: {last_page}")
    try:
        return redirect(url_for(last_page))
    except:
        return redirect(url_for("puzzle"))


@app.route('/reset_journey')
def reset_journey():
    if not session.get("authenticated"):
        return redirect(url_for("index"))
    reset_progress()
    set_progress("started", True)
    send_notification_email("She reset the journey 🧼", "She chose to start over from the beginning.")
    return redirect(url_for('puzzle'))

@app.route('/admin/<token>')
def admin(token):
    if token == "262921":  # Change this to something long/random
        reset_progress()
        send_notification_email("Admin Reset Triggered 🔐", "You manually reset her journey.")
        session.clear()
        return redirect(url_for('index'))
    return "Unauthorized", 403


@app.route('/puzzle')
def puzzle():
    if not session.get('authenticated'):
        return redirect(url_for('index'))
    set_progress("last_page", "puzzle")
    return render_template('puzzle.html')

@app.route('/gallery')
def gallery():
    if not session.get('authenticated'):
        return redirect(url_for('index'))
    set_progress("last_page", "gallery")
    return render_template('gallery.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")