from flask import Flask
from flask_restful import Resource, Api
from alien_translator import AlienTranslator

app = Flask(__name__)
api = Api(app)


translator = AlienTranslator()


class Student(Resource):
    def get(self, name):
        return {'student': translator.encrypt_to_code(name)}


api.add_resource(Student, '/student/<string:name>')

app.run(port=5000)
