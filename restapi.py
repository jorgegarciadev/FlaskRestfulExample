#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, request, jsonify, make_response
from flask_restful import Resource, Api
from sqlalchemy import create_engine
import codecs
engine = create_engine('sqlite:///csalud.db')

app = Flask(__name__)
api = Api(app)

class Provincias(Resource):

    def get(self):
        '''()->json
        Devuelve un JSON que contiene las provincias que aparacen en la base de datos
        '''
        conexion = engine.connect()
        peticion = conexion.execute("select distinct PROVINCIA from csalud")
        return make_response(jsonify({'provincias': \
         [i[0] for i in peticion.cursor.fetchall()]}), 200)

class Centros(Resource):

    def get(self, provincia):
        '''(str)->json
        Devuelve un JSON con los centros que están en la provicia proporcionada
        '''
        conexion = engine.connect()
        peticion = conexion.execute("select * from csalud where Provincia='%s'" \
            % provincia.upper())
        result = {'datos': [dict(zip(tuple (peticion.keys()) ,i)) for i in peticion.cursor]}
        return make_response(jsonify(result), 200)

api.add_resource(Provincias, '/provincias')    
api.add_resource(Centros, '/centros/<string:provincia>')

if __name__ == '__main__':
    app.run(debug = True)
