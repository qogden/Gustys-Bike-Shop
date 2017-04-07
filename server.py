import os
import psycopg2
import psycopg2.extras
import uuid

from flask.ext.socketio import SocketIO, emit
from flask import Flask, render_template, request, session, redirect
app = Flask(__name__)

app.secret_key = os.urandom(24).encode('hex')
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

def connectToDB():
  connectionString = 'dbname=bikes user=biker password=bike123 host=localhost'
  print connectionString
  try:
    return psycopg2.connect(connectionString)
  except:
    print("Can't connect to database")

@socketio.on('connect')
def makeConnection():
    print('connected')

@app.route('/')
def index():
	if("email" not in session):
	 	session['email'] = uuid.uuid1()
	 	session['loggedin'] = 'false'
	 
	return render_template('index.html')

@app.route('/logout')
def logout():
	 session['email'] = ''
	 session['loggedin'] = 'false'
	 return render_template('index.html')

@app.route('/login')
def login():
	print(session['email'])
	return render_template('login.html')
	
@app.route('/login', methods=['POST'])
def access():
	conn = connectToDB()
	cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
	
	query = cur.mogrify("SELECT * FROM users WHERE email = %s", (request.form['email'], ))
	cur.execute(query)
	cur.fetchall()
	emailresults = cur.rowcount
	conn.commit()
	
	noEmail = 'false'
	wrongPassword = 'false'
	print(session['email'])
	
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
				session['loggedin'] = 'true'
				return render_template('timesheet.html')
			else:
				session['email'] = request.form['email']
				session['loggedin'] = 'true'
				return render_template('index.html')
		else:
			wrongPassword = 'true'
			return render_template('login.html', wrongPassword = wrongPassword)
	else:
		noEmail = 'true'
		return render_template('login.html', noEmail = noEmail)

@app.route('/account')
def account():
	return render_template('signup.html')	

@app.route('/signup')
def signup2():
	print(session['email'])
	return render_template('signup.html')

@app.route('/signup', methods=['POST'])
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
	conn.commit()
	
	print(session['email'])
	
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
		session['loggedin'] = 'true'
		cur.execute("INSERT INTO users(email, password) VALUES(%s, crypt(%s, gen_salt('bf')))", (request.form['email'], request.form['password']))
		conn.commit()
		cur.execute("INSERT INTO customers(firstname, lastname, email) VALUES(%s, %s, (SELECT email FROM users WHERE email = %s))", (request.form['firstname'], request.form['lastname'], request.form['email']))
		conn.commit()
		return render_template('signup2.html')
	except:
		print("ERROR inserting into customer")
		print("INSERT INTO users(email, password) VALUES(%s, crypt(%s, gen_salt('bf')))" % (request.form['email'], request.form['password']) )
		print("TRIED: INSERT INTO customers(firstname, lastname, email) VALUES(%s, %s, (SELECT email FROM users WHERE email = %s))" % (request.form['firstname'], request.form['lastname'], request.form['email']))
		conn.rollback()
		return render_template('signup.html')
	conn.commit()
	
@app.route('/single')
def single():
	return render_template('single.html')
	
@app.route('/account_info')
def account_info():
	return render_template('account_info.html')
	
@app.route('/account_info', methods=['GET', 'POST'])
def update_account_info():
	conn = connectToDB()
	cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
	
	query = cur.mogrify("SELECT * FROM customers WHERE email = %s", (request.form['email'], ))
	cur.execute(query)
	cur.fetchall()
	emailresults = cur.rowcount
	conn.commit()

	
@app.route('/products')
def products():
	return render_template('products.html')

@app.route('/contact')
def contact():
	return render_template('contact.html')
	
def addToCart(productid, quantity):
	conn = connectToDB()
	cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
	
	cur.execute("SELECT id FROM customers WHERE email = %s", (session['email'], ))
	customerid = cur.fetchall()
	print (customerid)
	conn.commit()
	
	cur.execute("INSERT INTO cart(customerid, day, productid, quantity) VALUES(%s, (SELECT CURRENT_DATE), %s, %s)", (customerid, productid, quantity))
	conn.commit()
	
	message='item has been added'
	return message

