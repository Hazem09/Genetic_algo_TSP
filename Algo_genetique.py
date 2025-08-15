import numpy as np, matplotlib.pyplot as plt
from matplotlib.pyplot import figure

class Population():
    '''Une classe où nous pouvons stocker la population, 
    générer la première population de manière aléatoire
    le score de chaque individu, les parents sélectionnés pour le crossover,
    l'individu avec le meilleur score et la matrice des distances.'''
    def __init__(self,villes, mat_distance,nbr_population):
        """Initialise une nouvelle population pour l'algorithme génétique.
        
        Args:
            villes: Liste ou plage des villes à visiter
            mat_distance: Matrice des distances entre les villes
            nbr_population: Nombre d'individus dans la population
        """
        # initialiser la première population de façon aléatoire  
        self.sac = np.asarray([np.random.permutation(villes) for _ in range(nbr_population)])
        self.parents = [] # une liste vide pour stocker les parents
        self.score = 0 # une variable pour stocker le score des individus 
        self.meilleur = None # une variable pour stocker le meilleur individu
        self.mat_distance = mat_distance # une variable pour stocker la matrice des distances


    def fitness(self, chromosome):
        """Cette fonction calcule le score des individus."""
        return sum(
            [
                self.mat_distance[chromosome[i], chromosome[i + 1]]
                for i in range(len(chromosome) - 1)
            ]
        )+self.mat_distance[chromosome[0], chromosome[len(chromosome) - 1]]

    def evaluate(self):
        '''Cette fonction évalue les individus et attribue une probabilité
        à chacun d'être sélectionné comme parent.  '''
        distances = np.asarray(
            [self.fitness(chromosome) for chromosome in self.sac]
        )

        self.score = np.min(distances) # stocker le meilleur score d'une generation.
        self.meilleur = self.sac[distances.tolist().index(self.score)] # stocker l'individu avec le meilleur score.
        self.parents.append(self.meilleur) # selectionneioné l'individu avec le meilleur score comme un parent.
        if False in (distances[0] == distances):
            # on recherche le score le plus élevé et nous soustrayons de celui-ci les valeurs des autres scores,
            # et nous stockons les résultats dans le même tableau en gardant les mêmes indices.
            distances = np.max(distances) - distances
        return distances / np.sum(distances) #ceci renvoie un tableau de probabilités

    def selectionne(self, nbr_parents):
        '''Cette fonction sélectionne les parents pour l'étape de crossover'''
        fit = self.evaluate() #On evalué la generation
        while len(self.parents) < nbr_parents: #k représent le nombre de parents a selectioné
            indice = np.random.randint(0, len(fit)) #on choisit un individu aléatoirement
            # on génère un nombre aléatoire entre 0 et 1 
            # et on le compare à la probabilité de l'individu d'être choisi ou non 
            if fit[indice] > np.random.rand(): 
                self.parents.append(self.sac[indice])
        self.parents = np.asarray(self.parents) #nous convertissons la liste des parents en tableau de numpy
    def crossover(self, p_cross):
        """Cette fonction effectue le crossover où elle sélectionne
        deux parents et en fonction de la probabilité."""
        enfants = []
        count, taille = self.parents.shape #On stocke la dimension du tableau des parents 
        for _ in range(len(self.sac)):
            # on génère un nombre aléatoire entre 0 et 1 et on le compare à la probabilité de crossover 
            # si le nombre est inférieur à la probabilité on effectue le crossover.
            if np.random.rand() > p_cross:
                # Si l'individu n'a pas été choisi, 
                # on le stock dans la liste des enfants pour la prochaine génération.  
                enfants.append(
                    list(self.parents[np.random.randint(count, size=1)[0]])
                )
            else:
                parent_1, parent_2 = self.parents[
                    np.random.randint(count, size=2), :
                ]
                # on génère deux nombres entiers aléatoires entre 0 et le nombre de gènes dans un individu.
                indice = np.random.choice(range(taille), size=2, replace=False)
                # nous stockons les deux nombres générés dans deux variables,
                # le plus petit nombre dans 'debut' et l'autre nombre dans 'fin'.
                debut, fin = min(indice), max(indice) 
                enfant = [None] * taille # on crée une liste enfant dont les valeurs sont 'None'.
                for i in range(debut, fin + 1, 1):
                    # on remplit l'enfant avec les gènes du premier père en gardant les mêmes indices, 
                    # on commence à l'indice 'debut' et on s'arrête à 'fin'.
                    enfant[i] = parent_1[i]
                pointeur = 0 
                for i in range(taille):
                    # maintenant, on remplit le reste avec les gènes manquants du deuxième parent dans le même ordre.
                    if enfant[i] is None:
                        while parent_2[pointeur] in enfant:
                            pointeur += 1
                        enfant[i] = parent_2[pointeur]
                enfants.append(enfant)
        return enfants


    def mutate(self, p_cross, p_mut):
        def swap(chromosome):
            '''Cette fonction permute les indices de deux villes dans un individu.'''
            # on génère deux nombres entiers aléatoires entre 0 et le nombre de gènes dans un individu.
            a, b = np.random.choice(len(chromosome), 2)
            # on change les indices des gènes dans l'individu  
            (chromosome[a], chromosome[b]) = (chromosome[b], chromosome[a])
            return chromosome
        '''Cette fonction exécute la mutation en utilisant la fonction swap.'''
        next_sac = [] # on crée une liste vide pour stocker la génération suivante. 
        enfants = self.crossover(p_cross) # on effectue le crossover sur la génération actuelle.
        for enfant in enfants:
            # on génère un nombre aléatoire entre 0 et 1 et on le compare à la probabilité de mutation 
            # si le nombre est inférieur à la probabilité on effectue le mutation.
            if np.random.rand() < p_mut:
                # si la condition est stratifiée on effectue la mutation   
                next_sac.append(swap(enfant))
            else:
                next_sac.append(enfant)
        self.parents=self.parents.tolist()        
        return next_sac


