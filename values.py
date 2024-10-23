import random

c_s = fpor_s = []
t_v = timestamp = t_approx = t_current = 0
d_approx = d_ran = []
n = random.randint(1, 20)

def generate_fpor_s():
    for i in range(0, n):
        value = random.random()
        fpor_s.append(value)

def generate_c_s():
    for i in range(0, n):
        value = random.randint(0, 1)
        c_s.append(value)

def generate_times():
    global t_v, timestamp, t_approx, t_current
    t_v = random.random() * random.randint(0, 100)
    timestamp = random.random() * random.randint(0, 50)
    t_approx = random.random() * random.randint(0, 100)
    t_current = random.random() * random.randint(0, 200)

def generate_coordinates():
    # coordenadas variam de 0 ate 180 graus
    d_approx0 = random.random() * random.randint(0, 180)
    d_approx1 = random.random() * random.randint(0, 180)
    d_approx.append(d_approx0)
    d_approx.append(d_approx1)
    d_ran0 = random.random() * random.randint(0, 180)
    d_ran1 = random.random() * random.randint(0, 180)
    d_ran.append(d_ran0)
    d_ran.append(d_ran1)


