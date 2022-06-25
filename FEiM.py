from ast import Or
import os, pathlib 
from datetime import datetime
from time import time
import PIL.Image, PIL.ExifTags
import filetype, sys
from PIL import Image
import cv2,json


# assign directory
directory = 'out'
output_dir = 'test2'


def format_datetime(dt):
    # format datetime object 
    # strptime is short for "parse time" 
    # strftime is for "formatting time"
    return dt.strftime("%Y%m%d_%H%M%S")

def ts_epoch_to_datetime(timestamp):
    # convert timestamp into DateTime object
    dt = datetime.fromtimestamp(timestamp)
    return format_datetime(dt)

def to_datetime_obj(str):
    dt = datetime.strptime(str,'%Y:%m:%d %H:%M:%S')
    return format_datetime(dt)

def get_f_m_time(path):
    # file modification timestamp of a file
    m_time = os.path.getmtime(path)
    return ts_epoch_to_datetime(m_time)

def get_f_c_time_os(path):
    # file creation timestamp in float
    c_time = os.path.getctime(path)
    return ts_epoch_to_datetime(c_time)

def get_f_c_time_pathlib(path):
    creation_time = pathlib.Path(path).stat().st_ctime
    return ts_epoch_to_datetime(creation_time)

def get_exif_info_image(path):
    #stackoverflow.com/questions/4764932
    img = PIL.Image.open(path)
    #exif_data = img._getexif()
    return  {
        PIL.ExifTags.TAGS[k]: v
        for k, v in img._getexif().items()
        if k in PIL.ExifTags.TAGS
    }
 
def get_new_filename_image(path):
    """
    Function needs the path of the image (if not provided it will the stop)
    and returns a new file name based on the original creation date
    if the new name already exists (for example photo taken in the same second) it will add a zero
    """
    if not filetype.is_image(path): sys.exit("None image supplied")
    DateTimeOriginal = get_exif_info_image(path)['DateTimeOriginal']   
    f_dt_DateTimeOrginial = to_datetime_obj(DateTimeOriginal)
    extension = pathlib.Path(path).suffix
    new_name = f'{output_dir}\{f_dt_DateTimeOrginial}{extension}'
    if os.path.exists(new_name):
            return f'{output_dir}\{f_dt_DateTimeOrginial}0{extension}'
    return new_name

def rotate_image_PIL(path, orientation):
    picture = Image.open(path)
    return picture.rotate(90, resample=Image.BICUBIC, expand=True).save(path)

def rotate_image_CV2(path):
    """
    Based on the EXIF keys 'Orientation' and 'ExifImageHeight' the image should but turned different

    -.PNG is skipped because those seem to be screenshots that are already turned the right way
    -Orientation value 8 seems to be the right way

    -Pictures taken in portrait mode must be turned 90° degrees counterclockwise
    -Pictures taken in landscape mode must be turned 180° degrees (clockwise)
    To know in which mode the pictures were shot I stumbled upon 'ExifImageHeight' 
    which seems to be a good indicator. 
        For landscape mode, value 3024 was used, and portrait mode values 3088 and 4032

    """
    Orientation = get_exif_info_image(path)['Orientation']
    ExifImageHeight = get_exif_info_image(path)['ExifImageHeight']

    ExifImageHeight_mapping = {

    4032:'Portrait',
    3088:'Portrait',
    3024:'Landscape'

    }


    if Orientation == 1 and pathlib.Path(path).suffix != ".PNG": 
        img = cv2.imread(path)
        if ExifImageHeight_mapping[ExifImageHeight] == 'Portrait':
            img_rotated = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
            
        elif ExifImageHeight_mapping[ExifImageHeight] == 'Landscape':
            img_rotated = cv2.rotate(img, cv2.ROTATE_180)
            print(get_exif_info_image(path))

        else:
            print(ExifImageHeight)
            print('Ow ow ow error incoming')

        cv2.imwrite(path, img_rotated)




def main():
    renamed = 0

    print(f"[+] Directory '{directory}' contains {len(os.listdir(directory))}# files")
    for filename in os.listdir(directory):

        f = os.path.join(directory, filename)

        if filetype.is_image(f):
            try:
                old_name = f
                new_name = get_new_filename_image(f)

                rotate_image_CV2(f)
                os.rename(old_name, new_name)

                print(f"[+] Renaming '{old_name}' to '{new_name}'")
                
                renamed +=1
            except KeyError:
                #File doesn't have the DateTimeOriginal key
                pass
                #print(get_exif_info(f))
            except AttributeError:
                #File doesn't have exif data
                print(f"{f} has no exif data")
                pass
             
    print(f"[+] {renamed}# photos have been renamed")

if __name__ == "__main__":
    main()