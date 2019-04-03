import os
import argparse
import make_hdf
import const

def configure_scene_file(filename, outputs_dir, num_samples, index):
    outfile = os.path.join(outputs_dir, '%dspp_%d.xml' % (num_samples, index))
    with open(filename, 'r') as f_in, open(outfile, 'w') as f_out:
        for l in f_in:
            l = l.replace('@NUMBER_OF_SAMPLES@', str(num_samples))
            f_out.write(l)

    return outfile

def main():
    parser = argparse.ArgumentParser(description='Run mitsuba for each spp_counts')
    parser.add_argument('scene_file', help = 'scene file(.xml)')
    parser.add_argument('outputs_dir', help = 'outputs_dir which has .exr files')

    args = parser.parse_args()

    exe_file_abspath = os.path.abspath(const.exe_file)

    if not os.path.exists(args.outputs_dir):
        os.makedirs(args.outputs_dir)

    index  = 0
    for spp in const.spp_counts_render:
        scene_file = configure_scene_file(args.scene_file, args.outputs_dir, spp, index)
        print(exe_file_abspath)
        os.system('%s %s -j 4' % (exe_file_abspath, scene_file))
        index += 1
    
    make_hdf.makehdf(args.outputs_dir)


if __name__ == '__main__':
    main()