from flask import Flask, render_template, request, redirect, url_for
from twitter import scrape_trending_topics, collection
from bson.json_util import dumps
import json

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    data = dumps(collection.find().sort('_id', -1).limit(1))  # Get the latest document
    data = json.loads(data)[0]
    return render_template('index.html', data=data)

@app.route('/scrape', methods=['POST'])
def scrape():
    scrape_trending_topics()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)

