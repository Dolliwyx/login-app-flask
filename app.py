from flask import Flask, redirect, render_template, request
from modules import dbmanager
import bcrypt
import re

app = Flask(__name__)

@app.route("/")
@app.route("/login", methods=["GET", "POST"])
def login():
	is_error = False
	is_attempted = False

	if request.method == "POST":
		is_attempted = True
		records = dbmanager.read_records()
		
		# Loop over all records in the CSV
		for record in records:
			# Check for username match
			if record["username"] == request.form.get("username"):
				stored = record["password"]
				# Compare the hashed password with the user input
				if bcrypt.checkpw(request.form.get("password").encode("utf-8"), stored.encode("utf-8")):
					# Render welcome page if successful
					return render_template("welcome.html", username=request.form.get("username"))
			else: is_error = True
	
	# Render login page with error message if unsuccessful
	return render_template("login.html", error=True) if is_error or is_attempted else render_template("login.html") 


@app.route("/register", methods=["GET", "POST"])
def register():
	is_username_taken = False
	is_email_taken = False
	password_length_error = False
	password_match_error = False
	is_email_invalid = False
	
	if request.method == "POST":
		# Check if passwords match
		if request.form.get("password") != request.form.get("confirm_password"):
			password_match_error = True

		# Check if password is between 8 and 32 characters
		if len(request.form.get("password")) < 8 or len(request.form.get("password")) > 32:
			password_length_error = True

		records = dbmanager.read_records()
		
		for record in records:
			# Check if username or email is taken
			if record["username"] == request.form.get("username"):
				is_username_taken = True
				break
			if record["email"] == request.form.get("email"):
				is_email_taken = True
				break

			# Check if email is valid
			if re.search("^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$", request.form.get("email")) == None:
				is_email_invalid = True
				break
		
		# Create account and store to CSV if no errors
		if not is_username_taken and not is_email_taken and not is_email_invalid and not password_length_error and not password_match_error:
			salt = bcrypt.gensalt()
			dbmanager.create_record({ "username": request.form.get("username"), "email": request.form.get("email"), "password": bcrypt.hashpw(request.form.get("password").encode("utf-8"), salt).decode("utf-8"), "salt": salt.decode("utf-8") })
			return redirect("/login")
			
	# Render register page with error messages if unsuccessful
	return render_template("register.html", username_taken=is_username_taken, email_invalid=is_email_invalid, email_taken=is_email_taken, password_length_error=password_length_error, password_match_error=password_match_error)



@app.route("/welcome")
def welcome():
	return render_template("welcome.html")

if __name__ == '__main__':
	app.run(debug=True)