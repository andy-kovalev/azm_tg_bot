setx ENV_FILENAME %cd%"/.env/settings.env"
call ./venv/Scripts/activate.bat
python.exe ./tg_bot/__main__.py