from flask import Flask
from flask import json
from flask import request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def api_root():
    if request.headers['Content-Type'] == 'application/json':        
        print('\n'*10)
        print(request.get_json())
        print('\n'*10)
        return '', 200
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
