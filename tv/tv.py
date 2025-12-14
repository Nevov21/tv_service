from flask import Flask, request, render_template, redirect, url_for, jsonify, Response
import subprocess
import streamlink
from functools import wraps

app = Flask(__name__)

def check_auth(username, password):
    """Sprawdza poprawność loginu i hasła."""
    return username == 'belpaese' and password == '777777'

def authenticate():
    """Wysyła nagłówek 401 żądający autoryzacji."""
    return Response(
    'Musisz się zalogować, aby uzyskać dostęp.', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

player_process = None
PLAYER_CMD = 'mpv --fs --no-border --ao=alsa --audio-device=hdmi'

@app.route("/get_qualities", methods=["POST"])
@requires_auth
def get_qualities():
    url = request.form.get("url")
    if not url:
        return jsonify({"error": "Brak URL"}), 400
    try:
        streams = streamlink.streams(url)
        qualities = sorted(streams.keys(), key=lambda q: (q == "best", q))
        return jsonify({"qualities": qualities})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/", methods=["GET"])
@requires_auth
def index():
    return render_template("index.html")

@app.route("/play", methods=["POST"])
@requires_auth
def play():
    global player_process

    # Pobranie linku z pola
    url = request.form.get("url_custom")
    if url:
        url = url.strip()

    quality = request.form.get("quality", "best")

    if not url:
        return "Brak URL", 400

    stop_player()

    player_process = subprocess.Popen([
        "streamlink",
        "--player", PLAYER_CMD,
        url,
        quality
    ])

    return redirect(url_for("index"))

@app.route("/stop", methods=["POST"])
@requires_auth
def stop():
    stop_player()
    return redirect(url_for("index"))

def stop_player():
    global player_process
    if player_process and player_process.poll() is None:
        player_process.terminate()
        player_process = None
    else:
        subprocess.call(["pkill", "-f", "mpv"])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)