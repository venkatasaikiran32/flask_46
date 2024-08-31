from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)


# configurations 
app.config['SECRET_KEY'] = 'pwskills_sai_kiran'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'jpg', 'jpeg', 'png', 'gif'}
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB

# Ensures the upload folder exists 
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/', methods=['GET', 'POST'])
def upload_files():
    if request.method == 'POST':
        if 'files' not in request.files:
            return 'No file part'
        files = request.files.getlist('files')
        uploaded_files = []
        
        for file in files:
            if file.filename == '':
                continue
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                uploaded_files.append(filename)
        
        if uploaded_files:
            return redirect(url_for('uploaded_files', filenames=','.join(uploaded_files)))
        return 'No valid files uploaded'

    return render_template('uploads.html')

@app.route('/uploads')
def uploaded_files():
    filenames = request.args.get('filenames', '')
    filenames_list = filenames.split(',')
    return render_template('uploaded_files.html', filenames=filenames_list)

if __name__ == '__main__':
    app.run(debug=True)
