from flask import Flask, render_template, request, redirect, url_for
import os
from PIL import Image
from urllib.parse import quote
from datetime import timedelta

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.permanent_session_lifetime = timedelta(minutes=30)

ext_dict = {'pdf': 'PDF', 'png': 'png', 'jpg': 'jpeg'}

# Operation screen
@app.route('/')
def index():
    files = [file for file in os.listdir('files')]
    files.pop(0)
    return render_template('index.html', csv_files=files)

# Upload a file
@app.route('/upload', methods=["POST"])
def upload():
    # If the file does not exist
    if 'file' not in request.files:
        return redirect(url_for('index'))
    
    file = request.files.get('file')
    if not file or not file.filename:
        # If the file does not exist or the file name is empty
        return redirect(url_for('index'))
    
    name = request.form.get('text')
    extension = request.form.get('ext')
    if not name or not extension or extension == 'None':
        # If the name or extension is invalid
        return redirect(url_for('index'))
    
    # Set default filename
    file_name = 'uploaded_' + (file.filename or 'default_name')
    before_file_path = os.path.join('files', file_name)
    after_file_path = os.path.join('files', name + '.' + extension)
    
    file.save(before_file_path)
    os.rename(before_file_path, after_file_path)
    
    File = Image.open(after_file_path)
    File.save(after_file_path, ext_dict[extension])
    
    return redirect(url_for('index'))

# Dowload the file
@app.route('/download/<string:file>')
def download(file):
    file_path = os.path.join('files', file)
    
    if not os.path.exists(file_path):
        return redirect(url_for('index'))
    
    # Sending a file as a stream
    def generate():
        with open(file_path, 'rb') as f:
            yield from f
    
    # URL encode Japanese file names
    encoded_file_name = quote(file)
    
    # Create a response
    response = app.response_class(
        generate(),
        mimetype='application/octet-stream',
        headers={
            # Specify a file name encoded in UTF-8.
            'Content-Disposition': f"attachment; filename*=UTF-8''{encoded_file_name}"
        }
    )
    # Delete after sending file
    @response.call_on_close
    def remove_file():
        if os.path.exists(file_path):
            os.remove(file_path)
    return response    


# Delete the file
@app.route('/delete/<string:file>')
def delete(file):
    file_path = os.path.join('files', file)
    os.remove(file_path)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)



