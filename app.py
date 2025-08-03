from flask import Flask, render_template, request, redirect, url_for, session, flash
from datetime import timedelta
from utils import send_notification_email  # ← Import the email sender function
from progress_manager import get_progress, set_progress, reset_progress # ← Import the file handling function
from werkzeug.utils import secure_filename
import re, os

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Replace with a secure key
JOURNEY_ORDER = ["puzzle", "gallery", "name_guess", "poem", "timeline", "video"]

# ⏳ Set session timeout to 30 minutes
app.permanent_session_lifetime = timedelta(minutes=60)

UPLOAD_FOLDER = "uploads/selfies"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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
        send_notification_email(
                "She cracked the code 🗝️",
                "She entered the correct code and started the journey."
            )

        if progress.get("started"):
            session.permanent = True
            session["authenticated"] = True
            return redirect(url_for('ask_continue'))
        else:
            set_progress("started", True)
            session.permanent = True
            session["authenticated"] = True
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
    set_progress("last_page", "puzzle")
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
    return render_template('puzzle.html')

@app.route('/puzzle_complete', methods=["POST"])
def puzzle_complete():
    if not session.get('authenticated'):
        return redirect(url_for('index'))
    set_progress("last_page", "gallery")  # ✅ Only set after real completion
    send_notification_email("Puzzle Completed 🧩", "She completed the puzzle.")
    return '', 204  # Return empty response

@app.route('/gallery')
def gallery():
    if not session.get('authenticated'):
        return redirect(url_for('index'))
    if not is_page_allowed("gallery"):
        return redirect(url_for('puzzle'))
    set_progress("last_page", "gallery")
    return render_template('gallery.html')

@app.route('/go_to_name_guess', methods=["POST"])
def go_to_name_guess():
    if not session.get('authenticated'):
        return redirect(url_for('index'))
    if not is_page_allowed("name_guess"):
        return redirect(url_for('gallery'))
    set_progress("last_page", "name_guess")
    return redirect(url_for('name_guess'))

@app.route('/name_guess', methods=["GET", "POST"])
def name_guess():
    if not session.get("authenticated"):
        return redirect(url_for("index"))

    if "name_guess_attempts" not in session:
        session["name_guess_attempts"] = 0

    attempts = session["name_guess_attempts"]
    error_msg = None

    if request.method == "POST":
        guessed_name = ""
        attempts += 1
        session["name_guess_attempts"] = attempts

        # Handling different input forms
        if attempts == 1:
            guessed_name = request.form.get("guessed_name", "").strip().lower()
        else:
            parts = []
            for i in range(1, 9):  # Max 8 letters in Aravinth
                char = request.form.get(f"char{i}", "")
                parts.append(char.lower())
            guessed_name = "".join(parts).strip()

        nickname_pattern = r"^arvii*$"
        valid_names = {"aravind", "arvind", "aravinth", "arvinth"}

        if re.match(nickname_pattern, guessed_name) or guessed_name in valid_names:
            send_notification_email("Name Guess Cracked 💡", f"She guessed your name as '{guessed_name}'")
            set_progress("last_page", "name_guess")
            session.pop("name_guess_attempts", None)
            return redirect(url_for("poem"))

        elif attempts >= 3:
            send_notification_email("Auto-Skipped After 3 Guesses 🔄", f"She tried 3 times. Skipping name guess. \n Attempt {attempts}: '{guessed_name}'")
            set_progress("last_page", "name_guess")
            session.pop("name_guess_attempts", None)
            return redirect(url_for("go_to_poem"))
        else:
            send_notification_email("Wrong Name Guess ❌", f"Attempt {attempts}: '{guessed_name}'")
            error_msg = f"That's not it 😅. Try again! ({attempts} / 3)"

    return render_template("name_guess.html", error=error_msg)

@app.route('/go_to_poem', methods=["POST"])
def go_to_poem():
    if not session.get('authenticated'):
        return redirect(url_for('index'))
    if not is_page_allowed("poem"):
        return redirect(url_for('name_guess'))
    set_progress("last_page", "poem")
    send_notification_email("Redirect to Poem 📜")
    return redirect(url_for('poem'))

@app.route('/poem')
def poem():
    if not session.get('authenticated'):
        return redirect(url_for('index'))
    if not is_page_allowed("poem"):
        return redirect(url_for('name_guess'))
    set_progress("last_page", "poem")
    return render_template('poem.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

def is_page_allowed(current_page):
    progress = get_progress()
    last_page = progress.get("last_page", {}).get("value", None)
    
    if not last_page:
        return current_page == "puzzle"  # Only puzzle is allowed at first

    try:
        last_index = JOURNEY_ORDER.index(last_page)
        current_index = JOURNEY_ORDER.index(current_page)
        return current_index <= last_index + 1
    except ValueError:
        return False  # Unknown page


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")