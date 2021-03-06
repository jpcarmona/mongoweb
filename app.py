from flask import Flask, redirect, render_template, request, session, url_for
from flask_pymongo import PyMongo
import os

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'webmongo'
mongo_ip = '192.168.1.32'
port = '27017'
app.secret_key = str(os.system('openssl rand -base64 24'))

# Configuración de conexión a la base de datos
app.config['MONGO_URI'] = 'mongodb://'+mongo_ip+':'+port+'/'+app.config['MONGO_DBNAME']
mongo = PyMongo(app)


#Ruta principal
@app.route('/', methods=['GET'])
def inicio():
	if session:
		return redirect('/data')
	else:
		return render_template('login.html',valor=False)


#Login
@app.route('/login', methods=['POST'])
def login():
	usuario = request.form.get('usuario')
	contra = request.form.get('pass')
	try:
		conexion=mongo.db.authenticate(usuario,contra)
	except:
		conexion=False
	if conexion:
		session['usuario']= usuario
		session['pass']=contra
		return redirect('/data')
	else:		
		return render_template('login.html',valor=True)


#Logout
@app.route('/logout', methods=['GET'])
def logout():
	session.clear()
	mongo.db.logout()
	return redirect('/')

# Envío de datos de los collections a la plantilla
@app.route('/data', methods=['GET'])
def data():
	usuario=(session['usuario'])
	collections=mongo.db.collection_names()
	datos={}
	for collection in collections:
		datos[collection]=list(mongo.db[collection].find())
	return render_template('index.html',usuario=usuario,datos=datos)

#if __name__ == '__main__':
#    app.run(debug=True)