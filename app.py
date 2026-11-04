from io import BytesIO
from modules.assistant import get_assistant_response
from flask import send_file
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)
import time
from datetime import datetime
from flask import Flask, render_template, jsonify, request, send_from_directory
from modules.url_checker import analyze_url
from modules.history import (
    init_db,
    save_scan,
    get_recent_scans,
    get_monitoring_metrics
)
app = Flask(__name__)
APP_START_TIME = time.monotonic()

@app.route("/service-worker.js")
def service_worker():
    response = send_from_directory(
        "static",
        "service-worker.js",
        mimetype="application/javascript"
    )
    response.headers["Service-Worker-Allowed"] = "/"
    response.headers["Cache-Control"] = "no-cache"
    return response



# Create the scan history database and table
init_db()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/status")
def system_status():
    from datetime import datetime

    return jsonify({
        "application": "TYRONE THREAT",
        "version": "1.0.0",
        "status": "online",
        "timestamp": datetime.now().isoformat()
    })


@app.route("/api/dashboard")
def dashboard():
    return jsonify({
        "threats_detected": 0,
        "security_alerts": 0,
        "protected_systems": 1,
        "system_health": "Operational",
        "recent_activity": get_recent_scans(5)
    })

@app.route("/api/check-url", methods=["POST"])
def check_url():
    data = request.get_json(silent=True) or {}
    url = data.get("url", "")

    result = analyze_url(url)

    if result["success"]:
        try:
            save_scan(result)
        except Exception:
            app.logger.exception("Could not save URL scan history")

    status_code = 200 if result["success"] else 400

    return jsonify(result), status_code


@app.route("/api/history")
def scan_history():
    return jsonify({
        "success": True,
        "total": len(get_recent_scans(10)),
        "history": get_recent_scans(10)
    })


@app.route("/api/monitoring", methods=["GET"])
def monitoring():

    return jsonify({
        "application": "TYRONE THREAT",
        "status": "online",
        "uptime_seconds": int(time.monotonic() - APP_START_TIME),
        "metrics": get_monitoring_metrics(),
        "recent_activity": get_recent_scans(5),
        "checked_at": datetime.now().isoformat()
    })


@app.route("/api/reports/pdf", methods=["GET"])
def export_security_report():
    from datetime import datetime

    metrics = get_monitoring_metrics()
    scans = get_recent_scans(1000)

    total = metrics["total_scans"]
    low = metrics["low_risk"]
    medium = metrics["medium_risk"]
    high = metrics["high_risk"]

    pdf_buffer = BytesIO()

    document = SimpleDocTemplate(
        pdf_buffer,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=45,
        bottomMargin=45
    )

    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph(
        "TYRONE THREAT",
        styles["Title"]
    ))

    story.append(Paragraph(
        "Security Analysis Report",
        styles["Heading2"]
    ))

    story.append(Spacer(1, 12))

    story.append(Paragraph(
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        styles["Normal"]
    ))

    story.append(Spacer(1, 20))

    report_data = [
        ["Security Metric", "Recorded Value"],
        ["Total URL Scans", str(total)],
        ["Low Risk", str(low)],
        ["Medium Risk", str(medium)],
        ["High Risk", str(high)]
    ]

    summary_table = Table(
        report_data,
        colWidths=[260, 180]
    )

    summary_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#5b3cc4")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("PADDING", (0, 0), (-1, -1), 9),
        ("ALIGN", (1, 1), (1, -1), "CENTER")
    ]))

    story.append(summary_table)

    story.append(Spacer(1, 25))

    story.append(Paragraph(
        "Recent URL Scan Activity",
        styles["Heading2"]
    ))

    activity_data = [
        ["Hostname", "Risk Level", "Score", "Date"]
    ]

    for scan in scans:
        activity_data.append([
            str(scan.get("hostname", "Unknown")),
            str(scan.get("risk_level", "Unknown")),
            str(scan.get("risk_score", 0)),
            str(scan.get("created_at", "Unknown"))[:19]
        ])

    if len(activity_data) == 1:
        activity_data.append([
            "No scans recorded", "-", "-", "-"
        ])

    activity_table = Table(
        activity_data,
        colWidths=[125, 85, 55, 175],
        repeatRows=1
    )

    activity_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#5b3cc4")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("PADDING", (0, 0), (-1, -1), 6),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
        ("VALIGN", (0, 0), (-1, -1), "TOP")
    ]))

    story.append(activity_table)

    story.append(Spacer(1, 20))

    story.append(Paragraph(
        "Disclaimer: This report summarises URL analyses "
        "recorded by Tyrone Threat. Risk classifications are "
        "based on static URL indicators and do not guarantee "
        "that a website is safe or malicious. This report does "
        "not represent a complete network security audit.",
        styles["Italic"]
    ))

    document.build(story)

    pdf_buffer.seek(0)

    return send_file(
        pdf_buffer,
        mimetype="application/pdf",
        as_attachment=True,
        download_name="Tyrone_Threat_Security_Report.pdf"
    )

@app.route("/api/assistant", methods=["POST"])
def assistant():
    data = request.get_json(silent=True) or {}
    question = data.get("question", "")

    if not isinstance(question, str) or not question.strip():
        return jsonify({
            "success": False,
            "error": "Please enter a question."
        }), 400

    if len(question) > 500:
        return jsonify({
            "success": False,
            "error": "Your question must be 500 characters or fewer."
        }), 400

    answer = get_assistant_response(question)

    return jsonify({
        "success": True,
        "answer": answer
    })


if __name__ == "__main__":
    app.run(debug=False)

