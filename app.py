import os

from bson.objectid import ObjectId
from flask import Flask, redirect, render_template, request, url_for
from pymongo.errors import PyMongoError
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
  
app = Flask(__name__) 
  
# MongoDB connection setup
username = os.environ["MONGODB_USERNAME"]
password = os.environ["MONGODB_PASSWORD"]
db_name = os.environ["MONGODB_DB_NAME"]
host = os.environ["MONGODB_HOST"]
app_name = os.environ["MONGODB_APP_NAME"]

uri = (
    f"mongodb+srv://{username}:{password}"
    f"@{host}/?retryWrites=true&w=majority&appName={app_name}"
) 


# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))


# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Successfully connected to MongoDB!")
except PyMongoError as err:
    print(f"MongoDB connection error: {err}")
    raise

#client = MongoClient(host='test_mongodb', port=27017, username='root', password='pass', authSource="admin") # Local Connection 
db = client.mytododb 
students_collection = db.students   
  
@app.route('/pupil') 
def home(): 
    students = students_collection.find() 
    return render_template('index.html', students=students)  
 
@app.route('/pupil_add_student', methods=['POST']) 
def add_student(): 
    if request.method == 'POST': 
        student_data = { 
            'fname': request.form['fname'], 
            'lname': request.form['lname'], 
            'Gender': request.form['Gender'], 
            'ID': request.form['ID'], 
            'Subject': request.form['Subject'],
            'phone': request.form['phone'],
            'AdminDate': request.form['AdminDate']
        } 
        students_collection.insert_one(student_data) 
    return redirect(url_for('home')) 
    
@app.route('/pupil_delete_student/<student_id>', methods=['GET']) 
def delete_student(student_id): 
	students_collection.delete_one({'_id': ObjectId(student_id)}) 
	return redirect(url_for('home')) 




if __name__ == '__main__': 
    app.run(host='0.0.0.0', debug=False,port=8002) 

''' 
 app.run(host='0.0.0.0', debug=False,port=3000) 
'''