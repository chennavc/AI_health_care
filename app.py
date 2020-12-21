from flask import Flask, render_template, request
import jsonify
import requests
import pickle
import numpy as np
import sklearn
from sklearn.preprocessing import StandardScaler

app = Flask(__name__)

model = pickle.load(open('cancer_model.pkl', 'rb'))
kmodel = pickle.load(open('kidney_model.pkl', 'rb'))
hmodel=pickle.load(open('heart_model.pkl', 'rb'))



@app.route('/')
def start():
    return render_template('base.html')

@app.route('/cancer', methods=['GET','POST'])
def cancer():
    if request.method == 'POST':
        perimeter_worst=request.form['perimeter_worst']
        concave_points_mean=request.form['concave_points_mean']
        radius_worst=request.form['radius_worst']
        concave_points_worst=request.form['concave_points_worst']
        radius_mean=request.form['radius_mean']
        area_mean=request.form['area_mean']
        concavity_mean=request.form['concavity_mean']
        perimeter_mean=request.form['perimeter_mean']
        area_worst=request.form['area_worst']
        concavity_worst=request.form['concavity_worst']
       
        prediction=model.predict([[perimeter_worst,concave_points_mean,radius_worst,concave_points_worst,radius_mean,area_mean,concavity_mean,perimeter_mean,area_worst,concavity_worst]])
        output=prediction[0]
        if output== 0:
            return render_template('result.html',prediction_text="cancer negetive ")
        else:
            return render_template('result.html',prediction_text="cancer positive{}".format(output))
    else:
        return render_template('cancer.html')

@app.route('/kidney', methods=['GET','POST'])
def kidney():
    if request.method == 'POST':
        hypertension=request.form['hypertension']
        if(hypertension=='Yes'):
                hypertension=1
        else:
            hypertension=0  
        specific_gravity=request.form['specific_gravity']
        diabetes_mellitus=request.form['diabetes_mellitus']
        if(diabetes_mellitus=='Yes'):
            diabetes_mellitus=1
        else:
            diabetes_mellitus=0

        albumin=request.form['albumin']
        hemoglobin=request.form['hemoglobin']
        
        t=np.array([[hypertension,specific_gravity,diabetes_mellitus,albumin,hemoglobin]])
        prediction=kmodel.predict(t)
        print(prediction)
        output=prediction[0]
        if output== 0:
            return render_template('result.html',prediction_text="negetive ")
        else:
            return render_template('result.html',prediction_text="positive{}".format(output))
    else:
        return render_template('kidney.html')

@app.route('/heart', methods=['GET','POST'])
def heart():
    if request.method == 'POST':
        flourosopy=request.form['flourosopy']
        chest_pain_type=request.form['chest_pain_type']

        exang=request.form['exang']
        if(exang=='Yes'):
            exang=1
        else:
            exang=0

        thal=request.form['thal']
        thalach=request.form['thalach']
        
    
        prediction=hmodel.predict([[int(flourosopy),int(chest_pain_type),int(exang),int(thal),int(thalach)]])
        print(prediction)
        output=prediction[0]
        if output== 0:
            return render_template('result.html',prediction_text="negetive ")
        else:
            return render_template('result.html',prediction_text="positive{}".format(output))
    else:
        return render_template('heart.html')


if __name__ == '__main__':
    app.run(debug=True)