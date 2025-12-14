from flask import Flask, request, render_template, redirect, url_for
import subprocess

app = Flask(__name__)

player_process = None
PLAYER_CMD = 'mpv --fs --no-border --ao=alsa --audio-device=hdmi'

# Twoja własna lista streamów
STREAM_LIST = [
    {"title": "Twitch – RocketLeague", "url": "https://www.twitch.tv/rocketleague"},
    {"title": "YouTube – Piłka nożna na żywo", "url": "https://www.youtube.com/watch?v=hOoo9kEXOhI"},
    {"title": "Twitch – LoL Championship", "url": "https://twitch.tv/lol_championship"}
]

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", streams=STREAM_LIST)

@app.route("/play", methods=["POST"])
def play():
    global player_process

    # Pobranie linku z listy lub własnego pola
    selected_url = request.form.get("url_select")
    custom_url = request.form.get("url_custom")
    url = custom_url.strip() if custom_url else selected_url

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

