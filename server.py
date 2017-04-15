import os
import psycopg2
import psycopg2.extras

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
	totals = getTotals()
	emit('totals', totals)
	print('connected')

@app.route('/')
def index():
	if("email" not in session):
		session['email']=''
	 	session['loggedin'] = False
	 
	conn = connectToDB()
	cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

	cur.execute("SELECT * FROM products")
	stock = cur.fetchall()
	print stock
	conn.commit()
	
	i=0
	products = []
	for row in stock:
		for row in stock[i]:
			p = stock[i]
			items = {'id':p[0], 'name':p[1], 'image':p[2], 'price':p[4]}
		products.append(items)
		i+=1
	print products
	
	cur.execute("SELECT * FROM products WHERE producttype = (SELECT id FROM producttype WHERE producttype = 'bicycles')")
	stock = cur.fetchall()
	print stock
	conn.commit()
	
	i=0
	feature = []
	for row in stock:
		for row in stock[i]:
			p = stock[i]
			items = {'id':p[0], 'name':p[1], 'image':p[2]}
		feature.append(items)
		i+=1
	print products
	return render_template('index.html', stock = products)

@app.route('/logout')
def logout():
	session['email'] = ''
	session['loggedin'] = False
	 
	conn = connectToDB()
	cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

	cur.execute("SELECT * FROM products")
	stock = cur.fetchall()
	print stock
	conn.commit()
	
	i=0
	products = []
	for row in stock:
		for row in stock[i]:
			p = stock[i]
			items = {'id':p[0], 'name':p[1], 'image':p[2], 'price':p[4]}
		products.append(items)
		i+=1
	print products
	
	cur.execute("SELECT * FROM products WHERE producttype = (SELECT id FROM producttype WHERE producttype = 'bicycles')")
	stock = cur.fetchall()
	print stock
	conn.commit()
	
	i=0
	feature = []
	for row in stock:
		for row in stock[i]:
			p = stock[i]
			items = {'id':p[0], 'name':p[1], 'image':p[2]}
		feature.append(items)
		i+=1
	print products
	return render_template('index.html', stock = products)


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
	
	noEmail = False
	wrongPassword = False
	print(session['email'])
	
	if(emailresults == 1):
		query = cur.mogrify("SELECT * FROM users WHERE email = %s AND password = crypt(%s, password)", (request.form['email'], request.form['password']))
		cur.execute(query)
		cur.fetchall()
		passwordresults = cur.rowcount
		conn.commit()
		loggedin = True
		
		if(passwordresults == 1):
			query = cur.mogrify("SELECT * FROM employees WHERE email = %s", (request.form['email'], ))
			cur.execute(query)
			cur.fetchall()
			employeeresults = cur.rowcount
			conn.commit()
			
			if(employeeresults == 1):
				session['email'] = request.form['email']
				session['loggedin'] = True
				session['employee'] = True
				return render_template('timesheet.html')
			else:
				session['email'] = request.form['email']
				session['loggedin'] = True
				session['employee'] = False
				#switch all unregistered user products onto the customer
				
				cur.execute("SELECT * FROM products")
				stock = cur.fetchall()
				print stock
				conn.commit()
				
				i=0
				products = []
				for row in stock:
					for row in stock[i]:
						p = stock[i]
						items = {'id':p[0], 'name':p[1], 'image':p[2], 'price':p[4]}
					products.append(items)
					i+=1
				print products
				
				cur.execute("SELECT * FROM products WHERE producttype = (SELECT id FROM producttype WHERE producttype = 'bicycles')")
				stock = cur.fetchall()
				print stock
				conn.commit()
				
				i=0
				feature = []
				for row in stock:
					for row in stock[i]:
						p = stock[i]
						items = {'id':p[0], 'name':p[1], 'image':p[2]}
					feature.append(items)
					i+=1
				print products
				return render_template('index.html', stock = products)
				
		else:
			wrongPassword = True
			return render_template('login.html', wrongPassword = wrongPassword)
	else:
		noEmail = True
		return render_template('login.html', noEmail = noEmail)

@app.route('/signup')
def signup2():
	print(session['email'])
	return render_template('signup.html')

