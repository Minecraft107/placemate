from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db
from models.prediction import Prediction
from services.ml_predict import predict_placement

predict_bp = Blueprint("predict", __name__)


@predict_bp.route("/predict", methods=["POST"])
@jwt_required()
def make_prediction():
    user_id = get_jwt_identity()
    data = request.get_json()

    if not data:
        return jsonify({"error": "No input data provided"}), 400

    result = predict_placement(
        data,
        model_choice=data.get("model", "rf")
    )

    pred = Prediction(
        user_id=int(user_id),
        cgpa=data.get("cgpa"),
        backlogs=data.get("backlogs"),
        skills_score=data.get("skills_count"),
        ats_score=data.get("ats_score"),
        predicted_outcome=result["outcome"],
        confidence=result["confidence"],
        model_used=result["model_used"]
    )

    db.session.add(pred)
    db.session.commit()

    return jsonify(result), 200