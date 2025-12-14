1. Zainstaluj pythona **sudo apt install python3.11**
2. Zainstaluj manadżer pakietów pip3: **sudo apt install pip3**
3. Utwórz wirtualne środowisko poprzez komendę: **python3 -m venv ~/.venv**
4. Wejdź do wirtualnego środowiska: **source ~/.venv/bin/activate** i pobierz Flask dla pythona **pip3 install flask**
5. Stwórz serwis tv.service: **vim /etc/systemd/system/tv.service** i wklej zawartość zmieniając **usera**:
```
[Unit]
Description=Raspberry Pi TV Streamlink Web UI
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=jacek
WorkingDirectory=/home/jacek/tv
ExecStart=/home/jacek/.venv/bin/python /home/jacek/tv/tv.py
Restart=always
RestartSec=5


[Install]
WantedBy=multi-user.target
```

6. Wykonaj komendy: **sudo systemctl daemon-reload** oraz **systemctl enable tv.service**
7. Spróbuj wystartować program **sudo systemctl start tv.service** oraz sprawdzić jego logi na bieżąco: **journalctl -u tv.service -f**
>Aplikacja odpala się na porcie 8080. Możliwość skonfigurowania w pliku tv.py.