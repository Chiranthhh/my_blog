from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
from data import Articles
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt


blog = Flask(__name__)

# Config MySQL
blog.config['MYSQL_HOST'] = 'localhost'
blog.config['MYSQL_USER'] = 'root'
blog.config['MYSQL_PASSWORD'] = 'AnuuChii0614'
blog.config['MYSQL_DB'] = 'MySportsBlog'
blog.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# init MYSQL
mysql = MySQL(blog)

Articles = Articles()

@blog.route('/')
def index():
	return render_template('home.html')

@blog.route('/about')
def about():
	return render_template('about.html')

@blog.route('/articles')
def articles():
	return render_template('articles.html', articles = Articles)

@blog.route('/article/<string:id>/')
def article(id):
	return render_template('article.html', id = id)

class RegisterForm(Form):
	name = StringField('Name', [validators.Length(min=1, max=50)])
	username = StringField('Username', [validators.Length(min=4, max=25)])
	email = StringField('Email', [validators.Length(min=6, max=50)])
	password = PasswordField('Password', [
		validators.DataRequired(),
		validators.EqualTo('confirm', message='Passwords do not match')
	])
	confirm = PasswordField('Confirm Password')

@blog.route('/register', methods=['GET', 'POST'])
def register():
	form = RegisterForm(request.form)
	if request.method == 'POST' and form.validate():
		name = form.name.data
		email = form.email.data
		username = form.username.data
		password = sha256_crypt.encrypt(str(form.password.data))
		

		# Create cursor
		cur = mysql.connection.cursor()

		# Execute query 
		cur.execute("INSERT INTO users (name, email, username, password) VALUES (%s, %s, %s, %s)", (name, email, username, password))

		# Commit to DB
		mysql.connection.commit()

		# Close connection
		cur.close()

		flash('You are now registered and can log in', 'success')

		redirect(url_for('index'))
	return render_template('register.html', form=form)	

if __name__ == '__main__':
	blog.secret_key='secret123'
	blog.run(debug=True)