@app.route('/cart')
def cart():
	conn = connectToDB()
	cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
	
	cur.execute("SELECT id FROM customers WHERE email = %s", (session['email'], ))
	customerid = cur.fetchall()
	customerid = customerid[0][0]
	conn.commit()
	
	cur.execute("SELECT * FROM cart WHERE customerid = %s", (customerid, ))
	cart = cur.fetchall()
	conn.commit()
	
	subtotal = 0.00
	tax = 0.00
	shipping = 0.00
	total = 0.00
	
	i=0
	j=0
	k=0
	products = []
	for row in cart:
		c=cart[i]
		cur.execute("SELECT * FROM products WHERE id = %s", (c[3], ))
		item = cur.fetchall()
		conn.commit()
		print(i)
		for row in item:
			p=item[j]	
			items = [p[0], p[1], p[2], p[4], c[4]]
			subtotal = subtotal + float(p[4])
		products.append(items)
		i+=1
		
	print(products)
	if (subtotal != 0.00):
		shipping = 50.00
	tax = subtotal * 0.15
	tax = round(tax,2)
	total = subtotal+ tax + shipping
	
	subtotal = "{0:.2f}".format(subtotal)
	tax = "{0:.2f}".format(tax)
	shipping = "{0:.2f}".format(shipping)
	total = "{0:.2f}".format(total)
	
	session['total'] = total
	
	return render_template('cart.html', cart = products, total = total, subtotal = subtotal, tax = tax, shipping = shipping, count = i)

@socketio.on('cartqty')
def cartqty(productid, quantity):
	conn = connectToDB()
	cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
	print('cartqty')
	print(productid)
	print(quantity)
	
	if("email" not in session):
	 	cur.execute("SELECT id FROM customers WHERE email = %s", (session['customerid'], ))
		customerid = cur.fetchall()
		conn.commit()
	else:
		cur.execute("SELECT id FROM customers WHERE email = %s", (session['email'], ))
		customerid = cur.fetchall()
		conn.commit()
	customerid = customerid[0][0]
	print(customerid)
	cur.execute("UPDATE cart SET quantity = %s WHERE customerid = %s AND productid = '%s'", (quantity, customerid, productid))
	print('adjusted')
	conn.commit()
	emit('adjustedqty')
	#conn.commit()

@app.route('/cartrm', methods=['post'])
def cartrm():
	conn = connectToDB()
	cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
	print(1234)
	if("email" not in session):
	 	cur.execute("SELECT id FROM customers WHERE email = %s", (session['customerid'], ))
		customerid = cur.fetchall()
		conn.commit()
	else:
		cur.execute("SELECT id FROM customers WHERE email = %s", (session['email'], ))
		customerid = cur.fetchall()
		conn.commit()
		
	print('hey')
	customerid = customerid[0][0]
	productid = request.form['cartrm']
	
	cur.execute("DELETE FROM cart WHERE customerid = %s AND productid = %s", (customerid, productid))
	conn.commit()
	return redirect('/cart')


@app.route('/checkoutinfo')
def checkoutinfo():
	return render_template('checkoutinfo.html')

@app.route('/ordersummary')
def ordersummary():
	return render_template('ordersummary.html')

@app.route('/customerinfo')
def customerinfo():
	return render_template('customerinfo.html')

@app.route('/blog')
def blog():
	return render_template('blog.html')


# start the server
"""if __name__ == '__main__':
    app.run(host=os.getenv('IP', '0.0.0.0'), port =int(os.getenv('PORT', 8080)), debug=True)"""
    
if __name__ == '__main__':
    socketio.run(app,host=os.getenv('IP', '0.0.0.0'), port =int(os.getenv('PORT', 8080)), debug=True)