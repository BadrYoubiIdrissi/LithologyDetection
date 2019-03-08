from PIL import Image
import os
from tqdm import tqdm

def splitIntoSlices(input_path, output_path, verbose = True):
    max_height = 2**14
    if verbose : 
        file_iterator = tqdm(os.listdir(input_path))
    else:
        file_iterator = os.listdir(input_path)
    for img_fn in file_iterator:
        image = Image.open(os.path.join(input_path, img_fn))
        _, height = image.size
        divisible = height % max_height > 0
        for i in range(height//max_height+int(divisible)):
            a = slice(image, i)
            a.save(os.path.join(output_path, "slice_"+str(i)+"_"+img_fn))


def slice(image, i, max_height = 2**14):
    width, height = image.size
    start_height = i*max_height
    assert start_height < height
    end_height = min((i+1)*max_height, height)
    return image.crop((0, start_height, width, end_height))

