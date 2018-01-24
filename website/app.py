from flask import Flask, render_template, request, jsonify
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
    print('submitting')
    data = request.json
    f1_name, f2_name, f3_name = str(data[f1_name], data[f2_name], data[f3_name])
    f1_weight, f2_weight, f3_weight = float(data[f1_weight], data[f2_weight],
                                          data[f3_weight])
    f1 = tuple(f1_weight, f1_name)
    f2 = tuple(f2_weight, f2_name)
    f3 = tuple(f3_weight, f3_name)
    recommendations = model.recommend(f1, f2, f3, lat, lng)
    return jsonify(recommendations)

if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True, debug=True)
