import melons
from flask import Flask, render_template, redirect, flash, request, session
import jinja2
from forms import LoginForm
import customers


app = Flask(__name__) #this instatiates Flask class
app.secret_key = 'dev'
app.jinja_env.undefined = jinja2.StrictUndefined #this is for debugging purposes

@app.route('/') #routes or endpoints
def home():
    return render_template('base.html') #render template function searches for this file and navigates there

@app.route('/melons') #these are the endpoints
def all_melons(): #these are the view functions
    melon_list = melons.get_all()
    return render_template('all_melons.html', melon_list=melon_list) #first paramater is template location to be rendered, second paramter is the name of paramater and what we are assigning to that param, which is the context of what should be displayed on the page while using jinja)
    # return render_template('all_melons.html',melon_list=get_all()) *****QUESTION what is the difference between this and line above? why do we have to assign something to it in the above?

@app.route('/melon/<melon_id>')
def melon_details(melon_id):
    melon_information = melons.get_by_id(melon_id)
    return render_template('melon_details.html', melon_information=melon_information)

@app.route('/add_to_cart<melon_id>')
def add_to_cart(melon_id):
    if 'username' not in session:
        return redirect('/login')
    
    if 'cart' not in session: #session is something in python that is a default setting. A session is always running.
        #we are saying look for the key 'cart' in session, since session is a dict
        session['cart'] = {} #if key 'cart' is not in session dict, then create a key called 'cart' and set it as another empty dict
    cart = session['cart'] #we are then assigning this empty dict (which has a key parent called 'cart') to a variable


    cart[melon_id] = cart.get(melon_id, 0) + 1 #in cart, look for key called melon_id. We are getting this melon_id from url variable which is being inputted as the function param
    #then we are saying, get that melon_id and if this key melon_id doesn't exist in the cart, then the value is 0. We are then adding 1 each time this is called.
    session.modified = True
    flash(f'Melon {melon_id} added to cart')
    # print(cart)

    return redirect("/cart")

@app.route('/cart')
def cart_details():
    
    if 'username' not in session:
        return redirect('/login')
    
    order_total = 0
    cart_melons = []
    cart = session.get('cart', {}) #we are storing this cart session in a local variable

    for melon_id, quantity in cart.items():
        melon = melons.get_by_id(melon_id) #for each melon_id, get melon object from melons.py file using get_By_id function and store it in the variable melons
        #we are storing dicts (the original melon dicts from melons.py variable) in this local melon variable

        total_cost = quantity * melon.price
        order_total += total_cost

        melon.quantity = quantity
        melon.total_cost = total_cost

        cart_melons.append(melon)

    return render_template('cart.html', cart_melons=cart_melons, order_total=order_total)


@app.route('/empty-cart')
def empty_cart():
    session['cart'] = {}
    return redirect('/cart')

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user into site."""
    form = LoginForm(request.form) #we are instantiating LoginForm and passing form into a template
    #we pass request.form into LoginForm because we are submitting login using a POST request

    if form.validate_on_submit():
        # Form has been submitted with valid data
        username = form.username.data
        password = form.password.data

        # Check to see if a registered user exists with this username
        user = customers.get_by_username(username)

        if not user or user['password'] != password:
            flash('Invalid username or password')        
            return redirect('/login')

        # Store username in session to keep track of logged in user
        session['username'] = user['username']
        flash('Logged in')
        return redirect('/melons')
   
    # Form has not been submitted or data was not valid
    return render_template("login.html", form=form)

@app.route('/logout')
def logout():
    del session['username']
    flash('Logged out')
    return redirect('/login')

@app.errorhandler(404)
def error(e):
    return render_template('error.html')

if __name__ == '__main__':
    app.env = 'development' #this says we are in a devlopment environment instead of a production environment
    app.run(debug=True, port=8000, host='localhost') #this is how we run our flask server
    #debug is for helping with debuggin in development environment, port and host shows how to change these