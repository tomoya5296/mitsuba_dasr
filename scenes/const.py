import numpy as np

exe_file = '../../dist/mitsuba.exe'
outputs_dir = 'outputs'
spp_counts_hdf5  = np.array([ 1,  1,  1,  1,  2,  2,  2,  4,  4,  8,  8, 16, 0])
spp_counts_render  = np.array([ 1,  1,  1,  1,  2,  2,  2,  4,  4,  8,  8, 16, 1024])
layers_size = np.array([11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11  ])
exr_channels = (['color.R', 'color.G', 'color.B', 'distance.Y',
'albedo.R', 'albedo.G', 'albedo.B', 'normal.R', 'normal.G', 'normal.B', 'shadow.Y'])
img_size = 512
