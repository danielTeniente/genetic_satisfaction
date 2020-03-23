import matplotlib.pyplot as plt
import numpy as np

def mutar_individuo(individuo,num_task):
    individuo_mutado = individuo.copy()
    ix = np.random.randint(len(individuo))    
    individuo_mutado[ix]= np.random.randint(num_task)
    return individuo_mutado
    
def mutar_poblacion(poblacion,prob_mutacion, num_task):
    nueva_poblacion = poblacion.copy()
    for i in range(len(poblacion)):
        if(np.random.random()<prob_mutacion):
            nueva_poblacion[i] = mutar_individuo(poblacion[i],num_task)
    return nueva_poblacion

#Algoritmo

#Pido al usuario
seguir = input("Desea ingresar una tarea (s/n): ")

task_pool = []

while seguir=='s':
    nombre_tarea = input("Ingrese la tarea: ")
    largo_plazo = int(input("Ingrese la satisfacción a largo plazo (0 - 10): "))
    corto_plazo = int(input("Ingrese la satisfacción a corto plazo (0 - 10): "))
    task_pool.append([nombre_tarea,largo_plazo,corto_plazo])
    seguir = input("Desea ingresar una tarea (s/n): ")

horas_disponibles = int(input("Cuántas horas tiene disponibles: "))
len_individuo = horas_disponibles*2

#Población
num_poblacion = 100

#generaciones
num_generaciones = 5000

population=[]

#Se crean individuos aleatorios
for i in range(num_poblacion):
    population.append(np.random.randint(0,len(task_pool),len_individuo))


#promedio de la satisfaccion
satisfaction_mean = []
    
#Evolución
for i in range(num_generaciones):
    #fitness
    fitness = []
    for individuo in population:
        
        #largo plazo - corto plazo
        peso_largo_plazo = 0.7
        peso_corto_plazo = 0.3
        
        #el aburrimiento hace que el corto plazo sea mejor
        factor_aburrimiento = 0.02
        
        #promedio del individuo
        promedio_ind=0
        
        #quiero evitar hacer la misma tarea varias veces
        new_ix = []
        factor_descuento = np.ones(len(task_pool))*0.8
        
        for j,ix in enumerate(individuo):
            if ix in new_ix:
                promedio_ind += (task_pool[ix][1]*peso_largo_plazo + task_pool[ix][2]*peso_corto_plazo)*factor_descuento[ix]
                factor_descuento[ix] = factor_descuento[ix]*0.6
            else:
                promedio_ind += task_pool[ix][1]*peso_largo_plazo + task_pool[ix][2]*peso_corto_plazo
                new_ix.append(ix)
        
            #largo plazo - corto plazo
            peso_corto_plazo = peso_corto_plazo + peso_largo_plazo*factor_aburrimiento
            peso_largo_plazo = peso_largo_plazo - peso_largo_plazo*factor_aburrimiento
            
        fitness.append(promedio_ind/len(individuo))
    fitness = np.array(fitness)
    satisfaction_mean.append(fitness.mean())
    fitness = fitness/fitness.sum()
    
    #entrecruzamiento
    offspring = []
    for i in range(num_poblacion//2):
        parents = np.random.choice(num_poblacion, 2, p=fitness)
        cross_point = np.random.randint(len_individuo)
        offspring.append(list(population[parents[0]][:len_individuo]) + list(population[parents[1]][len_individuo:]))
        offspring.append(list(population[parents[1]][:len_individuo]) + list(population[parents[0]][len_individuo:]))
    
    #mutación
    population = mutar_poblacion(offspring,0.0025,num_task=len(task_pool))

plt.plot(satisfaction_mean)
plt.show()

mejores_individuos=[]
best=0

for individuo in population:
    promedio_ind=0
    for ix in individuo:
        promedio_ind += task_pool[ix][1]*0.7 + task_pool[ix][2]*0.3
    promedio_ind = promedio_ind/len(individuo)
    if promedio_ind >= best:
        best = promedio_ind
        mejores_individuos.append(individuo)
    if len(mejores_individuos)>5:
        mejores_individuos.pop(0)

for individuo in mejores_individuos:
    print("Plan")
    for ix in individuo:
        print(task_pool[ix])
    print()
