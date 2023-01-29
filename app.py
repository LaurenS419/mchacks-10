from flask import Flask
from flask_cors import CORS, cross_origin
from flask import request

app = Flask(__name__)
cors = CORS(app)

app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/test')
@cross_origin()
def index():
    return "Hello, World!"

@app.route('/pdf-analysis', methods = ['POST'])
@cross_origin()
def pdf_analysis():
    
    
    
    
    if request.method == 'POST':
        data = request.form # a multidict containing POST data
        return "pdf"


if __name__ == "__main__":
    app.run(debug=True)
