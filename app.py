import os
import time


from flask import Flask
from flask import abort
from flask import current_app
from flask import redirect
from flask import render_template
from flask import request
from flask import send_from_directory
from flask import url_for
from flask_uploads import IMAGES
from flask_uploads import ALL
from flask_uploads import UploadSet
from flask_uploads import configure_uploads

# Définir l'application
app = Flask(__name__)

# Configuration pour les uploads de vidéos
app.config["UPLOADED_VIDEOS_DEST"] = os.path.join(app.root_path, "static/videos")  # Répertoire de destination
app.config["UPLOADED_PHOTOS_DEST"] = os.path.join(app.root_path, "static/img")

# Créer un ensemble d'upload pour les vidéos
videos = UploadSet("videos", extensions=["mp4", "webm"])  # Extensions vidéos courantes
photos = UploadSet("photos", IMAGES)

# Configurer les uploads
configure_uploads(app, videos)
 
 
# configure uploads
configure_uploads(app, photos)

@app.route('/')
def index():
  return render_template('index.html')




# from flask import Flask, abort, current_app, redirect, render_template, request, send_from_directory, url_for
# from werkzeug.utils import secure_filename
# import os


# app = Flask(__name__)

# UPLOAD_FOLDER = '/static/video/'
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Check if the directory exists, create it if not
 


# Allowed file extensions
ALLOWED_IMG = {"jpg","jpeg" }
ALLOWED_VID = {"mp4", "webm" }


 
 
 

def allowed_img(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_IMG
def allowed_video(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_VID


@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return "No file found"
    file = request.files['file']
    if file.filename == "":
        return render_template('viewer.html' ,error='No video file selected')
    if file and allowed_img(file.filename):
        filename = photos.save(file)
        print(filename)
 
        return render_template('viewer.html',   imageUrl=filename)
    if file and allowed_video(file.filename):
            # Extract extension for proper renaming
            filename, extension = os.path.splitext(file.filename)

            # Generate a unique filename based on current timestamp (avoid collisions)
            new_filename = f"{int(time.time())}{extension}"
            file.filename=new_filename
            # Save the file with the new name
            try:
                videos.save(file )
                return render_template('viewer.html', video_name = new_filename, )

            except Exception as e:
                print(f"Error saving video: {e}")
                return "Error saving video: {e}"
    return "invalid file type"



# @app.route('/upload', methods=['POST'])
# def upload():
#   if request.method == 'POST':
#     file = request.files['file']
#     type = file.content_type.split('/')[0]

#     if type == 'image':
#       # Sauvegarder l'image
#       ...
#       # Rediriger vers la page d'affichage de l'image
#       ...
#     elif type == 'video':
#       # Sauvegarder la vidéo
#       ...
#       # Rediriger vers la page d'affichage de la vidéo
#       ...




@app.route("/about/")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/tutorial")
def tutorial():
    return render_template("tutorial.html")

@app.route("/article")
def article():
    return render_template("article.html")

@app.route("/tools")
def tools():
    return render_template("tools.html")

@app.route("/viewer/")
def viewer():
    return render_template("viewer.html")


if __name__ == "__main__":
    app.run(debug=True)