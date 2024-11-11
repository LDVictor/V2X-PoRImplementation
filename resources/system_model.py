from comyx.network import UserEquipment, BaseStation, Link
from comyx.propagation import get_noise_power
from comyx.utils import dbm2pow, get_distance, generate_seed, db2pow
import numpy as np
from numba import jit
from matplotlib import pyplot as plt

def communication_v2n(msg_content):
    plt.rcParams["font.family"] = "STIXGeneral"
    plt.rcParams["figure.figsize"] = (6, 4)

    Pt = np.linspace(-10, 30, 80)  # dBm
    Pt_lin = dbm2pow(Pt)  # Watt
    frequency = 2.4e9  # Carrier frequency
    mc = 100000  # Number of channel realizations
    n_antennas = 1

    fading_args = {"type": "rayleigh", "sigma": 1 / 2}
    pathloss_args = {
        "type": "reference",
        "alpha": 3.5,
        "p0": 20,
        "frequency": frequency,
    }  # p0 is the reference power in dBm

    RAN = BaseStation("RAN", position=[0, 0, 10], n_antennas=1, t_power=Pt_lin)
    UE = UserEquipment("UE", position=[200, 200, 1], n_antennas=1)

    # Shapes for channels
    shape_bu = (n_antennas, n_antennas, mc)

    # Links
    link_ran_ue = Link(
        RAN, UE,
        fading_args, pathloss_args,
        shape=shape_bu, seed=generate_seed(msg_content),
    )
    return link_ran_ue




