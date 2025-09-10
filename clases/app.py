from flask import Flask, jsonify, request
import math
from pymongo import MongoClient

app = Flask(__name__)
client=MongoClient("mongodb://localhost:27017/")
db = client ['microservicio']
divisas_collection = db["divisas"]

@app.route("/")
def hello_world():
    resultado="hola"
    return jsonify(resultado)

@app.route("/recibir_valor", methods=["POST"])
def recibe_valor():
    dato=request.get_json()
    digito=dato.get("valor")
    raiz=math.sqrt(digito)
    return jsonify(raiz)

@app.route("/contacto", methods=["GET",'POST'])
def about():
    if request.method=='POST':
     return "Formulario enviado correctamente"
    return 'Pagina de contacto'

@app.route("/paroImpar", methods=['POST'])
def paroimpar():
    dato=request.get_json()
    digito=dato.get('valor')
    if digito%2==0:
        return "el numero es par"
    return "el numero es impar"

@app.route("/divisas",methods=['POST'])
def divisas():
    data = request.get_json()
    result = divisas_collection.insert_one({
        "origen": data['origen'],
        "destino": data['destino'],
        "valor": float(data['valor'])
        })
    return jsonify({
        "mensaje":"Divisa guardada correctamente",
        "id": str(result.inserted_id)
    }),201

@app.route("/convertir",methods=['POST'])
def convertir():
    dato=request.get_json()
    origen = dato.get("origen")
    destino = dato.get("destino")
    cantidad = dato.get("cantidad")

    if not origen or not destino or not cantidad:
        return jsonify({"error":"Debe enviar origen, destino y cantidad"}),400
    
    tasa=divisas_collection.find_one({"origen":origen,"destino":destino})
    if not tasa:
        return jsonify({"error":f"No se encontro la tasa de {origen} a {destino}"}),404
    
    valor_unidad=tasa["valor"]
    resultado=float(cantidad)*valor_unidad

    return f"{cantidad} {origen} -> {resultado} {destino}"

    #return jsonify({"origen":origen,
     #               "destino":destino,
      #              "cantidad":cantidad,
    #                "valor_unidad":valor_unidad,
       #             "resultado":resultado}),200
    