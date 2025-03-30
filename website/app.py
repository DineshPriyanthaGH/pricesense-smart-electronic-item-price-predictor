import os
import pickle
import subprocess
from flask import Flask, render_template, request
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor

# Auto-install missing dependencies
try:
    import numpy as np
    from sklearn.ensemble import RandomForestRegressor  # Just to ensure sklearn is installed
except ImportError:
    print("Installing required dependencies...")
    subprocess.check_call(["pip", "install", "numpy", "scikit-learn", "flask"])

app = Flask(__name__, template_folder='templates')

# Categories under development
under_development = ["Camera", "Mobile Phone", "Smartphone", "Tablet", "Television"]

# Function to load the model and predict
def predict_price(lst):
    filename = 'model1/lappredictor.pickle'
    try:
        if not os.path.exists(filename):
            return "Error: Model file not found!"

        with open(filename, 'rb') as file:
            model = pickle.load(file)
        
        pred_value = model.predict([lst])
        return round(pred_value[0], 2)  # Round to 2 decimal places

    except Exception as e:
        return f"Error in prediction: {str(e)}"


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict')
def predict():
    item = request.args.get('item', '').lower()  # Normalize to lowercase

    # Add individual item checks for under-development pages
    if item == "mobile":
        return render_template('Mobilephone.html')  # Show Mobile phone under-development page

    if item in [x.lower() for x in under_development]:  # For other under-development items
        return render_template('under_development.html', item=item)  # Generic under-development page
    
    if item.lower() == "laptop":
        return render_template('laptop.html', pred=None)  # For laptop prediction page

    return render_template('404.html'), 404  # Custom 404 for unsupported items


@app.route('/predict/laptop', methods=['GET', 'POST'])
def predict_laptop():
    pred = None  # Default is None

    if request.method == 'POST':
        try:
            # Ensure all required fields exist
            required_fields = ['Ram', 'Weight', 'Touchscreen', 'Ips', 'Company', 'TypeName', 'OpSys', 'cpu_name', 'Gpu_name']
            for field in required_fields:
                if field not in request.form:
                    raise ValueError(f"Missing input: {field}")

            # Get user inputs
            Ram = request.form['Ram']
            Weight = request.form['Weight']
            Touchscreen = request.form['Touchscreen']
            Ips = request.form['Ips']
            Company = request.form['Company']
            TypeName = request.form['TypeName']
            OpSys = request.form['OpSys']
            cpu_name = request.form['cpu_name']
            Gpu_name = request.form['Gpu_name']

            # Create feature list
            feature_list = [
                int(Ram),
                float(Weight),
                1 if Touchscreen == 'Yes' else 0,
                1 if Ips == 'Yes' else 0
            ]

            # Define categorical options
            company_options = ['Acer', 'Apple', 'Asus', 'Dell', 'HP', 'Lenovo', 'MSI', 'Other', 'Toshiba']
            type_options = ['2 in 1 Convertible', 'Gaming', 'Netbook', 'Notebook', 'Ultrabook', 'Workstation']
            opsys_options = ['Linux', 'Mac', 'Other', 'Windows']
            cpu_options = ['AMD', 'Intel Core i3', 'Intel Core i5', 'Intel Core i7', 'Other']
            gpu_options = ['AMD', 'Intel', 'Nvidia']

            # One-hot encoding
            feature_list += [1 if item == Company else 0 for item in company_options]
            feature_list += [1 if item == TypeName else 0 for item in type_options]
            feature_list += [1 if item == OpSys else 0 for item in opsys_options]
            feature_list += [1 if item == cpu_name else 0 for item in cpu_options]
            feature_list += [1 if item == Gpu_name else 0 for item in gpu_options]

            # Predict the price
            predicted_value = predict_price(feature_list)

            # Convert to LKR (Assuming 1 USD = 300 LKR)
            if isinstance(predicted_value, (int, float)):  # Ensure no error message
                pred = predicted_value * 300  # Convert USD to LKR
            else:
                pred = predicted_value  # If error message, display as is

        except Exception as e:
            pred = f"Error: {str(e)}"

    return render_template('laptop.html', pred=pred)


# Custom 404 Page
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)
