from flask import Flask,render_template,request,redirect

# Create Application
app = Flask(__name__)

# Create End Points or Route
@app.route('/')
def index():
    return '<h1>Hello World</h1>'

# Handle URL Parameters
@app.route('/handle_url_params')
def handle_params():
    pass



if __name__ in '__main__':
    app.run(host='127.0.0.1',port=5000,debug=True)

