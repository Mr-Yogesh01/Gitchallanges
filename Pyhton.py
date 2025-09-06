from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import os

# -------------------------------
# Flask App Configuration
# -------------------------------
app = Flask(__name__)
app.secret_key = "supersecretkey"

# Database setup (SQLite for simplicity)
base_dir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(base_dir, 'users.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# -------------------------------
# Database Model
# -------------------------------
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f"<User {self.name}>"

# -------------------------------
# Routes
# -------------------------------

@app.route("/")
def index():
    users = User.query.all()
    return render_template("index.html", users=users)

@app.route("/add", methods=["GET", "POST"])
def add_user():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]

        if not name or not email:
            flash("All fields are required!", "danger")
            return redirect(url_for("add_user"))

        if User.query.filter_by(email=email).first():
            flash("Email already exists!", "warning")
            return redirect(url_for("add_user"))

        new_user = User(name=name, email=email)
        db.session.add(new_user)
        db.session.commit()

        flash("User added successfully!", "success")
        return redirect(url_for("index"))

    return render_template("add.html")

@app.route("/delete/<int:id>")
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    flash("User deleted successfully!", "info")
    return redirect(url_for("index"))

# -------------------------------
# Run Application
# -------------------------------
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
