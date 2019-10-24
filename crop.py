from PIL import Image
from sys import argv
import numpy as np

def rollingStride(a, size):
    shape = (a.shape[0] - size + 1, size)
    stride= a.strides + a.strides
    return np.lib.stride_tricks.as_strided(a, shape=shape, strides=stride)

def cropImage(src):             # src :: PIL.Image object
    # Convert to numpy array
    mod = np.array(src.convert('RGB'))

    # Chop off the sides
    margin = int(mod.shape[1] * 0.025)
    croppedSides = mod[:, margin:-margin, :]

    # Crop setup
    threshold   = int(mod.shape[0] * 0.05) + 1
    extra       = int(mod.shape[0] * 0.005)
    mask        = np.ones((threshold), dtype=bool)
    greyscale   = np.mean(croppedSides, axis=2)
    bg          = 0 # 255 for white
    reduced     = np.all(greyscale==bg, axis=1)

    # Top Cut
    mask[-1] = False
    cut = np.where(np.all(rollingStride(reduced, threshold) == mask, axis=1)==True)[0]
    topCut = 0
    if cut.size != 0:
        topCut = cut[0] + threshold - 1 + extra

    # Bottom Cut
    mask[-1] = True
    mask[0]  = False
    cut = np.where(np.all(rollingStride(reduced, threshold) == mask, axis=1)==True)[0]
    botCut = reduced.size
    if cut.size != 0:
        botCut = cut[np.where(cut>topCut)][0] - extra

    if topCut == 0 and botCut == reduced.size:
        return None
    else:
        return Image.fromarray(mod[topCut:botCut, ...])