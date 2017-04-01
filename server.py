import os
from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def index():
	return render_template('index.html')
	
@app.route('/login.html')
def login():
	return render_template('login.html')
	
@app.route('/single.html')
def single():
	return render_template('single.html')
	
@app.route('/products.html')
def products():
	return render_template('products.html')

@app.route('/contact.html')
def contact():
	return render_template('contact.html')
	
@app.route('/cart.html')
def cart():
	return render_template('cart.html')
	
@app.route('/account.html')
def account():
	return render_template('account.html')


# start the server
if __name__ == '__main__':
    app.run(host=os.getenv('IP', '0.0.0.0'), port =int(os.getenv('PORT', 8080)), debug=True)