@app.route('/signup', methods=['POST'])
def signup():
	conn = connectToDB()
	cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
	
	print(request.form['firstname'], request.form['lastname'], request.form['email'], request.form['password'], request.form['confirmpassword'])
	
	noPassMatch = False
	emailTaken = False
	
	query = cur.mogrify("SELECT * FROM users WHERE email = %s", (request.form['email'], ))
	cur.execute(query)
	cur.fetchall()
	emailresults = cur.rowcount
	conn.commit()
	
	print(session['email'])
	
	if(emailresults != 0):
		emailTaken = True
		message1='Email taken'
		print(message1)
		return render_template('account.html', emailTaken = emailTaken)
	
	if(request.form['password'] != request.form['confirmpassword']):
		noPassMatch = True
		message1='Passwords do not match'
		print(message1)
		return render_template('account.html', noPassMatch = noPassMatch)
		
	try:
		session['email'] = request.form['email']
		session['loggedin'] = True
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
	
@app.route('/bikes')
def products():
	conn = connectToDB()
	cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

	cur.execute("SELECT * FROM products WHERE producttype = (SELECT id FROM producttype WHERE producttype = 'bicycles')")
	stock = cur.fetchall()
	print stock
	conn.commit()
	
	i=0
	products = []
	for row in stock:
		for row in stock[i]:
			p = stock[i]
			items = {'id':p[0], 'name':p[1], 'image':p[2], 'price':p[4]}
		products.append(items)
		i+=1
	print products
	
	return render_template('bikes.html', stock = products)
	
@app.route('/parts')
def parts():
	conn = connectToDB()
	cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

	cur.execute("SELECT * FROM products WHERE producttype = (SELECT id FROM producttype WHERE producttype = 'parts')")
	stock = cur.fetchall()
	print stock
	conn.commit()
	
	i=0
	products = []
	for row in stock:
		for row in stock[i]:
			p = stock[i]
			items = {'id':p[0], 'name':p[1], 'image':p[2], 'price':p[4]}
		products.append(items)
		i+=1
	print products
	return render_template('parts.html', stock = products)
	
@app.route('/tools')
def tools():
	conn = connectToDB()
	cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

	cur.execute("SELECT * FROM products WHERE producttype = (SELECT id FROM producttype WHERE producttype = 'tools')")
	stock = cur.fetchall()
	print stock
	conn.commit()
	
	i=0
	products = []
	for row in stock:
		for row in stock[i]:
			p = stock[i]
			items = {'id':p[0], 'name':p[1], 'image':p[2], 'price':p[4]}
		products.append(items)
		i+=1
	print products
	return render_template('tools.html', stock = products)

@app.route('/account', methods=['GET','POST'])
def update_account_info():
	# Placeholder Data
	info = {'fname':'John', 'lname':'Smith',
			'bstreet':'rocky road','bstreet2':'','bcity':'the ricksburg','bstate':'solid','bzip':'1234',
			'sstreet':'rocky road','sstreet2':'','scity':'the ricksburg','sstate':'solid','szip':'1234',
			'cardno':'1234567','csc':'666','exp':'now'}
	
	conn = connectToDB()
	cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
	print(session['email'])
	#user = User.get(request.form['uuid'])
	#query = cur.mogrify("SELECT firstname FROM customers WHERE email = %s", (session['email'],))
	cur.execute("SELECT firstname FROM customers WHERE email = %s", (session['email'],))
	info["fname"] = cur.fetchall()[0][0]
	cur.execute("SELECT lastname FROM customers WHERE email = %s", (session['email'],))
	info["lname"] = cur.fetchall()[0][0]
	
	cur.execute("SELECT bstreet1 FROM customers WHERE email = %s", (session['email'],))
	info["bstreet"] = cur.fetchall()[0][0]
	cur.execute("SELECT bstreet2 FROM customers WHERE email = %s", (session['email'],))
	info["bstreet2"] = cur.fetchall()[0][0]
	cur.execute("SELECT bcity FROM customers WHERE email = %s", (session['email'],))
	info["bcity"] = cur.fetchall()[0][0]
	cur.execute("SELECT bstate FROM customers WHERE email = %s", (session['email'],))
	info["bstate"] = cur.fetchall()[0][0]
	cur.execute("SELECT bzip FROM customers WHERE email = %s", (session['email'],))
	info["bzip"] = cur.fetchall()[0][0]
	
	cur.execute("SELECT sstreet1 FROM customers WHERE email = %s", (session['email'],))
	info["sstreet"] = cur.fetchall()[0][0]
	cur.execute("SELECT sstreet2 FROM customers WHERE email = %s", (session['email'],))
	info["sstreet2"] = cur.fetchall()[0][0]
	cur.execute("SELECT scity FROM customers WHERE email = %s", (session['email'],))
	info["scity"] = cur.fetchall()[0][0]
	cur.execute("SELECT sstate FROM customers WHERE email = %s", (session['email'],))
	info["sstate"] = cur.fetchall()[0][0]
	cur.execute("SELECT szip FROM customers WHERE email = %s", (session['email'],))
	info["szip"] = cur.fetchall()[0][0]
	
	cur.execute("SELECT cardno FROM customers WHERE email = %s", (session['email'],))
	info["cardno"] = cur.fetchall()[0][0]
	cur.execute("SELECT csc FROM customers WHERE email = %s", (session['email'],))
	info["csc"] = cur.fetchall()[0][0]
	cur.execute("SELECT exp FROM customers WHERE email = %s", (session['email'],))
	info["exp"] = cur.fetchall()[0][0]
	

