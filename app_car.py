import numpy as np
from flask import Flask, request, render_template
import joblib

app = Flask(__name__)
model = joblib.load('car_price_prediction.pkl')


@app.route('/')
def home():
    return render_template('index_car.html')


@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        Year = int(request.form['Year'])
        Present_Price = float(request.form['Present_Price'])
        Kms_Driven = int(request.form['Kms_Driven'])
        Kms_Driven2 = np.log(Kms_Driven)
        Owner = int(request.form['Owner'])
        Fuel_Type_Petrol = request.form['Fuel_Type_Petrol']
        if Fuel_Type_Petrol == 'Petrol':
            Fuel_Type_Petrol = 1
            Fuel_Type_Disel = 0
        else:
            Fuel_Type_Petrol = 0
            Fuel_Type_Disel = 1
        Year = 2020 - Year
        Seller_Type_Individual = request.form['Seller_Type_Individual']
        if Seller_Type_Individual == 'Individual':
            Seller_Type_Individual = 1
        else:
            Seller_Type_Individual = 0
        Transmission_Manual = request.form['Transmission_Manual']
        if Transmission_Manual == 'Manual':
            Transmission_Manual = 1
        else:
            Transmission_Manual = 0
        prediction = model.predict([[Present_Price, Kms_Driven2, Owner, Year, Fuel_Type_Disel, Fuel_Type_Petrol, Seller_Type_Individual, Transmission_Manual]])
        output = round(prediction[0], 2)
        if output < 0:
            return render_template('index_car.html', prediction_text='Sorry! You cannot sell this Car')
        else:
            return render_template('index_car.html', prediction_text='You can sell the car at Rs.{} lakhs'.format(output))
    else:
        render_template('index_car.html')


if __name__ == '__main__':
    app.run(debug=True)