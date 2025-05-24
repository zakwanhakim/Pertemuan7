from flask import Blueprint, request, jsonify
from app.auth import require_api_key
from app.models import topup_data

bp = Blueprint("main", __name__, url_prefix="/api")

@bp.route("/topup", methods=["GET"])
@require_api_key
def get_all():
    return jsonify(topup_data)

@bp.route("/topup", methods=["POST"])
@require_api_key
def create():
    data = request.json
    if not data or 'user' not in data or 'amount' not in data:
        return jsonify({"error": "Data user atau jumlah tidak lengkap"}), 400
    topup_data.append(data)
    return jsonify({"message": "Topup berhasil ditambahkan", "data": data}), 201

@bp.route("/topup/<int:idx>", methods=["PUT"])
@require_api_key
def update(idx):
    if idx < 0 or idx >= len(topup_data):
        return jsonify({"error": "Data tidak ditemukan"}), 404
    data = request.json
    if not data or 'user' not in data or 'amount' not in data:
        return jsonify({"error": "Data user atau jumlah tidak lengkap"}), 400
    topup_data[idx] = data
    return jsonify({"message": "Topup berhasil diperbarui", "data": data})

@bp.route("/topup/<int:idx>", methods=["DELETE"])
@require_api_key
def delete(idx):
    if idx < 0 or idx >= len(topup_data):
        return jsonify({"error": "Data tidak ditemukan"}), 404
    deleted_item = topup_data.pop(idx)
    return jsonify({"message": "Topup berhasil dihapus", "data_terhapus": deleted_item})

@bp.route("/health")
def health_check():
    return jsonify({"status": "sehat"})
