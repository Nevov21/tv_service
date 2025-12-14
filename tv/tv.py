from flask import Flask, request, render_template, redirect, url_for, jsonify
import subprocess
import streamlink

app = Flask(__name__)

player_process = None
PLAYER_CMD = 'mpv --fs --no-border --ao=alsa --audio-device=hdmi'

@app.route("/get_qualities", methods=["POST"])
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
def index():
    return render_template("index.html")

@app.route("/play", methods=["POST"])
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