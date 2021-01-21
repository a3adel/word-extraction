from flask import Flask,request
from TaskImpl import TaskImpl
import json

app = Flask(__name__)

@app.route('/task', methods=['POST'])
def task():
    
    body = request.get_json()
    url = body['url']
    keywords = body['keywords']
    print(keywords)
    task = TaskImpl()
    result = task.run(url,keywords)
    response = app.response_class(
        response=json.dumps(result),
        mimetype='application/json'
    )
    return response