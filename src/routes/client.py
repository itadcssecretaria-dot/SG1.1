from flask import Blueprint, request, jsonify, current_app
from src.models import ClientCreate, ClientUpdate
from pydantic import ValidationError

client_bp = Blueprint("client_bp", __name__)

def get_supabase_client():
    return current_app.config["SUPABASE_CLIENT"]

@client_bp.route("/clients", methods=["GET"])
def get_clients():
    try:
        supabase = get_supabase_client()
        response = supabase.table("clients").select("*").execute()
        return jsonify(response.data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@client_bp.route("/clients/<client_id>", methods=["GET"])
def get_client(client_id):
    try:
        supabase = get_supabase_client()
        response = supabase.table("clients").select("*").eq("id", client_id).single().execute()
        return jsonify(response.data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@client_bp.route("/clients", methods=["POST"])
def create_client():
    try:
        client_data = ClientCreate(**request.get_json())
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400
    try:
        supabase = get_supabase_client()
        response = supabase.table("clients").insert(client_data.dict()).execute()
        return jsonify(response.data), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@client_bp.route("/clients/<client_id>", methods=["PUT"])
def update_client(client_id):
    try:
        client_data = ClientUpdate(**request.get_json())
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400
    try:
        supabase = get_supabase_client()
        response = supabase.table("clients").update(client_data.dict(exclude_unset=True)).eq("id", client_id).execute()
        return jsonify(response.data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@client_bp.route("/clients/<client_id>", methods=["DELETE"])
def delete_client(client_id):
    try:
        supabase = get_supabase_client()
        supabase.table("clients").delete().eq("id", client_id).execute()
        return jsonify({"message": "Client deleted successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


