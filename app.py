from flask import Flask, session, redirect, url_for, request, render_template, jsonify
from flask_session import Session  # Flask-Session extension
import csv, json

app = Flask(__name__)

# Secret key for session management
app.secret_key = 'your_secret_key_here'

# Session configuration (you can store sessions on the filesystem, database, etc.)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Reading from a CSV file
def read_csv(file_path):
    data = []
    with open(file_path, mode='r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data.append(row)
    return data

# Writing to a CSV file
def write_csv(file_path, data, fieldnames):
    with open(file_path, mode='w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)

def convert_csv_to_json(csv_file_path, json_file_path):
    data = []
    with open(csv_file_path, mode='r', encoding='utf-8') as csvfile:
        csv_reader = csv.DictReader(csvfile)
        for row in csv_reader:
            data.append(row)
    
    with open(json_file_path, mode='w', encoding='utf-8') as jsonfile:
        json.dump(data, jsonfile, ensure_ascii=False, indent=4)

def read_json(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as jsonfile:
            return json.load(jsonfile)
    except FileNotFoundError:
        return []

# Example usage
csv_file_path = 'data/products.csv'
json_file_path = 'data/products.json'
convert_csv_to_json(csv_file_path, json_file_path)

@app.route('/')
def index():
    products = read_json('data/products.json')
    return render_template('index.html', products=products)

@app.route('/add-to-cart/', methods=['POST'])
def add_to_cart():
    data = request.get_json() 
    product_id = data.get('product_id')
    if 'cart' not in session:
        session['cart'] = []
    
    session['cart'].append(product_id)
    session.modified = True
    
    return jsonify({"message": "Product added to cart", "cart": session['cart']})

@app.route('/cart')
def show_cart():
    cart_items = session.get('cart', [])
    return render_template('cart.html', cart_items=cart_items)


@app.route("/health",methods=['GET'])
def health():
    return "200"

if __name__ == '__main__':
    app.run(debug=True, port=3000)