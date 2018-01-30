from flask import Flask, render_template, request, jsonify, redirect, send_file
import pandas as pd
import yaml
from recommender_model import RecommenderModel
from io import BytesIO
from pathlib import Path
import base64

default_lat = 47.6130285
default_lng = -122.3420645

app = Flask(__name__)
df = pd.read_csv('../data/df_with_features.csv', index_col=0)
mapping_df = pd.read_csv('../data/mapping_df.csv', index_col=0)
model = RecommenderModel(df, mapping_df)

@app.route('/')
def index():
    return render_template('main.html', features=mapping_df.columns)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/tech')
def tech():
    return render_template('tech.html')

#This works with form input
@app.route('/submit', methods=['GET', 'POST'])
def submit():
    f1 = tuple((float(request.form['f1_weight']), request.form['feature1']))
    f2 = tuple((float(request.form['f2_weight']), request.form['feature2']))
    f3 = tuple((float(request.form['f3_weight']), request.form['feature3']))
    r = float(request.form['range'])
    if len(request.form['coord']) > 0:
        lat = request.form['coord'].split(',')[0]
        lng = request.form['coord'].split(',')[1]
    else:
        lat = default_lat
        lng = default_lng
        r = 20
    recs = model.recommend(f1, f2, f3, lat, lng, r).to_dict('records')
    for rec in recs:
        rec['split_address'] = rec['address'].replace(' ', '+') + '+seattle'
    return render_template('recommendations.html', recs=recs)

# @app.route('/submit', methods=['GET', 'POST'])
# def submit():
#     user_info = request.json
#     print(user_info)
#     f1 = tuple((float(user_info['f1_weight']), user_info['f1_name']))
#     f2 = tuple((float(user_info['f2_weight']), user_info['f2_name']))
#     f3 = tuple((float(user_info['f3_weight']), user_info['f3_name']))
#     lat = user_info['coord'].split(',')[0]
#     lng = user_info['coord'].split(',')[1]
#     r = float(user_info['range'])
#     recs = model.recommend(f1, f2, f3, lat, lng, r).to_dict('records')
#     for rec in recs:
#         rec['split_address'] = rec['address'].replace(' ', '+') + '+seattle'
#     return render_template('recommendations.html', recs=recs)

if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True, debug=True)
