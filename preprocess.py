from PIL import Image
import os
from tqdm import tqdm
import warnings

def splitIntoSlices(input_path, output_path, max_files = -1):
    warnings.simplefilter('ignore', Image.DecompressionBombWarning)
    max_height = 2**14
    for img_fn in tqdm(os.listdir(input_path)[:max_files]):
        image = Image.open(os.path.join(input_path, img_fn))
        _, height = image.size
        divisible = height % max_height > 0
        for i in range(height//max_height+int(divisible)):
            a = slice(image, i)
            new_f_name = img_fn.split(".")[0]+"_slc_"+str(i)+".png"
            a.save(os.path.join(output_path, new_f_name))


def slice(image, i, max_height = 2**14):
    width, height = image.size
    start_height = i*max_height
    assert start_height < height
    end_height = min((i+1)*max_height, height)
    return image.crop((0, start_height, width, end_height))

