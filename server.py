from flask import Flask
from flask_cors import CORS
import goodwill_api_post

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def pullData():
  return goodwill_api_post.Pull_items()

