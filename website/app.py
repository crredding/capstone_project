from flask import Flask, render_template, request, jsonify, redirect
import pandas as pd

from recommender_model import RecommenderModel

app = Flask(__name__)
df = pd.read_csv('../data/df_with_features.csv', index_col=0)
mapping_df = pd.read_csv('../data/mapping_df.csv', index_col=0)
model = RecommenderModel(df, mapping_df)

#This is just for testing, before lat and lng incorporated into the model
lat, lng = 47.612133, -122.335908

@app.route('/')
def index():
    return render_template('main.html')

@app.route('/submit', methods=['POST'])
def submit():
    f1 = tuple((float(request.form['f1_weight']), request.form['feature1']))
    f2 = tuple((float(request.form['f2_weight']), request.form['feature2']))
    f3 = tuple((float(request.form['f3_weight']), request.form['feature3']))
    recommendations = model.recommend(f1, f2, f3, lat, lng)
    print(recommendations)
    return redirect('/')
    # return jsonify(recommendations)

if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True, debug=True)
