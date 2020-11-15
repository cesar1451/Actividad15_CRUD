from flask import Flask, jsonify, request  
from conexion import crear_usuario, iniciar_sesion
from conexion import insertar_pelicula, get_peliculas, get_pelicula

app = Flask(__name__) #crear Entorno App de Flask con el nombre del archivo

@app.route("/api/v1/usuarios", methods=["POST"]) #Crear ruta y recibe un método
def usuario():
    if request.method == "POST" and request.is_json:
        try:
            data = request.get_json() #Guardar el json
            print(data)
            
            if crear_usuario(data['correo'], data['contrasenia']):
                return jsonify({"code": "ok"})  #Retornar un diccionario hacía el cliente
            else:
                return jsonify({"code": "existe"})
        
        except:
            return jsonify({"code": "error"})

@app.route("/api/v1/peliculas", methods=["POST", "GET"])
@app.route("/api/v1/peliculas/<int:id>", methods=["GET"])
def peliculas(id=None):
    if request.method == "POST" and request.is_json:
        try:
            data = request.get_json()
            print(data)
            if insertar_pelicula(data):
                return jsonify({"code": "ok"})
            else:
                return jsonify({"code": "no"})
        except:
            return jsonify({"code": "error"})
    elif request.method == "GET" and id is None:
        return jsonify(get_peliculas())     
    elif request.method == "GET" and id is not None:
        return jsonify(get_pelicula(id))     
      
@app.route("/api/v1/sesiones", methods=["POST"])
def sesion():
    if request.method == "POST" and request.is_json:
        try:
            data = request.get_json()
            correo = data['correo'] #Sacar los datos del json
            contra = data['contraseña']
            id, ok = iniciar_sesion(correo, contra)
            if ok:
                return jsonify({"code": "ok", "id": id})
            else:
                return jsonify({"code": "noexiste"})
        except:
            return jsonify({"code": "error"})
            
'''     
def usuarios():
    usuarios_list = get_usuarios() #Guardar usuario
    
    return jsonify(usuarios_list) #Conversion a json
'''

app.run(debug=True) #Lanzar el servidor y esperar peticiones
#Debug para cuando se modifique algo en el servidor se actualiza