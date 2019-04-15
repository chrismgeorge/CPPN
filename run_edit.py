from model import CPPN
import numpy as np
import argparse
import pickle

def parseArguments():
    # Create argument parser
    parser = argparse.ArgumentParser()

    # Optional arguments
    parser.add_argument("--x_dim", type=int, default=1280)
    parser.add_argument("--y_dim", type=int, default=720)
    parser.add_argument("--z_dim", type=int, default=5)
    parser.add_argument("--scale", type=int, default=16)

    parser.add_argument("--neurons_per_layer", type=int, default=6)
    parser.add_argument("--number_of_layers", type=int, default=4)
    parser.add_argument("--color_channels", type=int, default=1)

    parser.add_argument("--number_of_stills", type=int, default=5)
    parser.add_argument("--interpolations_per_image", type=int, default=24)
    parser.add_argument("--file_name", type=str, default='./videos/test01.mp4')

    # Parse arguments
    args = parser.parse_args()

    return args

def save_single_random_image(cppn, file_name, z_dim):
    z = np.random.uniform(-1.0, 1.0, size=(z_dim)).astype(np.float32)
    cppn.save_png(z, file_name)
    with open('outfile', 'wb') as f: # 'outfile' can be renamed
        pickle.dump([z.tolist()], f)

def save_many_images(cppn, z_dim):
    zs = []
    for i in range(200):
        file_name = './photos/test%d.png' % i
        z_vector = np.random.uniform(-1., 1., size=(z_dim)).astype(np.float32)
        cppn.save_png(z_vector, file_name)
        zs.append(z_vector.tolist())
        print('Done! The image is at %s' % file_name)
    with open('outfile', 'wb') as f: # can change 'outfile'
        pickle.dump(zs, f)

def redisplay_image(cppn, outfile, index, file_name):
    with open (outfile, 'rb') as fp: # 'outfile' can be renamed
        reloaded_vectors = pickle.load(fp)
    z = np.array(reloaded_vectors[index]) # would be named test10.png
    cppn.save_png(z, file_name) # make sure you name this something you'll remember

def wibble_around_image(cppn, outfile, index, file_name, z_dim):
    with open (outfile, 'rb') as fp: # 'outfile' can be renamed
        reloaded_vectors = pickle.load(fp)
    z_start = np.array(reloaded_vectors[index]) # would be named test10.png
    zs = []
    for i in range(10): # how many 'key frames' you want
        z = np.random.uniform(-.15, .15, size=(z_dim)).astype(np.float32)
        z = np.add(z_start, z)
        zs.append(z)
    cppn.save_mp4(zs, file_name, loop=False) # make sure this is named correctly

def make_random_video(cppn, file_name, z_dim):
    zs = [] # list of latent vectors
    for i in range(number_of_stills):
        zs.append(np.random.uniform(-1.0, 1.0, size=(z_dim)).astype(np.float32))
    cppn.save_mp4(zs, file_name, loop=True) # set to false if you don't want a loop


def main(x_dim, y_dim, z_dim, scale, neurons_per_layer, number_of_layers,
         color_channels, number_of_stills, interpolations_per_image, file_name):

    # Initialize CPPN with parameters #########################################
    print('Initializing CPPN...')
    cppn = CPPN(x_dim, y_dim, z_dim, scale, neurons_per_layer, number_of_layers,
                color_channels, interpolations_per_image)
    cppn.neural_net(True)
    ###########################################################################

    # (1) Uncomment the functions to perform their actions.
    # (2) Change any variable names to your preferred name.
    # (3) Run code!

    ## Change name to save a new model.
    model_name = 'new_model_3'

    ## Save CPPN if you want to.
    # cppn.save_model(model_name)

    ## Load a saved CPPN
    cppn.load_model(model_name)

    ## Save single random image
    file_name = './photos/000.png'
    # save_single_random_image(cppn, file_name, z_dim)

    ## Make 100 random images and save their latent vectors
    # save_many_images(cppn, z_dim)

    ## Re-display a specific image from a saved model.
    outfile = 'outfile'
    index = 0
    file_name = 'rename_me.png'
    # redisplay_image(cppn, outfile, index, file_name)

    ## Wibble around a specific image and make a video from it.
    outfile = 'outfile'
    index = 108
    file_name = './videos/new_video.mp4'
    # wibble_around_image(cppn, outfile, index, file_name, z_dim)

    ## Make a list of random video
    file_name = './videos/random_video.mp4'
    # make_random_video(cppn, file_name, z_dim)


if __name__ == '__main__':
    # Parse the arguments
    args = parseArguments()
    # Run function
    main(args.x_dim, args.y_dim, args.z_dim, args.scale, args.neurons_per_layer,
         args.number_of_layers, args.color_channels, args.number_of_stills,
         args.interpolations_per_image, args.file_name)


