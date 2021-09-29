"""
Fila M/M/1
"""
import random
import simpy

ctdClientes = 10
tasaLlegada = 1.0 / 6.0        #Inverso del intervalo medio entre llegadas en minutos
tasaAsistencia = 1.0 / 5.0     #Inverso del tiempo medio de servicio en minutos

def llegadas(env):
    """ Genera las llegadas de los clientes al sistema """
    for i in range(ctdClientes):
        yield env.timeout(random.expovariate(tasaLlegada))
        name = 'Cliente %d' % (i+1)
        env.process(atendimento(env, name))

def atendimento(env, name):
    """ Simula la atención al cliente en el servidor 1 """
    print('%7.2f\t Llegada\t %s' % (env.now, name))
    atendReq = Servidor1.request()
    yield atendReq
    print('%7.2f\t Asistencia\t %s' % (env.now, name))
    yield env.timeout(random.expovariate(tasaAsistencia))
    Servidor1.release(atendReq)
    print('%7.2f\t Salida\t %s' % (env.now, name))
 
""" Main """
print('\nM/M/1\n')
print('Tiempo\t', 'Evento\t\t', 'Cliente\n')

random.seed(10)
env = simpy.Environment()
Servidor1 = simpy.Resource(env, capacity=1)
env.process(llegadas(env))
env.run()



# OUTPUT

# M/M/1

# Tiempo   Evento          Cliente  

#    5.08  Llegada         Cliente 1
#    5.08  Asistencia      Cliente 1
#    8.44  Llegada         Cliente 2
#    9.40  Salida  Cliente 1        
#    9.40  Asistencia      Cliente 2
#    9.83  Llegada         Cliente 3
#   17.79  Salida  Cliente 2        
#   17.79  Asistencia      Cliente 3
#   20.24  Llegada         Cliente 4
#   21.29  Llegada         Cliente 5
#   23.09  Salida  Cliente 3        
#   23.09  Asistencia      Cliente 4
#   25.07  Salida  Cliente 4        
#   25.07  Asistencia      Cliente 5
#   25.70  Llegada         Cliente 6
#   26.51  Salida  Cliente 5        
#   26.51  Asistencia      Cliente 6
#   44.02  Llegada         Cliente 7
#   44.29  Llegada         Cliente 8
#   54.87  Salida  Cliente 6        
#   54.87  Asistencia      Cliente 7
#   56.10  Llegada         Cliente 9 
#   58.98  Llegada         Cliente 10
#   59.49  Salida  Cliente 7
#   59.49  Asistencia      Cliente 8 
#   61.16  Salida  Cliente 8
#   61.16  Asistencia      Cliente 9 
#   66.78  Salida  Cliente 9
#   66.78  Asistencia      Cliente 10
#   69.83  Salida  Cliente 10
