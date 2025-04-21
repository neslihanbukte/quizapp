from flask import Flask, render_template, request, redirect, session
from config import Config
from models import db, User, Result

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

with app.app_context():
    db.create_all()

correct_answers = {
    "question1": "C",  # @bot.command()
    "question2": "C",  # @app.route()
    "question3": "D",  # Scikit-learn
    "question4": "B",  # YOLO
    "question5": "C"   # BeautifulSoup
}

@app.route("/", methods=["GET", "POST"])
def quiz():
    if request.method == "POST":
        username = request.form.get("username").strip()
        if not username:
            return redirect("/")

        session["username"] = username

        user_answers = {
            "question1": request.form.get("question1"),
            "question2": request.form.get("question2"),
            "question3": request.form.get("question3"),
            "question4": request.form.get("question4"),
            "question5": request.form.get("question5")
        }

        score = 0
        for q_key in correct_answers:
            if user_answers[q_key] == correct_answers[q_key]:
                score += 20

        user = User.query.filter_by(username=username).first()
        if not user:
            user = User(username=username, highest_score=score, last_score=score)
            db.session.add(user)
        else:
            user.last_score = score
            if score > user.highest_score:
                user.highest_score = score

        db.session.commit()

        result = Result(user_id=user.id, score=score)
        db.session.add(result)
        db.session.commit()

        return redirect("/result")

    username = session.get("username")
    user_best = None
    global_best_score = 0
    global_best_user = None

    if username:
        user = User.query.filter_by(username=username).first()
        if user:
            user_best = user.highest_score

    best_user = User.query.order_by(User.highest_score.desc()).first()
    if best_user:
        global_best_score = best_user.highest_score
        global_best_user = best_user.username

    return render_template("quiz.html", user_best=user_best,
                           global_best_score=global_best_score,
                           global_best_user=global_best_user,
                           username=username)

@app.route("/result")
def result():
    username = session.get("username")
    if not username:
        return redirect("/")

    user = User.query.filter_by(username=username).first()
    if not user:
        return redirect("/")

    latest_result = Result.query.filter_by(user_id=user.id).order_by(Result.id.desc()).first()

    best_user = User.query.order_by(User.highest_score.desc()).first()
    global_best_score = best_user.highest_score if best_user else 0
    global_best_user = best_user.username if best_user else "?"

    return render_template("result.html",
                           score=latest_result.score,
                           user_best=user.highest_score,
                           global_best_score=global_best_score,
                           global_best_user=global_best_user,
                           username=username)

@app.cli.command("create-db")
def create_db():
    db.create_all()
    print("Veritabanı oluşturuldu.")

if __name__ == "__main__":
    app.run(debug=True)


