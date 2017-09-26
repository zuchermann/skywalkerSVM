import h5py
from util import get_image_data

folder = './../data/with_brace/ipad_zach/fingers'

images, data = get_image_data(folder)
out_data = [images, data]

with h5py.File(folder + '/image_data.h5', 'w') as hf:
    hf.create_dataset("images", data=images)
    hf.create_dataset("data", data=data)