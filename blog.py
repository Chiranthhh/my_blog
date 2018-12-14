from flask import Flask, render_template
from data import Articles

blog = Flask(__name__)

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

if __name__ == '__main__':
	blog.run(debug=True)