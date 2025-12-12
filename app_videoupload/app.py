import os
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename

# Define the folder where uploaded files will be stored
UPLOAD_FOLDER = 'static/uploads' 
# Define allowed video extensions
ALLOWED_EXTENSIONS = {'mp4', 'mov', 'avi', 'wmv', 'flv', 'webm', 'mkv'} 

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'default_secret_for_dev')

# Optional: Set a maximum content length (e.g., 100MB) to prevent large uploads
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024 

# Create the upload folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # 1. Check if the POST request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)

        file = request.files['file']

        # 2. Check if user selected a file
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        # 3. Check if the file is allowed and save it
        if file and allowed_file(file.filename):
            # Secure the filename to prevent directory traversal attacks
            filename = secure_filename(file.filename)

            # Save the file to the configured UPLOAD_FOLDER
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            flash(f'Video "{filename}" successfully uploaded!')
            # Redirect to a page that can display the video
            return redirect(url_for('uploaded_file', filename=filename))
        else:
            flash('Invalid file type. Allowed: ' + ', '.join(ALLOWED_EXTENSIONS))
            return redirect(request.url)

    # For GET request, render the upload form
    return render_template('upload.html')

# Add a route to serve the uploaded file (optional, but good for display)
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    # You'll need to create a display template here that uses the HTML5 <video> tag
    return render_template('video_display.html', filename=filename) 

if __name__ == '__main__':
    app.run(debug=True)