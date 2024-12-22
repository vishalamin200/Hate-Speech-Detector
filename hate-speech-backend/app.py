from flask import Flask, render_template, current_app
from flask_cors import CORS

from routes.hate_routes import hate_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(hate_bp)

@app.route('/')
def index():
    return "Server is running successfully!" 

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)