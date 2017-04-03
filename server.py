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
	
@app.route('/login')
def login():
	return render_template('login.html')

@app.route('/account')
def account():
	return render_template('account.html')	

@app.route('/signup', methods=['POST', 'GET'])
def signup():
	conn = connectToDB()
	cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
	
	print(request.form['firstname'], request.form['lastname'], request.form['email'], request.form['password'], request.form['confirmpassword'])
	
	return render_template('signup.html')	
	
@app.route('/single')
def single():
	return render_template('single.html')
	
@app.route('/products')
def products():
	return render_template('products.html')

@app.route('/contact')
def contact():
	return render_template('contact.html')
	
@app.route('/cart')
def cart():
	return render_template('cart.html')

@app.route('/blog')
def blog():
	return render_template('blog.html')

# start the server
if __name__ == '__main__':
    app.run(host=os.getenv('IP', '0.0.0.0'), port =int(os.getenv('PORT', 8080)), debug=True)