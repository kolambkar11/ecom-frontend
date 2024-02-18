from flask import Flask, request, jsonify

app = Flask(__name__)

cart = []

@app.route("/health",methods=['GET'])
def health():
    return "2001"

@app.route("/add",methods=['GET','POST'])
def add_to_cart():
    id = request.args.get('id')
    product_id = request.args.get('product')
    print(id,product_id)
    cart.append()
    return jsonify

if __name__ == "__main__":
    app.run(debug=True,port=3000)