from flask import Flask, render_template,json,request,send_file
from threading import Thread
from datetime import datetime
import os


from seam import *
from main import *

app = Flask(__name__,template_folder='')


@app.route('/')
def index():
  return render_template('Home.html')


@app.route('/user.json')
def get_user_data():
  with open('user.json', 'r') as file:
    return json.load(file)

@app.route('/log')
def log():
  filename = 'log.txt'
  # Provide the path to your text file
  filepath = './log.txt'
  return send_file(filepath, as_attachment=True)
@app.route('/update', methods=['POST'])
def update():
    request_data = request.get_json()
    if request_data['auth'] != os.environ['Auth']:
      return {"status":False,"data":'Auth Error'}
    with open('user.json', 'r') as file:
        data = json.load(file)
    
    if 'id' in request_data and 'date' in request_data:
      data[request_data['id']][0] = request_data['date']

    with open('user.json', 'w') as file:
        json.dump(data, file, indent=4)

    return {"status":True,"data":data}

def run():
  app.run(debug=False,host='0.0.0.0', port=8080)


t = Thread(target=run)
t.start()
t1 = Thread(target=seam_main)
t1.start()
t1 = Thread(target=main_main)
t1.start()

