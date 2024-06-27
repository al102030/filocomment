from flask import Flask, render_template  # , url_for
from flask_pymongo import PyMongo


app = Flask(__name__)
app.config['SECRET_KEY'] = '42769ccab55c0fbad66dbc1c5ee13de15c123db174bc731988acbccfac3d667d'
app.config["MONGO_URI"] = "mongodb://localhost:27017/filoDB"

# SetUp PyMongo
mongodb_client = PyMongo(app)
my_db = mongodb_client.db
collection = my_db['comment']
cm = collection.find().limit(50)
posts = [record for record in cm]  # It's better to use list(data)

comments = collection.find()
dates = [record for record in comments]

dates_dict = {}

# while len(dates_dict) > 30:

for item in dates[::-1]:
    if item['createDate'] in dates_dict:
        dates_dict[item['createDate']] += 1
    else:
        dates_dict[item['createDate']] = 1
    if len(dates_dict) > 30:
        break

keys_list = list(dates_dict.keys())
values_list = list(dates_dict.values())

# print(values_list)


@app.route("/")
def comment_chart():
    return render_template('chart.html', labels=keys_list[::-1], values=values_list[::-1], title='Timeline')


@app.route("/comment")
def comment():
    return render_template('comment.html', posts=dates, title='List')


if __name__ == "__main__":
    app.run(debug=True)
