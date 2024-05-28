import os
from flask import Flask, request, jsonify, url_for, session, redirect, render_template, flash
# from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import MenuStructure


app = Flask(__name__)
app.secret_key = 'mysecretkey'
# app.url_map.strict_slashes = False
# CORS(app)
users = {
    'admin': {'username': 'admin', 'password': 'admin'}
}

example_menu = MenuStructure("Example")
salad = {
    "name": "Salad", 
    "description": ["lettuce", "tomato", "cilantro", "chicken"], 
    "price": 5.99, 
    "category": "starters"
    }

pho = {
    "name": "Pho", 
    "description": ["noodles", "ginger", "beef", "lime"], 
    "price": 7.99, 
    "category": "main course"
}

tiramisu = {
    "name": "tiramisu", 
    "description": ["mascarpone", "matcha"], 
    "price": 3.99, 
    "category": "desserts"
}

example_menu.add_dish(salad)
example_menu.add_dish(pho)
example_menu.add_dish(tiramisu)
# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
# @app.route('/')
# def sitemap():
#     return generate_sitemap(app)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = users.get(username)
        if user and user['password'] == password:
            session['username'] = username
            return redirect(url_for('admin'))
        else:
            flash('Invalid credentials')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

@app.route('/admin')
def admin():
    if 'username' not in session or session['username'] != 'admin':
        abort(403)
    dishes = example_menu.get_all_dishes()
    return render_template('admin.html', dishes=dishes)

@app.route('/dishes', methods=['GET'])
def get_all_dishes():
    dishes = example_menu.get_all_dishes()
    return jsonify(dishes), 200

@app.route('/dishes/<int:id>', methods=['GET'])
def get_single_dish(id):
    dish = example_menu.get_dish(id)
    return jsonify(dish), 200

@app.route('/create_dish', methods=['GET','POST'])
def create_dish():
    if 'username' not in session or session['username'] != 'admin':
        abort(403)
    if request.method == 'POST':
        if not request.form or 'name' not in request.form:
            abort(400)
        dish = {
            'name': request.form['name'],
            'description': request.form.get('description'),
            'price': float(request.form.get('price', 0.0)),
            'category': request.form['category']
        }
        added_dish = example_menu.add_dish(dish)
        return redirect(url_for('admin'))
    return render_template('create_dish.html')

@app.route('/update_dish/<int:id>', methods=['GET', 'POST'])
def update_dish(id):
    if 'username' not in session or session['username'] != 'admin':
        abort(403)
    dish = example_menu.get_dish(id)
    if request.method == 'POST':
        updated_dish = {}
        if 'name' in request.form:
            updated_dish['name'] = request.form['name']
        if 'description' in request.form:
            updated_dish['description'] = request.form.get('description')
        if 'price' in request.form:
            updated_dish['price'] = float(request.form.get('price', 0.0))
        if 'category' in request.form:
            updated_dish['category'] = request.form['category']
        example_menu.update_dish(id, updated_dish)
        return redirect(url_for('admin'))
    return render_template('update_dish.html', dish=dish)

@app.route('/delete_dish/<int:id>', methods=['GET', 'POST'])
def delete_dish(id):
    if 'username' not in session or session['username'] != 'admin':
        abort(403)
    if request.method == 'POST':
        example_menu.delete_dish(id)
        return redirect(url_for('admin'))
    return render_template('delete_dish.html', dish_id=id)
   

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)