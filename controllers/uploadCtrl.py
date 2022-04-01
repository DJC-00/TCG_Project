import os
import werkzeug
from flask_app import app
from flask import render_template,redirect,request,session,flash
from functools import wraps
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from flask_app.models import uploader
from PIL import Image

uploadFile = "C:/Users/JuiceBox/My Drive/Code/Coding_Dojo/My Projects/card_project/flask_app/static/uploads"
quarintine = "C:/Users/JuiceBox/My Drive/Code/Coding_Dojo/My Projects/card_project/flask_app/static/quarintine"
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLD = 'C:/Users/JuiceBox/My Drive/Code/Coding_Dojo/My Projects/card_project/flask_app/static/uploads'
UPLOAD_FOLDER = os.path.join(APP_ROOT, UPLOAD_FOLD)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.jpeg']

@app.route('/upload')
def upload_file():
   return render_template('upload.html')
	
@app.route('/uploader', methods = ['GET', 'POST'])
def upload_my_file():
   new_file_name = 'Card_Image_00001'
   if request.method == 'POST':
      up_file = request.files['file']
      if up_file.filename == '':
         return redirect('//generatorHome')
      file_ext = os.path.splitext(up_file.filename)[1]
      if file_ext not in app.config['UPLOAD_EXTENSIONS']:
         return redirect('//generatorHome')
      new_file_name += str(os.path.splitext(up_file.filename)[1])
      up_file.save(os.path.join(app.config['UPLOAD_FOLDER'],secure_filename(new_file_name)))
      print("++++++++++++++++++++++ Safe Search! ++++++++++++++++++++++")
      uploader.detect_safe_search(os.path.join(app.config['UPLOAD_FOLDER'],secure_filename(new_file_name)))
      print("++++++++++++++++++++++ Safe Search! ++++++++++++++++++++++")
      im = Image.open(os.path.join(app.config['UPLOAD_FOLDER'],secure_filename(new_file_name)))
      print(f"width, {im.width} length, {im.height}")
      
      if im.height - im.width < 100 and im.height - im.width > -100 :
         session['orientation'] = "square"
      elif im.width > im.height:
         session['orientation'] = "land"
      else:
         session['orientation'] = "port"

      session['fName'] = new_file_name
      if request.form['cardName'] != '':
         session['cardName'] = request.form['cardName']
      return redirect("/viewCard")
