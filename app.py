from flask import Flask,render_template,request
import jsonify
import requests
import pickle
import numpy as np
import sklearn
from sklearn.preprocessing import StandardScaler
from flask_mysqldb import MySQL
app = Flask(__name__)
app = Flask(__name__)
model=pickle.load(open('Logic.pkl' , 'rb'))
app.config['MYSQL_HOST']= "localhost"
app.config['MYSQL_USER']= "root"
app.config['MYSQL_PASSWORD']="rootpassword"
app.config['MYSQL_DB']="liverdata"
app.config['MYSQL_CURSORCLASS']='DictCursor'
mysql=MySQL(app)
@app.route('/',methods=['GET','POST'])
def Home():
    if request.method=='POST':
        user=request.form
        Age=user['Age']
        Gender=user['Gender_Female']
        Total_bilirubin=user['Bilirubin']
        Direct_bilirubin=user['DBilirubin']
        A_Phosphotase=user['Alkalin']
        Al_Aminotransferase=user['Alamine']
        Asparatate=user['Asparatate']
        Total_proteins=user['Proteins']
        Albumin=user['Albumin']
        A_Globulin=user['AGRatio']
        cur=mysql.connection.cursor()
        cur.execute("INSERT INTO liver(Age,Gender,Total_bilirubin,Direct_bilirubin,A_Phosphotase, Al_Aminotransferase,Asparatate,Total_proteins,Albumin,A_Globulin) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(Age,Gender,Total_bilirubin,Direct_bilirubin,A_Phosphotase, Al_Aminotransferase,Asparatate,Total_proteins,Albumin,A_Globulin))
        mysql.connection.commit()
        cur.close()
        return predict()
    return render_template('front.html')
standard_to=StandardScaler()
@app.route("/predict",methods=['POST'])
def predict():
    if request.method == 'POST':
        Age=int(request.form['Age'])
        Gender_Female=request.form['Gender_Female']
        if(Gender_Female=='Female'):
            Gender_Female=1
            Gender_Male=0
        else:
            Gender_Female=0
            Gender_Male=1
        Total_bilirubin=float(request.form['Bilirubin'])
        Direct_bilirubin=float(request.form['DBilirubin'])
        A_Phosphotase=float(request.form['Alkalin'])
        Al_Aminotransferase=float(request.form['Alamine'])
        Asparatate=float(request.form['Asparatate'])
        Total_proteins=float(request.form['Proteins'])
        Albumin=float(request.form['Albumin'])
        A_Globulin=float(request.form['AGRatio'])
        prediction=model.predict([[Age,Gender_Female,Gender_Male,Total_bilirubin,Direct_bilirubin,A_Phosphotase,Al_Aminotransferase,Asparatate,Total_proteins,Albumin,A_Globulin]])
        output=round(prediction[0],2)
        if output<10:
            print("probability of chance:",output)
            return render_template('positive.html',prediction_text="their is chance of getting liver disease")
        else:
            return render_template('high.html',prediction_text="their is chance of getting liver disease")
    else:
        return render_template('front.html')
if __name__=="__main__":
    app.run(debug=True)
