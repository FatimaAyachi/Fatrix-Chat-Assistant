from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from AFA_chat import chatbot_response

app = Flask(__name__)
app.secret_key = "super_secret_key_123"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # fichier local
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(150), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@app.route('/register', methods=['GET', 'POST'])
def register():
    message = request.args.get('message', '')  # pour affichage message optionnel
    if request.method == 'POST':
        username = request.form.get('username').strip()
        password = request.form.get('password').strip()
        confirm = request.form.get('confirm').strip()

        if not username or not password or not confirm:
            error = "Please fill all fields"
            return render_template('register.html', error=error)

        if password != confirm:
            error = "Passwords do not match"
            return render_template('register.html', error=error)

        if User.query.filter_by(username=username).first():
            error = "Username already taken"
            return render_template('register.html', error=error)

        new_user = User(username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        session['user'] = username
        return redirect(url_for('home'))

    return render_template('register.html', message=message)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username").strip()
        password = request.form.get("password").strip()

        user = User.query.filter_by(username=username).first()

        if user:
            if user.check_password(password):
                session["user"] = user.username
                return redirect(url_for("home"))
            else:
                return render_template("login.html", error="Invalid password")
        else:
            # Utilisateur non trouvé => rediriger vers inscription avec message
            return redirect(url_for("register", message="User not found. Please register."))

    return render_template("login.html")


@app.route("/")
def home():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("index.html")


@app.route("/get_response", methods=["POST"])
def get_response():
    try:
        user_input = request.json.get("message")
        print(f"Message received: {user_input}")
        response = chatbot_response(user_input)
        return jsonify({"response": response})
    except Exception as e:
        print(f"Error :{e}")
        return jsonify({"response": "Sorry , an error occurred"})


with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
