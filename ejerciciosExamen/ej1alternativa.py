import multiprocessing
import psutil
import time
import os
import urllib3

"""
Crea dos procesos y lístalos usando psutil
El primer proceso estará 10 segundos vivo y matará al otro proceso, finalmente creará un fork de si mismo.
El segundo proceso a los 5 segundos cambiará la prioridad del primer proceso y lanzará el comando ping a la web de google
""" 

def funcionUno(dictPids):
    print(f"primer pid: {os.getpid()}")
    dictPids['pidUno'] = os.getpid()
    print(f"inicio proceso 1 con pid {dictPids['pidUno'] }")
    time.sleep(10)

    print("hora de matar")
    if psutil.pid_exists(dictPids['pidDos']):
        psutil.Process(dictPids['pidDos']).kill()
        print("proceso matado")
    else:
        print(f"proceso no eliminado, pid {dictPids['pidDos']} no encontrado")
    
    print("hora del fork")
    print(os.fork())

def funcionDos(dictPids):
    print(f"segundo pid: {os.getpid()}")
    dictPids['pidDos'] = os.getpid()
    print(f"inicio proceso 2 con pid {dictPids['pidDos']}")
    time.sleep(5)
    
    print("Hora de cambiar la prioridad del proceso")
    if psutil.pid_exists(dictPids['pidUno']):
        psutil.Process(dictPids['pidUno']).nice(1)
        print("prioridad cambiada")
    else:
        print(f"prioridad no cambiada, pid {dictPids['pidUno']} no encontrado")
        
    print("conectándome a google")
    os.system("ping -c 4 google.com")
    #tiempo para que el proceso no muera y que lo mate el primer proceso en vez
    time.sleep(15)


manager = multiprocessing.Manager()
dictPids = manager.dict({'pidUno': 0, 'pidDos': 0})
p1 = multiprocessing.Process(target=funcionUno, args=[dictPids])
p2 = multiprocessing.Process(target=funcionDos, args=[dictPids])
p1.start()
p2.start()
time.sleep(1)
print(f"el proceso 1 tiene pid {dictPids['pidUno']} y el proceso 2 tiene pid {dictPids['pidDos']}")
time.sleep(2)
print(psutil.pids())
p1.join()
p2.join()
print("ejecucion terminada")