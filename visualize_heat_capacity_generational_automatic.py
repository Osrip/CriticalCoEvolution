#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from os import path, makedirs
from automatic_plot_helper import load_settings
import os





def main(sim_name, settings, generation_list, i_type):

    # TODO: make these scripts take these as params
    loadfile = sim_name
    folder = 'save/' + loadfile
    # iter_gen = np.arange(0, 2000, 250)
    # iter_gen = np.append(iter_gen, 1999)
    # iter_gen = [0, 252, 504, 756, 1002, 1254, 1500, 1752, 1998]
    # iter_gen = [0, 1, 2, 5, 10, 20, 50, 100, 250, 1000, 1999,
    #             2250, 2500, 2750, 3000, 3250, 3500, 3750, 3999]
    # iter_gen = [0, 250, 500, 750, 1000, 1250, 1500, 1750, 1999,
    #            2250, 2500, 2750, 3000, 3250, 3500, 3750, 3999]
    #iter_gen = [1, 2, 3, 10, 20, 30, 40, 300, 600, 900, 1000, 1300, 1600, 1900, 2300, 2500, 2800, 3100, 3400, 3700, 3990]




    R = 10
    Nbetas = 102
    betas = 10 ** np.linspace(-1, 1, Nbetas)
    if i_type == 'pred':
        numAgents = settings['pop_size_pred']
        size = settings['pred_size']
    elif i_type == 'prey':
        numAgents = settings['pop_size_prey']
        size = settings['prey_size']




    print('Loading data...')
    if i_type == 'pred':
        C_folder_name = 'C_pred'
    elif i_type == 'prey':
        C_folder_name = 'C_prey'

    C_folder = folder + '/' + C_folder_name

    if generation_list is None:
        generation_list = automatic_generation_generation_list(C_folder)

    iter_gen = generation_list

    C = np.zeros((R, numAgents, Nbetas, len(iter_gen)))

    for ii, iter in enumerate(iter_gen):
        #for bind in np.arange(0, 100):
        for bind in np.arange(1, 100):
            filename = folder + '/' + C_folder_name + '/C_' + str(iter) + '/C-size_' + str(size) + '-Nbetas_' + \
                       str(Nbetas) + '-bind_' + str(bind) + '.npy'
            C[:, :, bind, ii] = np.load(filename)
    print('Done.')

    plt.rc('text', usetex=True)
    font = {'family': 'serif', 'size': 28, 'serif': ['computer modern roman']}
    plt.rc('font', **font)
    plt.rc('legend', **{'fontsize': 20})

    b = 0.8
    alpha = 0.3

    print('Generating figures...')
    for ii, iter in enumerate(iter_gen):

        try:

            fig, ax = plt.subplots(1, 1, figsize=(11, 10), sharex=True)
            fig.text(0.51, 0.035, r'$\beta$', ha='center', fontsize=28)
            fig.text(0.005, 0.5, r'$C/N$', va='center', rotation='vertical', fontsize=28)
            title = 'Specific Heat of Foraging Community\n Generation: ' + str(iter)
            fig.suptitle(title)

            # CHANGE THIS TO CUSTOMIZE HEIGHT OF PLOT
            upperbound = 1.5 * np.max(np.mean(np.mean(C[:, :, :-40, :], axis=0), axis=0))
            # upperbound = np.max(np.mean(np.mean(C, axis=0)), axis=0)
            upperbound = 0.4

            label = iter

            for numOrg in range(numAgents):
                c = np.dot(np.random.random(), [1, 1, 1])
                ax.scatter(betas, np.mean(C[:, numOrg, :, ii], axis=0),
                           color=[0, 0, 0], s=30, alpha=alpha, marker='x', label=label)

            xticks = [0.1, 0.5, 1, 2, 4, 10]
            ax.set_xscale("log", nonposx='clip')
            ax.set_xticks(xticks)
            ax.get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())

            plt.axis([0.1, 10, 0, upperbound])

            # leg = plt.legend(loc=2, title='Generation')
            #
            # for lh in leg.legendHandles:
            #     lh.set_alpha(1)
            #     lh.set_sizes(30)
            if i_type == 'pred':
                savefolder = folder + '/figs_pred/C/'
            elif i_type == 'prey':
                savefolder = folder + '/figs_prey/C/'

            savefilename = savefolder + 'C-size_' + str(size) + '-Nbetas_' + \
                           str(Nbetas) + '-gen_' + str(iter) + '.png'
            if not path.exists(savefolder):
                makedirs(savefolder)

            plt.savefig(savefilename, bbox_inches='tight')
            plt.close()
            # plt.clf()
            savemsg = 'Saving ' + savefilename
            print(savemsg)
            # plt.show()
            # plt.pause(0.1)
        except Exception:
            print('Could not plot generation {} in sim {}'.format(iter, sim_name))

def automatic_generation_generation_list(C_folder):
    C_gen_folders = [f.path for f in os.scandir(C_folder) if f.is_dir()]
    generation_list = get_generations(C_gen_folders)
    return generation_list

def get_generations(C_gen_folders):
    generation_list = []
    for C_gen_folder in C_gen_folders:
        if RepresentsInt(C_gen_folder.split('_')[-1]) is True:
            generation_list.append(C_gen_folder.split('_')[-1])
    return generation_list

def RepresentsInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

if __name__ == '__main__':
    sim_name = 'sim-20200403-211835-g_4000_-t_2000_-b_10_-ref_250_-a_0_250_500_750_1000_1500_2000_3000_3999_-n_second_test_pred_prey'
    generation_list = [0, 1254]
    settings = load_settings(sim_name)
    main(sim_name, settings, None, 'pred')
