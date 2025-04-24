from flask import Flask, render_template, request, redirect, url_for
import os
from PIL import Image
from urllib.parse import quote
from datetime import timedelta

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.permanent_session_lifetime = timedelta(minutes=30)

ext_dict = {'pdf': 'PDF', 'png': 'png', 'jpg': 'jpeg'}

# 操作画面
@app.route('/')
def index():
    files = [file for file in os.listdir('files')]
    files.pop(0)
    return render_template('index.html', csv_files=files)

# ファイルのアップロードを行う
@app.route('/upload', methods=["POST"])
def upload():
    # ファイルが無い場合
    if 'file' not in request.files:
        return redirect(url_for('index'))
    
    file = request.files.get('file')
    if not file or not file.filename:
        # ファイルが存在しない、またはファイル名が空の場合
        return redirect(url_for('index'))
    
    name = request.form.get('text')
    extension = request.form.get('ext')
    if not name or not extension or extension == 'None':
        # 名前または拡張子が無効な場合
        return redirect(url_for('index'))
    
    # file.filename が None の場合に備えてデフォルト値を設定
    file_name = 'uploaded_' + (file.filename or 'default_name')
    before_file_path = os.path.join('files', file_name)
    after_file_path = os.path.join('files', name + '.' + extension)
    
    file.save(before_file_path)
    os.rename(before_file_path, after_file_path)
    
    File = Image.open(after_file_path)
    File.save(after_file_path, ext_dict[extension])
    
    return redirect(url_for('index'))

# ファイルのダウンロードを行う
@app.route('/download/<string:file>')
def download(file):
    file_path = os.path.join('files', file)
    
    if not os.path.exists(file_path):
        return redirect(url_for('index'))
    
    # ファイルをストリームとして送信
    def generate():
        with open(file_path, 'rb') as f:
            yield from f
    
    # 日本語ファイル名をURLエンコード
    encoded_file_name = quote(file)
    
    # レスポンスを作成
    response = app.response_class(
        generate(),
        mimetype='application/octet-stream',
        headers={
            # UTF-8でエンコードされたファイル名を指定
            'Content-Disposition': f"attachment; filename*=UTF-8''{encoded_file_name}"
        }
    )
    # ファイル送信後に削除
    @response.call_on_close
    def remove_file():
        if os.path.exists(file_path):
            os.remove(file_path)
    return response    




@app.route('/delete/<string:file>')
def delete(file):
    file_path = os.path.join('files', file)
    os.remove(file_path)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)



