import matplotlib.pyplot as plt
import pandas as pd
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

def main(args):
    """
    Use:
    python genetic_satisfaction_from_csv.py tasks_path hours_per_day
    Parameters:
    tasks_path : path of the csv with tasks and values
    hours_per_day: number of hours you want to planificate

    Example:
    python genetic_satisfaction_from_csv.py task.csv 8
    """

    if len(args) == 2:
        
        tasks_path = str(args[0])
        hours_per_day = int(args[1])

        #all tasks will be listed
        task_pool_dataset = pd.read_csv(tasks_path)
        task_pool = []
        for i in range(len(task_pool_dataset)):
            task_pool.append([task_pool_dataset.iloc[i][0],int(task_pool_dataset.iloc[i][1]),int(task_pool_dataset.iloc[i][2])])
        

        #length of the individual
        len_ind = hours_per_day * 2

        #length of population
        len_pop = 100

        #number of generations
        num_gen = 1000

        #list of random individuals
        population=[]

        for i in range(len_pop):
            population.append(np.random.randint(0,len(task_pool),len_ind))

        #to see the progress
        satisfaction_mean = []

        #Evoluction
        for i in range(num_gen):
            #fitness
            fitness = []
            for ind in population:
                
                #long-term weight vs short-term weight
                ltw = 0.7
                stw = 0.3
                
                #boredom makes you prefer the short term
                b_factor = 0.025
                
                #individual mean
                ind_mean = 0
                
                #people don't like to do only one thing
                new_ix = []
                same_factor = np.ones(len(task_pool))*0.9
                
                for ix in ind:
                    if ix in new_ix:
                        ind_mean += (task_pool[ix][1]*ltw + task_pool[ix][2]*stw)*same_factor[ix]
                        same_factor[ix] = same_factor[ix]**2
                    else:
                        ind_mean += task_pool[ix][1]*ltw + task_pool[ix][2]*stw
                        new_ix.append(ix)

                    #boredom makes you prefer the short term
                    stw = stw + ltw*b_factor
                    ltw = ltw - ltw*b_factor
                    
                fitness.append(ind_mean/len(ind))
            fitness = np.array(fitness)
            print(fitness.mean())
            satisfaction_mean.append(fitness.mean())
            fitness = fitness/fitness.sum()
            
            #crossover
            offspring = []
            for i in range(len_pop//2):
                parents = np.random.choice(len_pop, 2, p=fitness)
                cross_point = np.random.randint(len_ind)
                offspring.append(list(population[parents[0]][:cross_point]) + list(population[parents[1]][cross_point:]))
                offspring.append(list(population[parents[1]][:cross_point]) + list(population[parents[0]][cross_point:]))
            
            #mutation
            population = mutar_poblacion(offspring,0.0025,num_task=len(task_pool))


        #lets see if we can maximize this
        plt.plot(satisfaction_mean)
        plt.show()

        best_ind=[]
        best=0

        for ind in population:
            
            #long-term weight vs short-term weight
            ltw = 0.7
            stw = 0.3
            
            #boredom makes you prefer the short term
            b_factor = 0.025
            
            #individual mean
            ind_mean = 0
            
            #people don't like to do only one thing
            new_ix = []
            same_factor = np.ones(len(task_pool))*0.9
            
            for ix in ind:
                if ix in new_ix:
                    ind_mean += (task_pool[ix][1]*ltw + task_pool[ix][2]*stw)*same_factor[ix]
                    same_factor[ix] = same_factor[ix]**2
                else:
                    ind_mean += task_pool[ix][1]*ltw + task_pool[ix][2]*stw
                    new_ix.append(ix)

                #boredom makes you prefer the short term
                stw = stw + ltw*b_factor
                ltw = ltw - ltw*b_factor

            ind_mean = ind_mean/len_ind
            if ind_mean > best:
                best = ind_mean
                best_ind.append(ind)

            if len(best_ind)>5:
                best_ind.pop(0)

        for i,ind in enumerate(best_ind):
            print("Plan ",i+1)
            for ix in ind:
                print(task_pool[ix][0])
            print()


    else:
        print(main.__doc__)

if __name__ == "__main__":
    import sys
    main(sys.argv[1:])




    
