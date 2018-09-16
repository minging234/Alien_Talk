from flask import Flask, render_template, request, jsonify
from flask_restful import Resource, Api
from alien_translator import AlienTranslator

app = Flask(__name__)
api = Api(app)


translator = AlienTranslator("hahaha")


class Student(Resource):
    def get(self, name):
        return {'student': translator.encrypt_to_code(name)}


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/front')
def front():
    return render_template('front.html')


@app.route('/test', methods=['POST'])
def text():
    print("got")
    return render_template('index.html', RESULT="🤗")



api.add_resource(Student, '/student/<string:name>')

app.run(port=5000)


