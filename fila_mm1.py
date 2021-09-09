"""
Cola M/M/1
"""
import random
import simpy
import numpy as np
import scipy.stats as st

nClients = 100000
arrivalFee = 1.0 / 6.0      # inverse of the average interval between arrivals in minutes = lambda
attendFee = 1.0 / 5.0       # inverse of the average service time in minutes = mu
timesInQueue = []

def arrivals(env):
    """ Generates customer arrivals in the system """
    for i in range(nClients):
        yield env.timeout(random.expovariate(arrivalFee))
        name = 'Client %d' % (i+1)
        env.process(attendence(env, name))

def attendence(env, name):
    """ Simulates customer service on server 1 """
    arrival = env.now                   # guarda la hora de llegada del cliente
    # print('%7.2f\t Arrival\t %s' % (env.now, name))
    
    atendReq = Servidor1.request()      # solicita el recurso del servidor1
    yield atendReq                      # espera en la cola hasta la liberación del recurso para sólo entonces ocuparlo

    timeInQueue = env.now - arrival     # calcula el tiempo de espera
    timesInQueue.append(timeInQueue)    # crea una lista con el tiempo de espera de cada cliente

    # print('%7.2f\t Atendence\t %s\t Time in Queue: %7.2f' % (env.now, name, timeInQueue))
    
    # Si el cliente tarda más de 5s en la cola aborta la ejecución del programa
    # if timeInQueue > 5:
    #     print('\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
    #     print('TIME IN QUEUE IS OF %s IS MORE THAN 5 MINUTES (%7.2f)' % (name, timeInQueue))
    #     print('STOPING THE SIMULATION!')
    #     print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n')
    #     exit()

    yield env.timeout(random.expovariate(attendFee))    # espera un tiempo de servicio distribuido exponencialmente
    Servidor1.release(atendReq)                         # libera el recurso del servidor1

    # print('%7.2f\t Departure\t %s\t Clients in Queue: %d' % (env.now, name, len(Servidor1.queue)))

""" Main block """
print('\nM/M/1\n')
print('Time\t', 'Event\t\t', 'Client\n')

random.seed(27)
env = simpy.Environment()
Servidor1 = simpy.Resource(env, capacity=1)
env.process(arrivals(env))
env.run()

# Calcular el tiempo medio de espera en la cola
print('\n\nTIEMPO MEDIO DE ESPERA EN LA COLA >> %7.2f minutos' % (sum(timesInQueue)/len(timesInQueue)))

# Calcular teóricamente el tiempo medio de espera en una cola
'''
    Tmedio_espera_fila = lambda / (mu * (mu-lambda))

    lambda = 1 / Tmedio_entre_chegada

    mu = 1 / Tmedio_entre_atendimentos
'''
averageWaitTime = arrivalFee / (attendFee * (attendFee - arrivalFee))
print('TIEMPO MEDIO DE ESPERA EN LA COLA TEORICAMENTE >> %7.2f minutos\n\n' % (averageWaitTime))

# Calcule el intervalo de confianza del 95%.
'''
    confidence_interval = scipy.stats.t.interval(confidence_level, degrees_freedom, data_mean, data_standard_error)
    
    # Llama a scipy.stats.t.interval(alpha, df, mean, std) donde:
        df =  los grados de libertad, 
        mean = media de la muestra
        std = error estándar de la muestra para calcular un intervalo de confianza con el nivel de confianza alpha.

    confidence_level = 0.95
    degrees_freedom = data.size - 1     # Usa data.size - 1 con data como matriz de los datos de la muestra para encontrar los grados de libertad. 
    data_mean = np.mean(data)       # Llama a np.mean(data) para encontrar la media de los datos de la muestra data. 
    data_standard_error = scipy.stats.sem(data)     # Llama a scipy.stats.sem(data) para encontrar el error estándar de data.

'''
confidence_interval = st.t.interval(alpha=0.95, df=len(timesInQueue)-1,
              loc=np.mean(timesInQueue), scale=st.sem(timesInQueue))

# redondear los intervalos a tres decimales
confidence_interval = [round(num, 3) for num in confidence_interval]

print('INTERVALO DE CONFIANCA A 95%: ')
print(confidence_interval)