#	if request.method == 'POST':
#    	user = User.get(request.form['uuid'])
	#query = cur.mogrify("UPDATE customers SET firstname = 'Ia' where firstname = 'Ian'")
	#query = cur.mogrify("UPDATE customers SET firstname = 'Iand' where email = 'ian.carlyle@yahoo.com'")
#	print(query)
#	cur.execute(query)
#	cur.fetchall()
#	conn.commit()
	
	
#	session['fname'] = 'Nullname'
#	session['lname'] = 'Null_last'
#	print(session['fname'])

#	try:
#		cur.execute("INSERT INTO customers(firstname, lastname, email) VALUES(%s, %s, (SELECT email FROM users WHERE email = %s))", (request.form['firstname'], request.form['lastname'], request.form['email']))
#		conn.commit()
#		return render_template('signup2.html')
#	except:
#		print("ERROR updating customer info")
#		print("TRIED: INSERT INTO customers(firstname, lastname, email) VALUES(%s, %s, (SELECT email FROM users WHERE email = %s))" % (request.form['firstname'], request.form['lastname'], request.form['email']))
#		conn.rollback()
#		return render_template('account.html')
#	conn.commit()
	
	
	
	#query = cur.mogrify("SELECT * FROM users WHERE email = %s", (request.form['fname'], ))
	#cur.execute(query)
	#cur.fetchall()
	#results = cur.rowcount
	#conn.commit()
	
	return render_template('account.html', info=info)

@app.route('/contact')
def contact():
	return render_template('contact.html')
	
@socketio.on('addToCart')	
def addToCart(productid, quantity):
	conn = connectToDB()
	cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
	print(productid, quantity)
	print(session['email'])
	
	cur.execute("SELECT id FROM customers WHERE email = %s", (session['email'], ))
	customerid = cur.fetchall()
	print (customerid)
	conn.commit()
	
	cur.execute("INSERT INTO cart(customerid, day, productid, quantity) VALUES(%s, (SELECT CURRENT_DATE), %s, %s)", (customerid, productid, quantity))
	conn.commit()
	
	message='item has been added'
	emit('added')

@socketio.on('cart')
def cart():
	totals = getTotals()
	emit('totals', totals)

@app.route('/cart')
def cart1():
	products = getProducts()
	totals = getTotals()
	return render_template('cart.html', cart = products, totals = totals)
	
@socketio.on('cartqty')
def cartqty(productid, quantity):
	conn = connectToDB()
	cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
	print('cartqty')
	print(productid)
	print(quantity)
	
	cur.execute("SELECT id FROM customers WHERE email = %s", (session['email'], ))
	customerid = cur.fetchall()
	conn.commit()
	
	customerid = customerid[0][0]
	print(customerid)
	cur.execute("UPDATE cart SET quantity = %s WHERE customerid = %s AND productid = '%s'", (quantity, customerid, productid))
	print('adjusted')
	conn.commit()
	
	totals=getTotals()
	
	emit('totals', totals)

@app.route('/cartrm', methods=['post'])
def cartrm():
	conn = connectToDB()
	cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

	cur.execute("SELECT id FROM customers WHERE email = %s", (session['email'], ))
	customerid = cur.fetchall()
	conn.commit()
		
	customerid = customerid[0][0]
	productid = request.form['cartrm']
	
	cur.execute("DELETE FROM cart WHERE customerid = %s AND productid = %s", (customerid, productid))
	conn.commit()
	return redirect('/cart')

@app.route('/ordersummary')
def ordersummary():
	
	userinfo = getUserInfo()
	products = getProducts()
	totals = getTotals()
	
	return render_template('ordersummary.html', info = userinfo, cart = products, totals = totals)

