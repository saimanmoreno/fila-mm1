import random                           # gerador de números aleatórios
import simpy                            # biblioteca de simulação

TEMPO_MEDIO_CHEGADAS = 1.0              # tempo médio entre chegadas sucessivas de clientes
TEMPO_MEDIO_ATENDIMENTO = 0.5           # tempo médio de atendimento no servidor

def geraChegadas(env):
    # função que cria chegadas de entidades no sistema
    contaChegada = 0
    while True:
        # aguardo um intervalo de tempo exponencialmente distribuído
        yield env.timeout(random.expovariate(TEMPO_MEDIO_CHEGADAS))
        contaChegada += 1
        print('%.1f Chegada do cliente %d' % (env.now, contaChegada))

        # inicia o processo de atendimento
        env.process(atendimentoServidor(env, "cliente %d" % contaChegada, servidorRes))

def atendimentoServidor(env, nome, servidorRes):
    # função que ocupa o servidor e realiza o atendimento
    # armazena o instante de chegada do cliente
    chegada = env.now    
    # solicita o recurso servidorRes
    request = servidorRes.request()

    # aguarda em fila até a liberação do recurso e o ocupa
    yield request
    # calcula o tempo em fila
    tempoFila = env.now - chegada                  
    print('%.1f Servidor inicia o atendimento do %s. Tempo em fila: %.1f'
            % (env.now, nome, tempoFila))

    # aguarda um tempo de atendimento exponencialmente distribuído
    yield env.timeout(random.expovariate(TEMPO_MEDIO_ATENDIMENTO))
    print('%.1f Servidor termina o atendimento do %s. Clientes em fila: %i' 
            % (env.now, nome, len(servidorRes.queue)))

    # libera o recurso servidorRes
    yield servidorRes.release(request)

random.seed(25)                                 # semente do gerador de números aleatórios
env = simpy.Environment()                       # cria o environment do modelo
servidorRes = simpy.Resource(env, capacity=1)   # cria o recurso servidorRes
env.process(geraChegadas(env))                  # incia processo de geração de chegadas

env.run(until=5)                                # executa o modelo por 5 min