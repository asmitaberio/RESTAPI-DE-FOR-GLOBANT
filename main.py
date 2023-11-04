from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
import io
import csv
import os
import pandas as pd
from sqlalchemy import create_engine

app = Flask(__name__)

DEBUG = os.environ.get('DEBUG', 'True') == 'True'

app.config['JWT_SECRET_KEY'] = 'secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost/YOUR-DATABASE'

jwt = JWTManager(app)
db = SQLAlchemy(app)

class api_access(db.Model):
    __table_args__ = {'schema':'YOUR-SCHEMA'}
    USERNAME = db.Column(db.String(255), nullable=False, primary_key=True)
    PASSWORD = db.Column(db.String(255), nullable=False)
    ACCESS_ENABLED = db.Column(db.Integer, nullable=False)

    def __init__(self, USERNAME, PASSWORD, ACCESS_ENABLED):
        self.user = USERNAME
        self.pwd = PASSWORD
        self.access_enabled = ACCESS_ENABLED


@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')

    with app.app_context():
        data = api_access.query.all()
        for i in data:
            if username == i.USERNAME and password == i.PASSWORD and i.ACCESS_ENABLED == 1:
                access_token = create_access_token(identity=username)
                return {'access_token': access_token}, 200
            elif username != i.USERNAME or password != i.PASSWORD:
                return {'message':'Incorrect credentials'}, 401
            elif username == i.USERNAME and password == i.PASSWORD and i.ACCESS_ENABLED == 0:
                return {'message':'Access denied'}, 403
            else:
                return {'message':'User does not exist'}, 404

data = []

@app.route('/upload-data', methods=['POST'])
@jwt_required()
def upload_data():
    try:
        max_rows =  request.args.get('enable_max_rows', 'no')
        csv_file = request.files['csv_file']
        if not csv_file:
            return {'error':'CSV file was not given'}, 400
        
        csv_data = csv_file.read().decode('utf-8')
        csv_stream = io.StringIO(csv_data)
        csv_reader = csv.reader(csv_stream)

        for row in csv_reader:
            data.append(row)
        df = pd.DataFrame(data)
        if len(df.index) > 1000 and max_rows == 'no':
            return {'error':f'{csv_file.filename} dataset too large, must be less than 1000 rows or enable max_rows'}, 400
        else:
            dbpd = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
            conn = dbpd.connect()
            df.to_sql(csv_file.filename, con=conn, if_exists='fail', index=False, schema='HR')
            return {'message':'Data loaded'}, 200
    except Exception as e:
        return {'error':str(e)}, 500

@app.route('/hired_employees_2021_q', methods=['GET'])
@jwt_required()
def hired_employees_2021_q():
    try:
        dbpd = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
        conn = dbpd.connect()
        df = pd.read_sql('select * from YOUR-TABLE', con=conn).fillna(0).to_dict(orient='dict')
        return {'data':df}, 200
    except Exception as e:
        return {'error':str(e)}, 500

@app.route('/hired_by_dept_2021', methods=['GET'])
@jwt_required()
def hired_by_dept_2021():
    try:
        dbpd = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
        conn = dbpd.connect()
        df = pd.read_sql('select * from YOUR-TABLE', con=conn)
        df = df.loc[df['hired'] > df['hired'].mean()].to_dict(orient='dict')
        return {'data':df}, 200
    except Exception as e:
        return {'error':str(e)}, 500

if __name__ == '__main__':
    app.run(debug=DEBUG)