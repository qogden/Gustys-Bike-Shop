import os
import psycopg2
import psycopg2.extras

from flask import Flask, render_template, request, session
app = Flask(__name__)

app.secret_key = os.urandom(24).encode('hex')
app.config['SECRET_KEY'] = 'secret!'

def connectToDB():
  connectionString = 'dbname=bikes user=biker password=bike123 host=localhost'
  print connectionString
  try:
    return psycopg2.connect(connectionString)
  except:
    print("Can't connect to database")

@app.route('/')
def index():
	return render_template('index.html')
	
@app.route('/login.html')
def login():
	return render_template('login.html')

@app.route('/account.html')
def account():
	conn = connectToDB()
	cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
	
	return render_template('account.html')	

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

@app.route('/blog.html')
def blog():
	return render_template('blog.html')

# start the server
if __name__ == '__main__':
    app.run(host=os.getenv('IP', '0.0.0.0'), port =int(os.getenv('PORT', 8080)), debug=True)