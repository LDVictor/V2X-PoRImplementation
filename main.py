import timeit
import functions

inicio = timeit.default_timer()
functions.calculate_fpor(0.5, 0.5)
fim = timeit.default_timer()
print("Duração: %f ms" % ((fim - inicio) * 1000))
