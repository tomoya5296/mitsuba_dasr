from struct import *
import numpy as np
import argparse
import h5py
import os
import const
import inspect
import copy
import OpenEXR
import Imath

class ByteIO:
    def __init__(self, name, mode):
        enable_mode = ("rb","wb","ab")
        if mode not in enable_mode:
            raise Exception('ByteIO: file mode error. mode="' + mode + '" is unsupport.')
        self.file = open(name, mode)

    def __del__(self):
        self.close()

    def close(self):
        self.file.close()

    def writeInt(self, num):
        self.file.write(pack('<i',num))

    def writeFloat(self, real_num):
        self.file.write(pack('<f',real_num))

    def readInt(self):
        return unpack('<i',self.file.read(4))[0]

    def readFloat(self):
        return unpack('<f',self.file.read(4))[0]

def clamp(x):
    if (x < 0.0):
        return 0.0
    if (x > 255.0):
        return 255.0
    return x

def GammaCorrect(value):
    if (value <= 0.0031308):
        return 12.92 * value
    return 1.055 * np.power(value, (float)(1.0 / 2.4)) - 0.055

def to_int(value):
    return int(clamp(255.0 * GammaCorrect(value) + 0.5))

def ensure_dir(dir_path):
    directory = os.path.dirname(dir_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

def make_compressed_result(src_file):
    pt = Imath.PixelType(Imath.PixelType.FLOAT)
    file = OpenEXR.InputFile(src_file)
    dw = file.header()['dataWindow']
    size = (dw.max.x - dw.min.x + 1, dw.max.y - dw.min.y + 1)
    compressed_result = np.empty((len(const.exr_channels), const.img_size, const.img_size))
    for i, channel in enumerate(const.exr_channels):
        str = file.channel(channel, pt)
        color = np.fromstring(str, dtype = np.float32)
        color.shape = (size[1], size[0])
        compressed_result[i] = color


    return compressed_result

def makehdf(outputs_dir):

    #load results
    layers_size = copy.deepcopy(const.layers_size)
    layers_size_accum = np.cumsum(layers_size)
    layers_size_accum = np.insert(layers_size_accum, 0, 0)

    compressed_results = np.empty((layers_size_accum[-1], const.img_size, const.img_size))

    index  = 0
    for spp in const.spp_counts_render:
        outfile = os.path.join(outputs_dir, '%dspp_%d.exr' % (spp, index))
        compressed_result = make_compressed_result(outfile)
        compressed_results[ layers_size_accum[index] : layers_size_accum[index] + layers_size[index],:,:] = compressed_result
        index += 1

    #make hd5f results
    hd5f_name = os.path.join(outputs_dir, 'results.h5')
    with h5py.File(hd5f_name, 'w') as fw:
        fw.attrs['spp_count'] = const.spp_counts_hdf5
        fw.attrs['layers_size'] = const.layers_size
        fw.create_dataset('result', data=compressed_results)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description ='Read hdr files and save the hdf5 file')
    parser.add_argument('outputs_dir', help = 'outputs_dir which has .exr files')
    args = parser.parse_args()
    if not os.path.exists(args.outputs_dir):
        print(args.outputs_dir + "doesn't exist")
        exit()
    makehdf(args.outputs_dir)