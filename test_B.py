import os
from options.test_options import TestOptions
from data import create_dataset
from models import create_model
from util.util import tensor2im, MkdirSimple
import cv2
from tqdm import tqdm
import numpy as np


if __name__ == '__main__':
    opt = TestOptions().parse()  # get test options
    opt.dataset_mode = 'single'
    # hard-code some parameters for test
    opt.num_threads = 0   # test code only supports num_threads = 1
    opt.batch_size = 1    # test code only supports batch_size = 1
    opt.serial_batches = True  # disable data shuffling; comment this line if results on randomly chosen images are needed.
    opt.no_flip = True    # no flip; comment this line if results on flipped images are needed.
    opt.display_id = -1   # no visdom display; the test code saves the results to a HTML file.
    dataset = create_dataset(opt)  # create a dataset given opt.dataset_mode and other options
    model = create_model(opt)      # create a model given opt.model and other options
    model.setup(opt)               # regular setup: load and print networks; create schedulers
    output_dir = opt.dataroot + "_new"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # test with eval mode. This only affects layers like batchnorm and dropout.
    # For [pix2pix]: we use batchnorm and dropout in the original pix2pix. You can experiment it with and without eval() mode.
    # For [CycleGAN]: It should not affect CycleGAN as CycleGAN uses instancenorm without dropout.
    if opt.eval:
        model.eval()
    for data in tqdm(dataset):
        model.set_input(data)  # unpack data from data loader
        img_path = os.path.join(output_dir, model.get_image_paths()[0][len(opt.dataroot)+1:])
        if os.path.exists(img_path):
            continue
        model.test()           # run inference
        visuals = model.get_current_visuals()  # get image results
        for label, im_data in visuals.items():
            if 'fake' in label:
                img = tensor2im(im_data)
                MkdirSimple(img_path)
                cv2.imwrite(img_path, img[..., ::-1])
