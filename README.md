# image_extension_change

Renderというサイトでウェブアプリケーションをデプロイするために公開しているコードです。[https://render.com/]
アプリケーションはこちら[https://image-extension-change.onrender.com]
このwebアプリケーションはGoogleChromeやMicrosoftEdgeで開いてください。ファイル名が漢字の際の文字化けを防ぐことが出来ます。


#Features

このコードは写真ファイルをPDF化し、ファイル名の変更を一度に行えるものです。変換したファイルを、他のユーザーと写真を共有することもできます。
私の友人のために制作したものなので、拡張子がPDFのみになっています。ext_dictの中に値を追加することで、他の拡張子への変換も行えます。
「共有する」の欄にチェックを入れると、自動でダウンロードはされずに「共有したファイル」ページで、他のユーザーがダウンロードや削除を行えるようになります。
変換するファイルを複数選択した際は、それらが縦に連結されたものがダウンロードできます。横幅は1番目のファイルのものを用いるため注意してください。


#Requirement

Python 3.12.4
Flask 3.1.0
pillow 11.2.1
urllib3 2.2.3


#Note

"Files"は、共有したファイルを保持するためのフォルダです。".gitkeep"は、Github内に何も含んでいないフォルダの作成ができないため、入れているファイルです。コードでは、".gitkeep"を無視してファイルを扱っています。
"requirements.txt"は、renderにてインストールが必要なパッケージをまとめているファイルです。
".gitkeep"と"requirements.txt"は、個人での実装では必要ありません。
LinuxとMacの環境ではテストしていないので、正常に動かない場合があります。


#Author

NAME: mmmadoo
Email: madosan02220@gmail.com


#Licence

MIT licence
