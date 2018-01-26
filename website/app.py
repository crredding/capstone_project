from flask import Flask, render_template, request, jsonify, redirect, send_file
import pandas as pd
import yaml
from recommender_model import RecommenderModel
from google_api_functions import *
from io import BytesIO
#from PIL import Image
from pathlib import Path
import base64

with open('/Users/ReddingSkinnyRobot/.secrets/google_api.yaml') as f:
    google_secrets = yaml.load(f)

app = Flask(__name__)
df = pd.read_csv('../data/df_with_features.csv', index_col=0)
mapping_df = pd.read_csv('../data/mapping_df.csv', index_col=0)
model = RecommenderModel(df, mapping_df)

#This is just for testing, before lat and lng incorporated into the model
lat, lng = 47.612133, -122.335908

with open('static/images/default_shop_image.jpg', 'rb') as f1:
    f2 = f1.read()
    default_shop_image = base64.b64encode(bytearray(f2))

@app.route('/')
def index():
    return render_template('main.html')

@app.route('/submit', methods=['GET', 'POST'])
def submit():
    f1 = tuple((float(request.form['f1_weight']), request.form['feature1']))
    f2 = tuple((float(request.form['f2_weight']), request.form['feature2']))
    f3 = tuple((float(request.form['f3_weight']), request.form['feature3']))
    r = float(request.form['range'])
    recs = model.recommend(f1, f2, f3, lat, lng, r).to_dict('records')
    for rec in recs:
        rec['split_address'] = rec['address'].replace(' ', '+') + '+seattle'
    print(request.form)
    return render_template('recommendations.html', recs=recs)

if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True, debug=True)
