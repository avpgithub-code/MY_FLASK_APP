from flask import Flask,render_template,request,redirect,session,url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

# Create Application
app = Flask(__name__)
app.secret_key = "your_secret_key"

# Configure SQLAlchemy to work with Flask
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database_auth.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db_auth = SQLAlchemy(app)

# Databse Model - Represents a single row
class User(db_auth.Model):
    # Class Variables
    id = db_auth.Column(db_auth.Integer, primary_key=True)
    username = db_auth.Column(db_auth.String(25), unique=True, nullable=False)
    password = db_auth.Column(db_auth.String(150), nullable=False)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


# Create End Points or Route
@app.route('/')
def home():
    if "username" in session:
        return redirect(url_for("dashboard"))
    return render_template("index_auth.html")

# Login
@app.route("/login", methods=["POST"])
def login():
    # Collect the info from the form 
    username = request.form["username"]
    password = request.form["password"]
    user = User.query.filter_by(username=username).first()
    # Check it's in the DB / Login
    if user and user.Check_password(password):
        session['username'] = username
        return redirect(url_for('dashboard'))
    else:
        # Otherwise show home page: Not a User
        return render_template("index_auth.html")

# Register
@app.route("/register", methods=["POST"])
def register():
    username = request.form["username"]
    password = request.form["password"]
    user = User.query.filter_by(username=username).first()
    # Check it's in the DB / Login
    if user:
        return render_template("index_auth.htmml", error="User already exists")
    else:
        new_user = User(username=username)
        new_user.set_password(password)
        db_auth.session.add(new_user)
        db_auth.session.commit()
        session['username'] = username
        return redirect(url_for('dashboard'))
    
# Dashboard
@app.route("/dashboard")
def dashboard():
    if "username" in session:
        return render_template("dashboard.html", username=session['username'])
    return redirect(url_for('home'))

# Logout
@app.route("/logout")
def logout():
    session.pop('username',None)
    return redirect(url_for('home'))

if __name__ in '__main__':
    with app.app_context():
        db_auth.create_all()
    
    app.run(host='127.0.0.1',port=5000,debug=True)

