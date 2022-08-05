from pdf2image import convert_from_path
import os
import pdf2image

def pdf2image_c(path,number): 
    images = convert_from_path(path_dict+'/'+path,dpi=500,poppler_path=r'/opt/homebrew/Cellar/poppler/22.06.0_1/bin')
    for i in range(len(images)):
        images[i].save(f'CV_imges/CV'+ str(number) +'.jpg','JPEG')
path_dict='CV'
paths=os.listdir(path_dict)
for i in range(1,len(paths)):
    pdf2image_c(paths[i],i)