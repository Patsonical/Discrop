from PIL import Image
import numpy as np

def rollingStride(a, size):
    shape = (a.shape[0] - size + 1, size)
    stride= a.strides + a.strides
    return np.lib.stride_tricks.as_strided(a, shape=shape, strides=stride)

def cropImage(src):             # src :: PIL.Image object
    # Convert to numpy array
    mod = np.array(src.convert('RGB'))

    # Don't crop if the image is too wide
    if mod.shape[0] < mod.shape[1]:
        return None

    # Chop off the sides
    margin = int(mod.shape[1] * 0.025)
    croppedSides = mod[:, margin:-margin, :]

    # Reduce color depth (decrease threshold for "same color")
    colorMultiplier = 0.05
    lessColor = (croppedSides * colorMultiplier).astype('uint8')

    # Crop setup
    threshold   = int(mod.shape[0] * 0.05) + 1
    extra       = int(mod.shape[0] * 0.005)
    mask        = np.ones((threshold), dtype=bool)
    greyscale   = np.mean(lessColor, axis=2)
    reduced     = np.all(greyscale.T == greyscale[:,0], axis=0)

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
    cut = cut[np.where(cut>topCut)]
    botCut = reduced.size
    if cut.size != 0:
        botCut = cut[0] - extra

    if topCut == 0 and botCut == reduced.size:
        return None
    else:
        return Image.fromarray(mod[topCut:botCut, ...])
