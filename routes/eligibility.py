from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.user import User
from models.company import Company

eligibility_bp = Blueprint('eligibility', __name__)


# ---------------- GET COMPANIES (MISSING EARLIER) ----------------
@eligibility_bp.route('/companies', methods=['GET'])
@jwt_required()
def get_companies():
    companies = Company.query.all()

    return jsonify([
        {
            "id": c.id,
            "name": c.name,
            "min_cgpa": c.min_cgpa,
            "backlogs_allowed": c.backlogs_allowed,
            "required_skills": c.required_skills,
            "min_package": c.min_package,
            "eligible_branches": c.eligible_branches
        }
        for c in companies
    ]), 200


# ---------------- ELIGIBILITY CHECK ----------------
@eligibility_bp.route('/eligibility/check', methods=['POST'])
@jwt_required()
def check_eligibility():
    user_id = get_jwt_identity()
    user = User.query.get(int(user_id))   # ✅ FIXED (important)

    if not user.cgpa:
        return jsonify({'error': 'Please complete your profile (CGPA, branch) first'}), 400

    user_skills = set(user.skills.lower().split(',')) if user.skills else set()
    companies = Company.query.all()

    eligible = []
    not_eligible = []

    for company in companies:
        reasons_fail = []

        if user.cgpa < company.min_cgpa:
            reasons_fail.append(f"CGPA {user.cgpa} < required {company.min_cgpa}")

        if user.backlogs > company.backlogs_allowed:
            reasons_fail.append(f"Has {user.backlogs} backlogs, company allows {company.backlogs_allowed}")

        required_skills = set(s.lower() for s in (company.required_skills or []))
        missing_skills = required_skills - user_skills

        if missing_skills:
            reasons_fail.append(f"Missing skills: {', '.join(missing_skills)}")

        if reasons_fail:
            not_eligible.append({
                'company': company.name,
                'reasons': reasons_fail
            })
        else:
            eligible.append({
                'company': company.name,
                'min_package': company.min_package
            })

    return jsonify({
        'eligible_count': len(eligible),
        'eligible': eligible,
        'not_eligible': not_eligible
    }), 200