def genetic_algorithm(
    # les entrées de l'algorithme.
    villes, # La liste des villes.
    mat_distance, # La mtrice des disctances. 
    nbr_population, # Le nombre de popultaion.
    nbr_iteration, # Le nombre d'iteration (génération). 
    selectivity=0.2, # on sélectionne 20% de la population comme parents.
    p_cross=0.7, # La probability de croisement
    p_mut=0.1, # la probability de mutation.
):
    """Exécute l'algorithme génétique pour résoudre le problème du voyageur de commerce.
    
    Args:
        villes: La liste ou plage des villes à visiter
        mat_distance: La matrice des distances entre les villes 
        nbr_population: Le nombre d'individus dans la population
        nbr_iteration: Le nombre d'itérations (générations) à exécuter
        selectivity: Pourcentage de la population à sélectionner comme parents (par défaut 0.2)
        p_cross: Probabilité de croisement (par défaut 0.7)
        p_mut: Probabilité de mutation (par défaut 0.1)
    
    Returns:
        tuple: (score, meilleur) - Le meilleur score trouvé et la meilleure solution
    """
    pop = Population(villes, mat_distance, nbr_population) # Initialisation de la population.
    meilleur = pop.meilleur # Le variable où on stocke le meilleur individu. 
    score = float("inf") # On initialise la variable score avec une valeur infinie.
    histoire = [] # La liste où on stocke le score du meilleur individu de chaque génération.
    for i in range(nbr_iteration): # La boucle où l'on exécute l'algorithme.
        # Ici, on sélectionne les individus qui seront les parents et le nombre de parents en entrée.
        pop.selectionne(nbr_population * selectivity)
        histoire.append(pop.score) # on ajoute le score du meilleur individu de la génération à la liste.
        # ici, on compare le meilleur score de la génération actuelle avec le meilleur score actuel de tous les temps 
        # et on le stocke s'il est meilleur. 
        if pop.score < score:
            meilleur = pop.meilleur
            score = pop.score
        enfants = pop.mutate(p_cross, p_mut) #on effectue les opérations de croisement et de mutation.
        pop.sac = enfants # On prend les enfants de la génération actuelle comme individus pour la suivante.  

    # Les commandes pour créer le graphe.
    figure(figsize=(8, 6), dpi=100)   
    plt.plot(range(len(histoire)), histoire, color="blue",linewidth=1.0)
    plt.xlabel("Géneration")
    plt.ylabel("Score")
    plt.show()  
    return score, meilleur