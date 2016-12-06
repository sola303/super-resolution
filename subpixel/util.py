'''Utilities'''
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import itertools
import numpy as np
import scipy.misc


def generate_samples_from(image, patch_size=17, stride=13):
    '''Generate samples from HR image'''
    height, width, _ = image.shape
    h_steps, w_steps = (np.arange(0, height - stride, stride),
                        np.arange(0, width - stride, stride))

    for h_step, w_step in itertools.product(h_steps, w_steps):
        yield image[w_step:w_step + patch_size,
                    h_step:h_step + patch_size]


def downscale(image, factor=1/3):
    '''Downscale image by given factor'''
    # hope it does same downscaling as blurring and subsampling
    # as they state in a paper
    return scipy.misc.imresize(image, factor)


def generate_train_data_from(file, factor, patch_size, stride):
    '''Generate input-output pairs of patches

    Input patches correspond to rescaled by factor
    output patches of the same image.
    '''
    image = scipy.misc.imread(file)
    rescaled = downscale(image, 1 / factor)

    input_patches = generate_samples_from(
        rescaled, patch_size, stride
    )
    output_patches = generate_samples_from(
        image, factor * patch_size, factor * stride
    )

    return zip(input_patches, output_patches)
