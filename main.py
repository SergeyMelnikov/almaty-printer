from flask import Flask, render_template, request, abort, redirect, url_for, send_file
from pdf import make_pdf, print_pdf
import comps
import time

app = Flask(__name__)


@app.route("/")
def index():
    ip = request.remote_addr
    team = comps.get_names(comps.get(ip))
    return render_template("index.html", team=team)

@app.route("/success")
def success():
    return render_template("success.html")

@app.route("/print", methods=["POST"])
def post_print():
    body = request.form.get('body')
    ip = request.remote_addr
    if not body:
        return abort(400)
    team = comps.get(ip)
    timestamp = int(time.time())
    with open(f"prints/{team}-{timestamp}.txt", "w", encoding="utf8") as f:
        f.write(body)
    pdf_file = make_pdf(f"prints/{team}-{timestamp}.pdf", body, team)
    print_pdf(pdf_file)
    return redirect(url_for("success"))
#    return send_file(pdf_file) # left for debugging purposes. Uncomment to see pdf in browser


if __name__ == "__main__":
    app.run("0.0.0.0", 80, debug=False)

