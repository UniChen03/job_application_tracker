from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    page_title = "Job Application Tracker"

    applications = [
        {
            "company": "Comp1",
            "position": "Posi1",
            "wage": "20",
            "status": "Stat1",
        },
        {
            "company": "Comp2",
            "position": "Posi2",
            "wage": "20",
            "status": "Stat2",
        },
    ]

    return render_template(
        "index.html", 
        page_title=page_title, 
        applications=applications
    )