import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "./card_project/flask_app/static/uploads"
app.config['MAX_CONTENT_PATH'] = 1024 * 1024
app.secret_key = "Secret Tunnel!"
