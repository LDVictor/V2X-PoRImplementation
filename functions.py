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

