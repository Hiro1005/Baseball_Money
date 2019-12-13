import numpy as np

def insert_csv(data):
    import csv
    import uuid
    tuid = str(uuid.uuid1())
    with open("./logs/"+tuid+".csv", "a") as f:
        writer = csv.writer(f, lineterminator='\n')
        writer.writerow(["battingavg", "OBR", "run", "hit", "double", "triple", "homerun", "RBI", "fourball", "strikeout", "stolen", "error"])
        writer.writerow(data)
    return tuid

def predictIris(params):
    from sklearn.externals import joblib
    # load the model
    forest = joblib.load('./model_baseball.sav') 
    # predict
    params = params.reshape(1,-1)
    pred = forest.predict(params)
    return pred

def getIrisName(irisId):
    return str(irisId[0] * 10000)

from flask import Flask, render_template, request, flash
from wtforms import Form, FloatField, SubmitField, validators, ValidationError

# App config.
DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '1005'

class IrisForm(Form):
    battingavg = FloatField("打率：batting avg(0〜1の値)",
                     [validators.InputRequired("all parameters are required!"),
                     validators.NumberRange(min=0, max=1)])
    OBR = FloatField("出塁率：OBR(0〜1の値)",
                     [validators.InputRequired("all parameters are required!"),
                     validators.NumberRange(min=0, max=1)])
    run = FloatField("得点：score(0以上の整数)",
                     [validators.InputRequired("all parameters are required!"),
                     validators.NumberRange(min=0, max=300)])
    hit = FloatField("ヒット数：hit(0以上の整数)",
                     [validators.InputRequired("all parameters are required!"),
                     validators.NumberRange(min=0, max=300)])
    double = FloatField("ツーベースヒット数：double(0以上の整数)",
                     [validators.InputRequired("all parameters are required!"),
                     validators.NumberRange(min=0, max=100)])
    triple = FloatField("スリーベースヒット数：triple(0以上の整数)",
                     [validators.InputRequired("all parameters are required!"),
                     validators.NumberRange(min=0, max=100)])
    homerun = FloatField("ホームラン数：homerun(0以上の整数)",
                     [validators.InputRequired("all parameters are required!"),
                     validators.NumberRange(min=0, max=100)])
    RBI = FloatField("打点：RBI(0以上の整数)",
                     [validators.InputRequired("all parameters are required!"),
                     validators.NumberRange(min=0, max=200)])
    fourball = FloatField("フォアボール数：fourball(0以上の整数)",
                     [validators.InputRequired("all parameters are required!"),
                     validators.NumberRange(min=0, max=100)])
    strikeout = FloatField("三振：strikeput(0以上の整数)",
                     [validators.InputRequired("all parameters are required!"),
                     validators.NumberRange(min=0, max=100)])
    stolen = FloatField("盗塁数：stolen(0以上の整数)",
                     [validators.InputRequired("all parameters are required!"),
                     validators.NumberRange(min=0, max=100)])
    error = FloatField("エラーの数：error(0以上の整数)",
                     [validators.InputRequired("all parameters are required!"),
                     validators.NumberRange(min=0, max=100)])
    submit = SubmitField("予測する：Predict")

@app.route('/', methods = ['GET', 'POST'])
def irisPred():
    form = IrisForm(request.form)
    if request.method == 'POST':
        if form.validate() == False:
            flash("You need all parameters")
            return render_template('irisPred.html', form = form)
        else:            
            battingavg = float(request.form["battingavg"])            
            OBR = float(request.form["OBR"])            
            run = float(request.form["run"])            
            hit = float(request.form["hit"])
            double = float(request.form["double"])            
            triple = float(request.form["triple"])            
            homerun = float(request.form["homerun"])            
            RBI = float(request.form["RBI"])
            fourball = float(request.form["fourball"])            
            strikeout = float(request.form["strikeout"])            
            stolen = float(request.form["stolen"])            
            error = float(request.form["error"])
            params = np.array([battingavg, OBR, run, hit, double, triple, homerun, RBI, fourball, strikeout, stolen, error])
            print(params)
            insert_csv(params)
            pred = predictIris(params)
            irisName = getIrisName(pred)
            
            return render_template('success.html', irisName=irisName)
    elif request.method == 'GET':
        return render_template('irisPred.html', form = form)

if __name__ == "__main__":
    app.debug = True
    # app.run(host='0.0.0.1')
    app.run(host='127.0.0.1', port=5000)
    
    
    

