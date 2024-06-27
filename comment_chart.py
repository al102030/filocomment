from flask import Flask, render_template  # , url_for
from flask_pymongo import PyMongo
from datetime import datetime, timedelta


app = Flask(__name__)
app.config['SECRET_KEY'] = '42769ccab55c0fbad66dbc1c5ee13de15c123db174bc731988acbccfac3d667d'
app.config["MONGO_URI"] = "mongodb://localhost:27017/filoDB"

# SetUp PyMongo
mongodb_client = PyMongo(app)
my_db = mongodb_client.db
collection = my_db['comment']


date_str = "1398/05/25"

query = {
    'createDate': {'$gt': date_str}
}

comments = collection.find(query)
dates = [record for record in comments]

dates_dict = {}

for item in dates[::-1]:
    if item['createDate'] in dates_dict:
        dates_dict[item['createDate']] += 1
    else:
        dates_dict[item['createDate']] = 1
    if len(dates_dict) > 29:
        break

keys_list = list(dates_dict.keys())
values_list = list(dates_dict.values())

print(len(values_list))


@app.route("/")
def comment_chart():
    return render_template('chart.html', labels=keys_list[::-1], values=values_list[::-1], title='Timeline')


if __name__ == "__main__":
    app.run(debug=True)
