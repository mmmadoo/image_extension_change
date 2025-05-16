from PIL import Image
import os

def image_combination(alist):
    img_width = alist[0].width
    img_height = 0
    for file in alist:
        img_height += file.height
    
    img = Image.new('RGB',(img_width,img_height))

    update_height = 0
    for i in range(len(alist)):
        img.paste(alist[i],(0,update_height))
        update_height += alist[i].height
    
    return img

def delete_before_file(name_alist):
    for name in name_alist:
        os.remove(name)

# ファイルをストリームとして送信
def generate(file_path):
    with open(file_path, 'rb') as f:
        yield from f
