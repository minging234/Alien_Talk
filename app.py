from flask import request, Flask, jsonify, render_template
from alien_translator import AlienTranslator
from universe import UniverseGod
import util

app = Flask(__name__)

god = UniverseGod()


@app.route('/')
def index():
    return render_template('front.html')


@app.route('/encrypt', methods=['POST'])
def encrypt():
    item = request.form
    message = item['plaint_text']
    keyword = item['key']
    translator = AlienTranslator(keyword)
    return render_template('index.html', RESULT=translator.encrypt_to_code(message))


@app.route('/decrypt', methods=['POST'])
def decrypt():
    item = request.form
    code = item['cipher_text']
    keyword = item['key']
    translator = AlienTranslator(keyword)
    return render_template('index.html', RESULT=translator.decrypt_to_msg(code))


@app.route('/future_encrypt', methods=['POST'])
def future_encrypt():
    item = request.form
    message = item['plaint_text']
    keyword = item['key']
    date = item['date']

    translator = AlienTranslator(keyword)
    msg = translator.encrypt_to_code(message)
    code = god.gen_future_code(date, msg)
    return render_template('index.html', RESULT=code)


@app.route('/present_decrypt', methods=['POST'])
def present_decrypt():
    item = request.form
    code = item['code']
    keyword = item['key']
    date = item['date']

    date_signature = god.gen_passed_time_signature(date)

    if date_signature == "INVALID DATE":
        return render_template('index.html', RESULT="NOT TIME YET")

    time_translator = AlienTranslator(date_signature)
    message = time_translator.decrypt_to_msg(code)

    translator = AlienTranslator(keyword)
    message = translator.decrypt_to_msg(message)

    return render_template('index.html', RESULT=message)


@app.route('/universe_status', methods=['GET'])
def universe_status():
    return jsonify({'current_date': str(god.gen_current_time_signature()), "public_key": util.get_public_key()})


app.run(port=5000, host='0.0.0.0')
