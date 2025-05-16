from flask import Flask, render_template, request, redirect, url_for
import os
from PIL import Image
from urllib.parse import quote
from datetime import timedelta
from werkzeug.utils import secure_filename
from function import *


app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.permanent_session_lifetime = timedelta(minutes=30)

ext_dict = {'pdf': 'PDF'}

# 入力画面
@app.route('/')
def index(complete=True):
    if complete:
        return render_template('index.html',messege=False)
    else:
        return render_template('index.html',message=True)
    
# 共有されたファイル一覧ページ
@app.route('/share')
def move_share():
    files = [file for file in os.listdir('files')]
    files.pop(0)
    return render_template('share.html', files=files)


# ファイルのアップロードを行う
@app.route('/upload', methods=["POST"])
def upload():
    global is_shared
    files = request.files.getlist('file')
    name = request.form.get('text')
    extension = request.form.get('ext')
    is_shared = request.form.get('is_shared')

    # ファイルが存在しない、またはファイル名が空の場合
    for file in files:
        if not file or not file.filename:
            return redirect(url_for('index'))
    #名前または拡張子が無効な場合
    if not name or not extension or extension == 'None':
        return redirect(url_for('index'))

    file_name_list = []
    for file in files:
        file_name = 'uploaded_' + secure_filename(file.filename or 'default_name')
        file_name_list.append(file_name)
        file.save(file_name)

    img_list = []
    for i in range(len(file_name_list)):
        opened_file = Image.open(file_name_list[i])
        img_list.append(opened_file)

    after_file_path = os.path.join('files', name + '.' + extension)
    image_combination(img_list).save(after_file_path, ext_dict[extension])

    delete_before_file(file_name_list)
    
    if is_shared == 'True':
        return redirect(url_for('index'))
    else:
        return download(name + '.' + extension)



# ファイルのダウンロードを行う
def download(file):
    file_path = os.path.join('files', file)
    
    if not os.path.exists(file_path):
        return redirect(url_for('move_share'))
    
    # 日本語ファイル名をURLエンコード
    encoded_file_name = quote(file)
    
    # レスポンスを作成
    response = app.response_class(
        generate(file_path),
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


@app.route('/download/<string:file>')
def shared_download(file):
    file_path = os.path.join('files', file)
    
    if not os.path.exists(file_path):
        return redirect(url_for('move_share'))
    
    # 日本語ファイル名をURLエンコード
    encoded_file_name = quote(file)
    
    # レスポンスを作成
    response = app.response_class(
        generate(file_path),
        mimetype='application/octet-stream',
        headers={
            # UTF-8でエンコードされたファイル名を指定
            'Content-Disposition': f"attachment; filename*=UTF-8''{encoded_file_name}"
        }
    )
    return response

@app.route('/delete/<string:file>')
def delete(file):
    file_path = os.path.join('files', file)
    os.remove(file_path)
    return redirect(url_for('move_share'))

if __name__ == '__main__':
    app.run(debug=True)