def getUserInfo():
	conn = connectToDB()
	cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
	
	cur.execute("SELECT * FROM customers WHERE email = %s", (session['email'], ))
	r = cur.fetchall()
	conn.commit()
	
	i = 0
	j = 0
	for row in r:
		for now in r[i]:
			if r[i][j] == None:
				r[i][j] = ''
			print r[i][j]
			j+=1
		i+=1

	cur.execute("SELECT cardno, csc FROM customers WHERE email = %s", (session['email'], ))
	r2 = cur.fetchall()
	conn.commit()

	

	userInfo = {'first': r[0][1], 'last':r[0][2], 'email':r[0][3], 'bstreet': r[0][4], 'bstreet2': r[0][5], 'bcity':r[0][6], 'bstate':r[0][7], 'bzip':r[0][8], 'sstreet': r[0][9], 'sstreet2': r[0][10], 'scity':r[0][11], 'sstate':r[0][12], 'szip':r[0][13], 'cardno':r[0][14], 'csc':r[0][15], 'exp':r[0][16]}
		
	return userInfo

def getProducts():
	conn = connectToDB()
	cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
	
	cur.execute("SELECT id FROM customers WHERE email = %s", (session['email'], ))
	customerid = cur.fetchall()
	print('getProducts CustomerID;', customerid)
	customerid = customerid[0][0]
	conn.commit()

	cur.execute("SELECT * FROM cart WHERE customerid = %s", (customerid, ))
	cart = cur.fetchall()
	print cart
	conn.commit()
	
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
		products.append(items)
		i+=1
	print products
	return products

def getTotals():
	conn = connectToDB()
	cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

	if (session['loggedin'] and session['employee'] == False):
		print(session['email'])
		
		query = cur.mogrify("SELECT id FROM customers WHERE email = %s", (session['email'], ))
		print(query)
		cur.execute(query)
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
		count = 0
		for row in cart:
			c=cart[i]
			cur.execute("SELECT * FROM products WHERE id = %s", (c[3], ))
			item = cur.fetchall()
			conn.commit()
			for row in item:
				p=item[j]	
				count = count + c[4]
				subtotal = (subtotal + float(p[4]))*float(c[4])
			i+=1
		
	else:
		subtotal = 0.00
		tax = 0.00
		shipping = 0.00
		total = 0.00
		count = 0
			
	if (subtotal != 0.00):
		shipping = 50.00
	tax = subtotal * 0.15
	tax = round(tax,2)
	total = subtotal+ tax + shipping
	
	subtotal = "{0:.2f}".format(subtotal)
	tax = "{0:.2f}".format(tax)
	shipping = "{0:.2f}".format(shipping)
	total = "{0:.2f}".format(total)
	
	totals={'total':total, 'subtotal':subtotal, 'tax':tax, 'shipping':shipping, 'count': count}
	
	return totals
	
@app.route('/orderconfirmation', methods = ['POST'])
def order():
	conn = connectToDB()
	cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
	
	firstname = request.form['firstname']
	lastname = request.form['lastname']
	email = request.form['email']
	
	bstreet = request.form['bstreet']
	bstreet2 = request.form['bstreet2']
	bcity = request.form['bcity']
	bstate = request.form['bstate']
	bzip = request.form['bzip']
	
	sstreet = request.form['sstreet']
	sstreet2 = request.form['sstreet2']
	scity = request.form['scity']
	sstate = request.form['sstate']
	szip = request.form['szip']
	
	cardno = request.form['cardno']
	csc = request.form['csc']
	exp = request.form['exp']
	
	#insert into orders
	query=cur.mogrify("Insert INTO orders(customerid, orderdate, firstname, lastname, email, bstreet, bstreet2, bcity, bstate, bzip, sstreet, sstreet2, scity, szip, cardno, csc, exp) VALUES ((SELECT id FROM customerid WHERE email = %s), (SELECT current_timestamp), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
	(session['email'], firstname, lastname, email, bstreet, bstreet2, bcity, bstate, bzip, sstreet, sstreet2, scity, szip, cardno, csc, exp))
	print(query)
	
	#insert into orderdetails using curval(orders_pid_seq)
	
	
	
	return render_template('orderconfirmation.html')

@app.route('/blog')
def blog():
	return render_template('blog.html')


# start the server
if __name__ == '__main__':
    socketio.run(app,host=os.getenv('IP', '0.0.0.0'), port =int(os.getenv('PORT', 8080)), debug=True)