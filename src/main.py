import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from supabase import create_client, Client
from config import Config

# Importações dos blueprints
from src.routes.user import user_bp
from src.routes.product import product_bp
from src.routes.client import client_bp
from src.routes.sale import sale_bp

# Inicializa o cliente Supabase
supabase: Client = create_client(Config.SUPABASE_URL, Config.SUPABASE_KEY)

app = Flask(__name__)
CORS(app) # Habilita CORS para todas as rotas

# Configurações do Flask
app.config["SUPABASE_CLIENT"] = supabase

# Registra os blueprints
app.register_blueprint(user_bp, url_prefix="/api")
app.register_blueprint(product_bp, url_prefix="/api")
app.register_blueprint(client_bp, url_prefix="/api")
app.register_blueprint(sale_bp, url_prefix="/api")

@app.route("/api/status", methods=["GET"])
def status():
    return jsonify({"status": "API is running!"}), 200

if __name__ == "__main__":
    app.run(debug=False)


