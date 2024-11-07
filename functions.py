from p2pnetwork.node import Node
from values import vehicle_1, vehicle_2, ran

def verify_sw(t_v, timestamp):
    inf = t_v - timestamp
    sup = t_v + timestamp
    sw = (inf <= t_v <= sup)
    return sw

def calculate_fpor(tpor, dpor):
    fpor = (tpor + dpor) / 2
    return fpor

def calculate_tpor(t_approx, t_current):
    if t_current != 0:
        tpor = t_approx / t_current
    else:
        tpor = 0
    return tpor

def calculate_dpor(d_approx, d_ran):
    # latitude [0] e longitude [1]
    dpor = (d_approx[0] + d_approx[1]) / (d_ran[0] + d_ran[1])
    return dpor

def calculate_ic(c_s, fpor_s):
    sum = 0
    for i in range(len(fpor_s)):
        sum += (c_s[i] + fpor_s[i])
    ic = sum / len(fpor_s)
    return ic

def return_trust_ic(ic):
    return ic >= 0.5

def return_trust_rep(rep):
    return rep >= 3.5

def send_v2v_msg(msg_content):
    vehicle_1.connect_with_node('127.0.0.1', 8002)
    return vehicle_1.send_to_node(8002, msg_content)

def send_v2n_msg(msg_content):
    vehicle_1.connect_with_node('127.4.45.1', 9000)
    return vehicle_1.send_to_node(9000, msg_content)