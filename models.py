from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    highest_score = db.Column(db.Integer, default=0)
    last_score = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f"<User {self.username}>"

class Result(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    score = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<Result User ID={self.user_id} Score={self.score}>"

