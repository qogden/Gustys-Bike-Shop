import os
import psycopg2
import psycopg2.extras
import uuid

#from flask.ext.socketio import SocketIO, emit
from flask import Flask, render_template, request, session
app = Flask(__name__)

app.secret_key = os.urandom(24).encode('hex')
app.config['SECRET_KEY'] = 'secret!'
#socketio = SocketIO(app)

def connectToDB():
  connectionString = 'dbname=bikes user=biker password=bike123 host=localhost'
  print connectionString
  try:
    return psycopg2.connect(connectionString)
  except:
    print("Can't connect to database")

@app.route('/')
def index():
	if("email" not in session):
	 	session['email'] = uuid.uuid1()
	 	loggedin = 'false'
	return render_template('index.html')
	
@app.route('/login')
def login():
	return render_template('login.html')
	
@app.route('/login', methods=['GET', 'POST'])
def access():
	conn = connectToDB()
	cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
	
	query = cur.mogrify("SELECT * FROM users WHERE email = %s", (request.form['email'], ))
	cur.execute(query)
	cur.fetchall()
	emailresults = cur.rowcount
	print (emailresults)
	conn.commit()
	
	noEmail = 'false'
	wrongPassword = 'false'
	print(request.form['password'])
	
	if(emailresults == 1):
		query = cur.mogrify("SELECT * FROM users WHERE email = %s AND password = crypt(%s, password)", (request.form['email'], request.form['password']))
		cur.execute(query)
		cur.fetchall()
		passwordresults = cur.rowcount
		conn.commit()
		loggedin = 'true'
		
		if(passwordresults == 1):
			query = cur.mogrify("SELECT * FROM employees WHERE email = %s", (request.form['email'], ))
			cur.execute(query)
			cur.fetchall()
			employeeresults = cur.rowcount
			conn.commit()
			
			if(employeeresults == 1):
				session['email'] = request.form['email']
				return render_template('timesheet.html', loggedin = loggedin)
			else:
				session['email'] = request.form['email']
				return render_template('index.html', loggedin = loggedin)
		else:
			wrongPassword = 'true'
			return render_template('login.html', wrongPassword = wrongPassword)
	else:
		noEmail = 'true'
		return render_template('login.html', noEmail = noEmail)

@app.route('/account')
def account():
	return render_template('account.html')	

@app.route('/signup', methods=['POST', 'GET'])
def signup():
	conn = connectToDB()
	cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
	
	print(request.form['firstname'], request.form['lastname'], request.form['email'], request.form['password'], request.form['confirmpassword'])
	
	noPassMatch = 'false'
	emailTaken = 'false'
	
	query = cur.mogrify("SELECT * FROM users WHERE email = %s", (request.form['email'], ))
	cur.execute(query)
	cur.fetchall()
	emailresults = cur.rowcount
	print (emailresults)
	conn.commit()
	
	if(emailresults != 0):
		emailTaken = 'true'
		message1='Email taken'
		print(message1)
		return render_template('account.html', emailTaken = emailTaken)
	
	if(request.form['password'] != request.form['confirmpassword']):
		noPassMatch = 'true'
		message1='Passwords do not match'
		print(message1)
		return render_template('account.html', noPassMatch = noPassMatch)
		
	try:
		session['email'] = request.form['email']
		loggedin = 'true'
		cur.execute("INSERT INTO users(email, password) VALUES(%s, crypt(%s, gen_salt('bf')))", (request.form['email'], request.form['password']))
		conn.commit()
		cur.execute("INSERT INTO customers(firstname, lastname, email) VALUES(%s, %s, (SELECT email FROM users WHERE email = %s))", (request.form['firstname'], request.form['lastname'], request.form['email']))
		conn.commit()
		return render_template('signup.html', loggedin = loggedin)
	except:
		print("ERROR inserting into customer")
		print("INSERT INTO users(email, password) VALUES(%s, crypt(%s, gen_salt('bf')))" % (request.form['email'], request.form['password']) )
		print("TRIED: INSERT INTO customers(firstname, lastname, email) VALUES(%s, %s, (SELECT email FROM users WHERE email = %s))" % (request.form['firstname'], request.form['lastname'], request.form['email']))
		conn.rollback()
		return render_template('account.html')
	conn.commit()
	
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
    
"""if __name__ == '__main__':
    socketio.run(app,host=os.getenv('IP', '0.0.0.0'), port =int(os.getenv('PORT', 8080)), debug=True)"""