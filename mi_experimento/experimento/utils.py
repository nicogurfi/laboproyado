# experimento/utils.py

import numpy as np

def generate_mean_list(mu, std, N):

    numeros = np.random.normal(loc=mu, scale=std, size=N)

    # Normalizar a media 0 y desviación estándar 1
    numeros = (numeros - np.mean(numeros)) / np.std(numeros, ddof=0)
    numeros = numeros * std + mu  # Escalar y trasladar

    rounded_numbers = np.around(numeros)
    rounded_mean = np.mean(rounded_numbers[:-1])

    # Calcular el valor del último número para que el promedio final sea exactamente mu
    last_number = mu * N - np.sum(rounded_numbers[:-1])
    final_numbers = list(rounded_numbers[:-1]) + [last_number]

    return final_numbers
