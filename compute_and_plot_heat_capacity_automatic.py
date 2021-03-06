from automatic_plot_helper import detect_all_isings
from automatic_plot_helper import list_to_blank_seperated_str
from automatic_plot_helper import load_settings
import visualize_heat_capacity_generational_automatic
import os

def main(sim_name, settings, i_type, generations = None):
    if generations is None:
        gen_nums = detect_all_isings(sim_name, i_type)
        generations = [gen_nums[-1]]
    cores = settings['cores']
    compute_plot_heat_capacity(sim_name, generations, cores, settings, i_type)

def compute_plot_heat_capacity(sim_name, generation_list, cores, settings, i_type):
    gens_str = list_to_blank_seperated_str(generation_list)
    os.system('bash bash-heat-capacity-generational-automatic.sh {} "{}" {} {}'.format(sim_name, gens_str, cores, i_type))
    try:
        visualize_heat_capacity_generational_automatic.main(sim_name, settings, None, i_type)
    except Exception:
        print('Could not generate heat capacity plots for sim {}'.format(sim_name))

if __name__ == '__main__':

    #sim_name = 'sim-20200403-192708-g_5_-t_20_-ref_0_-tt_10'  # 'Laptop_HEL_runs/single_runs_HEL/sim-20200209-124814-ser_-b_10_-f_100_-n_1'#'sim-20200327-220128-g_8000_-b_1_-ref_2000_-a_500_1000_2000_4000_6000_8000_-n_3_sensors'
    sim_names = ['sim-20200403-211835-g_4000_-t_2000_-b_10_-ref_250_-a_0_250_500_750_1000_1500_2000_3000_3999_-n_second_test_pred_prey'] # ['sim-20200403-211845-g_4000_-t_2000_-b_1_-ref_250_-a_0_250_500_750_1000_1500_2000_3000_3999_-n_second_test_pred_prey', 'sim-20200403-211835-g_4000_-t_2000_-b_10_-ref_250_-a_0_250_500_750_1000_1500_2000_3000_3999_-n_second_test_pred_prey', 'sim-20200403-211857-g_4000_-t_2000_-b_0.1_-ref_250_-a_0_250_500_750_1000_1500_2000_3000_3999_-n_second_test_pred_prey']
    for sim_name in sim_names:
        cores = 20
        gen_nums = detect_all_isings(sim_name, 'pred')
        generation_list = [0, gen_nums[-1]]
        #generation_list = [0]
        settings = load_settings(sim_name)
        compute_plot_heat_capacity(sim_name, generation_list, cores, settings, 'pred')
        compute_plot_heat_capacity(sim_name, generation_list, cores, settings, 'prey')

