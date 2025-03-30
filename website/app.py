from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict')
def predict():
    item = request.args.get('item', '')
    if item == "laptop":
        return render_template('laptop.html')  # Render Laptop Prediction Form
    return "Item not found", 404

@app.route('/predict/laptop', methods=['POST', 'GET'])
def predict_laptop():
    if request.method == 'POST':
        Ram= request.form['Ram']

        
       Weight = request.form['Weight'] 
        # Process the data and return the prediction
        
    

if __name__ == '__main__':
    app.run(debug=True)
