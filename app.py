from flask import Flask, render_template, request, jsonify
import json
import random

app = Flask(__name__)

# ── In-memory store (replace with a real DB later) ──────────────────────────
submissions = []

# ── Simple rule-based risk engine ────────────────────────────────────────────
def calculate_risk(data):
    score = 0
    factors = []

    attendance = float(data.get("attendance_rate", 100))
    if attendance < 60:
        score += 35
        factors.append("Critically low attendance (<60%)")
    elif attendance < 75:
        score += 20
        factors.append("Below-average attendance (<75%)")

    stage = data.get("education_stage", "")
    if stage in ["Secondary", "College Transition"]:
        score += 20
        factors.append(f"High-risk transition stage: {stage}")

    scholarship = data.get("scholarship_access", "No")
    if scholarship == "No":
        score += 15
        factors.append("No scholarship access")

    early_marriage = data.get("early_marriage_risk", "No")
    if early_marriage == "Yes":
        score += 20
        factors.append("Early marriage risk identified")

    transport = data.get("transport_barrier", "No")
    if transport == "Yes":
        score += 10
        factors.append("Transportation barrier present")

    caregiving = data.get("caregiving_role", "No")
    if caregiving == "Yes":
        score += 10
        factors.append("Caregiving responsibilities at home")

    household_income = data.get("household_income", "Medium")
    if household_income == "Low":
        score += 15
        factors.append("Low household income")

    safety = data.get("safety_concern", "No")
    if safety == "Yes":
        score += 15
        factors.append("Safety concerns reported")

    dropout_history = data.get("dropout_history", "No")
    if dropout_history == "Yes":
        score += 20
        factors.append("Previous dropout history")

    score = min(score, 100)

    if score >= 70:
        level = "HIGH"
        color = "#ff6b6b"
        recommendation = "Immediate intervention required. Assign a mentor, provide financial aid, and conduct a home visit."
    elif score >= 40:
        level = "MEDIUM"
        color = "#f4a853"
        recommendation = "Monitor closely. Offer counseling, transport support, and connect with scholarship programs."
    else:
        level = "LOW"
        color = "#51cf66"
        recommendation = "Student appears stable. Continue regular check-ins and encourage peer support networks."

    return {
        "score": score,
        "level": level,
        "color": color,
        "factors": factors,
        "recommendation": recommendation
    }


def get_regional_stats():
    """Simulate regional vulnerability data."""
    regions = ["North Zone", "South Zone", "East Zone", "West Zone", "Central Zone"]
    return [
        {
            "region": r,
            "dropout_rate": round(random.uniform(10, 55), 1),
            "avg_attendance": round(random.uniform(50, 95), 1),
            "scholarship_coverage": round(random.uniform(20, 80), 1)
        }
        for r in regions
    ]


# ── Routes ────────────────────────────────────────────────────────────────────
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()
    risk = calculate_risk(data)
    record = {**data, "risk": risk}
    submissions.append(record)
    return jsonify({"success": True, "risk": risk, "total_records": len(submissions)})


@app.route("/dashboard")
def dashboard():
    regional = get_regional_stats()
    high_risk = sum(1 for s in submissions if s["risk"]["level"] == "HIGH")
    medium_risk = sum(1 for s in submissions if s["risk"]["level"] == "MEDIUM")
    low_risk = sum(1 for s in submissions if s["risk"]["level"] == "LOW")
    return jsonify({
        "total": len(submissions),
        "high_risk": high_risk,
        "medium_risk": medium_risk,
        "low_risk": low_risk,
        "regional": regional,
        "recent": submissions[-5:][::-1]
    })


if __name__ == "__main__":
    app.run(debug=True, port=5000)