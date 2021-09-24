import tarfile
from itertools import product
from os import makedirs
import os
from os.path import isdir, abspath, join
from shutil import rmtree

import numpy as np
from KicadModTree import *

dst_folder = abspath("smdpad.pretty")
dst_file = abspath("smdpad.tar.xz")
if isdir(dst_folder):
    rmtree(dst_folder)
makedirs(dst_folder)

unit = 2.54
dimensions = np.array([0.5, 1, 1.5, 2]) * unit
spacings = np.array([1 / 10, 1 / 5, 1 / 2, 1, 1.5, 2]) * unit
X = range(1, 21)
Y = range(1, 3)
for width, height, spacing, x, y in product(dimensions, dimensions, spacings, X, Y):
    footprint_name = f"smdpad_%02ix%02i_%01.2f_%01.2f_%01.2f" % (y, x, width, height, spacing)

    # init kicad footprint
    kicad_mod = Footprint(footprint_name)
    kicad_mod.setDescription("A SMD pas to solder wires on")
    # kicad_mod.setTags("smd,pad,connector".split(','))

    # set general values
    kicad_mod.append(Text(type='reference', text='SMDPAD?', at=[0, height * y], layer='F.SilkS'))
    kicad_mod.append(Text(type='value', text=footprint_name, at=[0, -height * y], layer='F.Fab'))
    #
    # # create silkscreen
    # kicad_mod.append(RectLine(start=[-2, -2], end=[5, 2], layer='F.SilkS'))
    #
    # # create courtyard
    # kicad_mod.append(RectLine(start=[-2.25, -2.25], end=[5.25, 2.25], layer='F.CrtYd'))

    # create pads
    for i, (_x, _y) in enumerate(product(np.arange(x) * (width + spacing), np.arange(y) * (height + spacing))):
        kicad_mod.append(Pad(number=i + 1, type=Pad.TYPE_SMT, shape=Pad.SHAPE_RECT,
                             at=[_x, _y], size=[width, height], layers=Pad.LAYERS_SMT))

    # add model
    # kicad_mod.append(Model(filename="example.3dshapes/example_footprint.wrl",
    #                        at=[0, 0, 0], scale=[1, 1, 1], rotate=[0, 0, 0]))

    # output kicad model
    file_handler = KicadFileHandler(kicad_mod)
    filename = footprint_name + ".kicad_mod"
    file_handler.writeFile(join(dst_folder, filename))

# Compress result
with tarfile.open(dst_file, "w:xz") as tar:
    tar.add(os.path.relpath(dst_folder))
rmtree(dst_folder)