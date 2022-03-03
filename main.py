from flask import Flask, render_template, request
import jsonify
import requests
import pickle
import numpy as np
import sklearn
from sklearn.preprocessing import StandardScaler
app = Flask(__name__)
model = pickle.load(open('random_forest_regression_model.pkl', 'rb'))
@app.route('/',methods=['GET'])
def Home():
    return render_template('index.html')


standard_to = StandardScaler()
@app.route("/predict", methods=['POST'])
def predict():
    Fuel_Type_Diesel=0
    if request.method == 'POST':
        Year = int(request.form['Year'])

        km_driven=int(request.form['km_driven'])
        #Kms_Driven2=np.log(km_driven)

        engine = int(request.form['engine'])
        #engine2 = np.log(engine)

        Petrol=request.form['Petrol']
        if(Petrol=='Petrol'):
                Petrol=1
                Diesel=0
        else:
            Petrol=0
            Diesel=1
        age=2022-Year

        Manual=request.form['Manual']
        if(Manual=='Manual'):
            Manual=1
        else:
            Manual=0
        prediction=model.predict([[km_driven,engine,Manual,Diesel,Petrol,age]])
        output=round(prediction[0],2)
        if output<0:
            return render_template('index.html',prediction_texts="Sorry you cannot sell this car")
        else:
            return render_template('index.html',prediction_text="You Can Sell The Car at {}".format(output))
    else:
        return render_template('index.html')

if __name__=="__main__":
    app.run(debug=True)

