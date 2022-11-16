import flask 
from flask import request,render_template,Flask
import requests

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "s9JFUuhkmDNPSXzHJy3xbwO4tfzjVkyaAL-KPk57G0Uy"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
 API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}


app = Flask(__name__)  # initialising flask app


@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')



@app.route('/predict', methods=['POST', 'GET'])
def predict():
    if request.method == 'POST':
        SELLER_TYPE = request.form['seller']
        ABTEST=request.form['abtest']
        VEHICLE_TYPE=request.form['vehicleType']
        YEAR_OF_REGISTRATION = int(request.form['yearOfRegistration'])
        POWER_IN_PS=float(request.form['powerPS'])
        KILOMETERS_DRIVEN=float(request.form['kilometer'])
        MONTH_OF_REGISTRATION=int(request.form['monthOfRegistration'])
        FUEL_TYPE= request.form['fuelType']
        NOT_REPAIRED_DAMAGE=request.form['notRepairedDamage']
        NUMBER_OF_PICTURES=int(request.form['nrOfPictures'])
        POSTAL_CODE=int(request.form['postalCode'])
        OFFER_TYPE=request.form['offerType_Gesuch']
        GEARBOX_MANUELL=request.form['gearbox_manuell']
        
        if SELLER_TYPE == 'private':
            SELLER_TYPE = 1
        else:
            SELLER_TYPE = 0
          



        if ABTEST == 'test':
            ABTEST = 0
        else:
            ABTEST = 1




        if VEHICLE_TYPE == 'limousine':
            VEHICLE_TYPE= 0
        elif VEHICLE_TYPE == 'kleinwagen':
            VEHICLE_TYPE = 1
        elif VEHICLE_TYPE == 'kombi':
            VEHICLE_TYPE = 2
        elif VEHICLE_TYPE == 'bus':
            VEHICLE_TYPE = 3
        elif VEHICLE_TYPE == 'carbio':
            VEHICLE_TYPE = 4
        elif VEHICLE_TYPE == 'coupe':
            VEHICLE_TYPE = 5
        elif VEHICLE_TYPE == 'suv':
            VEHICLE_TYPE = 6
        else :
            VEHICLE_TYPE =7



        if  FUEL_TYPE == 'benzin' :
            FUEL_TYPE == 0
        elif FUEL_TYPE == 'diesel' :
            FUEL_TYPE = 1
        elif FUEL_TYPE == 'lpg':
            FUEL_TYPE = 2   
        elif FUEL_TYPE == 'cng':
            FUEL_TYPE = 3
        elif FUEL_TYPE == 'hybrid':
            FUEL_TYPE =4
        elif FUEL_TYPE == 'andere':
            FUEL_TYPE  =5
        else:
            FUEL_TYPE = 6



        if NOT_REPAIRED_DAMAGE == 'nein':
            NOT_REPAIRED_DAMAGE = 0
        else:
            NOT_REPAIRED_DAMAGE = 1


        if OFFER_TYPE== 'Angebot':
            OFFER_TYPE = 0
        else:
            OFFER_TYPE = 1


        if GEARBOX_MANUELL == 'manuell':
            GEARBOX_MANUELL = 1
        else :
            GEARBOX_MANUELL = 0    

        X=[[SELLER_TYPE,ABTEST,VEHICLE_TYPE,YEAR_OF_REGISTRATION,POWER_IN_PS,KILOMETERS_DRIVEN,MONTH_OF_REGISTRATION,FUEL_TYPE,NOT_REPAIRED_DAMAGE,NUMBER_OF_PICTURES,POSTAL_CODE,OFFER_TYPE,GEARBOX_MANUELL]]
        # NOTE: manually define and pass the array(s) of values to be scored in the next line
        payload_scoring = {"input_data": [{"field":[[SELLER_TYPE,ABTEST,VEHICLE_TYPE,YEAR_OF_REGISTRATION,POWER_IN_PS,KILOMETERS_DRIVEN,MONTH_OF_REGISTRATION,FUEL_TYPE,NOT_REPAIRED_DAMAGE,NUMBER_OF_PICTURES,POSTAL_CODE,OFFER_TYPE,GEARBOX_MANUELL]],"values":X}]}

        response_scoring = requests.post('https://eu-de.ml.cloud.ibm.com/ml/v4/deployments/83fcc2c2-0f66-492b-b174-6eaa1d66b1fd/predictions?version=2022-11-12', json=payload_scoring,
        headers={'Authorization': 'Bearer ' + mltoken})
        print(response_scoring)
        prediction=response_scoring.json()
        print(prediction)
        predict=prediction['predictions'][0]['values'][0][0]
        

        return render_template('index.html', prediction_text="Predicted Price Of  Your  Car  Is {} €".format(predict))
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

