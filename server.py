from flask import Flask, Response, redirect, url_for, request, session, abort, render_template, flash
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
from functools import wraps

#CONFIGURATION -------------------------
app = Flask(__name__)
app.config.update(DEBUG = True, SECRET_KEY = 'secret_xxx')
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
#---------------------------------------


class User(UserMixin):
	def __init__(self, id):
		self.id = id

	def get_id(self):         
		return str(self.id)

#Mock user database
users = {'admin': {'admin': '1234', 'role': 'Admin'},
			'moderator': {'moderator': '1234', 'role': 'Moderator'}}


def admin_required(f):
	@wraps(f)
	def wrap(*args, **kwargs):
		user = current_user.get_id()
		if users[user]['role'] == "Admin":
			return f(*args, **kwargs)
		else:
			flash("You need to be an admin to view this page.")
			return redirect(url_for('test'))

	return wrap
	

#ROUTES --------------------------------------------------------
@app.route('/')
@login_required
def home():
    return Response("Hello World!")
    
@app.route('/main')
@login_required
@admin_required
def main():
	return "Main Page"

@app.route('/test')
@login_required
def test():
	return "Test page"
 
#LOGIN
@app.route("/login", methods=["GET", "POST"])
def login():
	if request.method == 'POST':
		
		username = request.form['username']
		password = request.form['password']
		#CHECK
		if username in users and password == users[username][username]:
			user = User(id=username)
			login_user(user)
			return redirect(url_for('main'))
		return redirect(url_for('login'))
		
	return render_template("login.html")


#LOGOUT
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return Response('<p>Logged out</p>')
#---------------------------------------------------------------


#CALLBACK TO RELOAD     
@login_manager.user_loader
def load_user(userid):
    return User(userid)
    

if __name__ == "__main__":
    app.run()
