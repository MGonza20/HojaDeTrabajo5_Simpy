'''
Juan Fernando Ramirez 20666
Sara María Paguaga Gonzáles 20634
'''

import random
import simpy
import statistics


RAM0 = 100
#random seed es el rango de aleatoriedad de nuestra simulacion
RANDOM_SEED =10
#Es una cifra de la cantidad de procesos generados que se debe cambiar para realizar las graficas
PROCESOS = 50
#El intervalo fue proporcionado por la HT
INTERVALO = 10
#Informacion proporcionada por la HT
#La velocidad del CPU se modela con que atiende un proceso en una 1 unidad de tiempo, lo cual permite realizar tres instrucciones.
VELOCIDADCPU = 3
#Procesos de entrada y salida
ProcesoIO = 1
#numero de procesadores
CPU = 1
#El tiempo en la simulación
time = []

#Función de los procesos del sistema

def procesos(env, name, state):
    #El enviroment del sistema operativo se inicializa en la variable inicio
    inicio = env.now
    ramProceso = random.randint(1, 10)  # RAM que se va a utilizar, en un intervalo de 1 a 10 con números random
    instrucciones = random.randint(1, 10)  # Acciones a realizar en el CPU, en un intervalo de 1 a 10 con números random
    print("El %s esta en estado %s y se acepto en %d" % (name, state, env.now)) #Se indica el estado del proceso y donde se crea

    with RAM1.get(ramProceso) as req1:  # En esta linea se remueve la RAM a utilizar
        yield req1
        state = "READY"  # Se le asigna estado "ready"
        print("El %s esta en estado %s y toma %s de RAM en %d" % (name, state, ramProceso, env.now)) #Se indica el estado del proceso, donde y que toma de RAM
        siguiente = 0
        while instrucciones >= 3:  # mientras que hayan 3 o mas instrucciones a atender
            with CPU.request() as req2:  # Se toma atencion del CPU
                print("El %s esta en estado %s espera espacio en CPU en %d" % (name, state, env.now)) #Se indica el estado del proceso y donde se espera espacio en el CPU
                yield req2
                state = "RUNNING" #Se asigna el estado "running" dadas las condiciones
                print("El %s esta en estado %s y  esta en CPU en %d" % (name, state, env.now)) #Se indica el estado del proceso y donde esta en el cpu

                instrucciones = instrucciones - VELOCIDADCPU  # Se procesa las instrucciones en el cpu
                yield env.timeout(1)

                if instrucciones >= 3:  # se genera numero random para saber si seguir corriendo o realizar un proceso de entrada salida (I/O)
                    siguiente = random.randint(1, 2)

                #Se realizqan operaciones de entrada y salida
                if siguiente == 1:
                    state = "WAIT" #Dada la condición anterior que siguiente es 1, asignar estado de espera "Wait"
                    print("El %s esta en operaciones I/0 en %d" % (name, env.now)) #Imprimir en donde se encuentra el proceso en operaciones I/O
                    yield env.timeout(ProcesoIO) #Se pasa el parámetro el valor de ProcesoIO para el timeout, es decir que pare
                if siguiente == 0:
                    instrucciones = 0 #Dada la condición anterior que siguiente es 1, asignar a instrucciones el valor 0

        state = "TERMINATED" # Se asigna estado finalizado o "Terminated"
        print("El %s esta en estado %s en %d" % (name, state, env.now)) #Se indica que el estado del proceso y donde
        RAM1.put(ramProceso)  # Se regresa RAM utilizada
    fin = env.now
    time.append(fin - inicio)  # Se calcula tiempo de processo
    time.append(fin - inicio)  # Se calcula tiempo de processo

#Se crea función para iniciar la simulación
def iniciarSimulacion(env, numero, intervalo):

    for i in range(numero + 1):
        state = "New" #Cuando se comienza se asigna estado "new"

        print("El Proceso " +str(i)+ " esta en estado " + state + " y se creo en " + str(int(env.now))) #Se indica el estado del proceso y donde se crea
        distribucion= random.expovariate(1.0 / intervalo)  # se asigna intervalo de creacion
        state = "WAIT"  # se asigna estado a "wait"
        p = procesos(env, "Proceso %02d" % i, state)  # se crea proceso
        env.process(p)
        yield env.timeout(distribucion)  # Tiempo que transcurrio para crear proceso

print("Se inicia el Sistema")
#Cuerpo
env = simpy.Environment()  # Se crea el envirnment
CPU = simpy.Resource(env, capacity=CPU)
RAM1 = simpy.Container(env, init=RAM0, capacity=RAM0)
random.seed(RANDOM_SEED)  # Se le coloca semilla al random para poder hacer comparaciones
 # Se renombra la memoriaRAM
env.process(iniciarSimulacion(env, PROCESOS, INTERVALO))  # Se crea el proceso
env.run()  # Se corre hasta que se acaben los procesos

#Se imprime el resumen de los datos estadísticos, los cuales son tiempo promedio de proceso y la desviación estandard
print("\n" * 1)
print("--------------------Estadisticas--------------------------")
print("")
print("El tiempo promedio de cada proceso fue de ", statistics.mean(time))
print("con una desviacion estandard de los datos de ", statistics.stdev(time))

print('Mirar: https://www.youtube.com/watch?v=4JkIs37a2JE mientras se simula ... ;-)')