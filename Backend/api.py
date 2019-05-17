from flask import Flask
from flask import jsonify
from flask_cors import CORS
import index
import processor

app = Flask(__name__)
CORS(app)

@app.route("/<query>")
def hello(query):
	action = index.getAction(query)
	text = processor.process(action, query)
	return jsonify(text)
