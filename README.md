# flask-login-roles
A simple Flask-Login backend with user roles

## Requirements:

You need to have flask and flask-login installed on your computer. To install them, you could do:

````
$ pip install flask
$ pip install flask-login
````

## Run:

To run the project, go to the main folder and run the server.py with the latest version of python. Then, go to 127.0.0.1:5000 on your browser.

<p>Logging in:</p>

To log in, go to 127.0.0.1:5000/login. A simple html form will appear. You can log in as one of this users:

````python
#Mock user database
users = {'admin': {'admin': '1234', 'role': 'Admin'},
			'moderator': {'moderator': '1234', 'role': 'Moderator'}}
````

<p>Logging out:</p>

To log out, go to 127.0.0.1:5000/logout. Then you can go to 127.0.0.1:500 and you will be redirected to the login page.

## User Roles:

In order to implement user roles, the mock user database has an extra argument with the role of each available user. If we want to restrict ceirtain pages only to the users with the role 'Admin', we could use our own decorator:

````python
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
````

This function gets the current_user role and checks if the user's role is 'Admin'. If so, you will be able to acces the route marked with @admin_required. Otherwise, you will be redirected to a 'test' page.
