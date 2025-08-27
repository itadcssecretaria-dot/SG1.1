from flask import Blueprint, request, jsonify, current_app
from src.models import SaleCreate, SaleUpdate
from pydantic import ValidationError

sale_bp = Blueprint("sale_bp", __name__)

def get_supabase_client():
    return current_app.config["SUPABASE_CLIENT"]

@sale_bp.route("/sales", methods=["GET"])
def get_sales():
    try:
        supabase = get_supabase_client()
        response = supabase.table("sales").select("*").execute()
        return jsonify(response.data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@sale_bp.route("/sales/<sale_id>", methods=["GET"])
def get_sale(sale_id):
    try:
        supabase = get_supabase_client()
        response = supabase.table("sales").select("*").eq("id", sale_id).single().execute()
        return jsonify(response.data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@sale_bp.route("/sales", methods=["POST"])
def create_sale():
    try:
        sale_data = SaleCreate(**request.get_json())
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400
    try:
        supabase = get_supabase_client()
        response = supabase.table("sales").insert(sale_data.dict()).execute()
        return jsonify(response.data), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@sale_bp.route("/sales/<sale_id>", methods=["PUT"])
def update_sale(sale_id):
    try:
        sale_data = SaleUpdate(**request.get_json())
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400
    try:
        supabase = get_supabase_client()
        response = supabase.table("sales").update(sale_data.dict(exclude_unset=True)).eq("id", sale_id).execute()
        return jsonify(response.data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@sale_bp.route("/sales/<sale_id>", methods=["DELETE"])
def delete_sale(sale_id):
    try:
        supabase = get_supabase_client()
        supabase.table("sales").delete().eq("id", sale_id).execute()
        return jsonify({"message": "Sale deleted successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


