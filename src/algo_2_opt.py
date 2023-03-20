import time

import numpy as np
import pandas as pd

from affichage_resultats import affichage
from distance import distance_trajet
from init_test_data import data_TSPLIB, trajet_en_df


# En s'inspirant de la documentation wikipedia sur le 2-opt pour résoudre le TSP, nous
# allons essayer de l'implémenter. Cet algorithme donne un résultat sub-optimal en temps
# très raisonnable. L'unique optimisation que nous réaliserons concerne la maj de la distance
# parcourue. En effet, on ne calculera uniquement la partie du trajet qui se verra modifiée
# à la suite de l'inversion. Cela concerne nous 2 arêtes du graph à parcourir.

# Cf. https://fr.wikipedia.org/wiki/2-opt


def gain(matrice_distance: np.array, meilleur_chemin: list, i: int, j: int) -> float:
    """Gain de distance en parcourant en sens inverse une suite de ville.

    On vient calculer la différence de distance entre la somme des anciennes arêtes et
    la somme des nouvelles arêtes formées. Si cette somme est positive on vient de trouver
    deux arêtes qui étaient sécantes avant l'inversion.

    Parameters
    ----------
    matrice_distance : np.array
        matrice stockant l'integralité des distances inter villes
    meilleur_chemin : list
        suite de villes donnant le chemin parcouru
    i : int
        indice de la ville où commence l'inversion
    j : int
        indice de la ville où finie l'inversion

    Returns
    -------
    float
        le gain effectif de l'inversion
    """
    avant_permutation = meilleur_chemin[i-1]
    debut_permutation = meilleur_chemin[i]
    fin_permutation = meilleur_chemin[j]
    apres_permuation = meilleur_chemin[j+1]

    # Distance avant inversion
    distance_initiale = matrice_distance[avant_permutation, debut_permutation
                                         ]+matrice_distance[fin_permutation, apres_permuation]
    # Distance après inversion
    distance_finale = matrice_distance[avant_permutation, fin_permutation
                                       ]+matrice_distance[debut_permutation, apres_permuation]
    return (distance_initiale-distance_finale)


def inversion(liste: list, debut_inversion: int, fin_inversion: int) -> list:
    """Inversion d'une partie du chemin parcouru

    Parameters
    ----------
    liste : list
        suite de villes donnant le chemin initialement parcouru
    debut_inversion : int
        index de la ville où l'inversion commence
    fin_inversion : int
        index de la ville où l'inversion finie

    Returns
    -------
    list
        Un nouveau parcours avec l'inversion réalisé
    """
    nouvelle_liste = liste[:debut_inversion] + \
        list(
        reversed(liste[debut_inversion:fin_inversion+1])) + liste[fin_inversion+1:]
    return nouvelle_liste


def deux_opt(itineraire_initial: list, matrice_distance: np.array) -> tuple(list, float):
    """Recherche de deux arêtes sécantes.

    Cette fonction implémente l'algorithme 2-opt décrit sur wikipédia.

    Parameters
    ----------
    itineraire_initial : list
        suite de villes donnant le chemin parcouru. Ce chemin initial influ énormément
        sur la solution finale trouvée.
    matrice_distance : np.array
        matrice stockant l'integralité des distances inter villes

    Returns
    -------
    chemin_explores : list
        l'ensemble des chemins sub-optimal trouvés
    temps_calcul : int
        temps necessaire à la résolution du problème
    """
    start_time = time.time()

    amelioration = True
    # Stockage du meilleur résultat courant
    meilleur_chemin = itineraire_initial
    meilleur_distance = distance_trajet(meilleur_chemin, matrice_distance)
    nombre_ville = len(meilleur_chemin)

    while amelioration:
        amelioration = False
        for debut_inversion in range(1, nombre_ville - 2):
            for fin_inversion in range(debut_inversion + 1, nombre_ville - 1):
                if (gain(matrice_distance, meilleur_chemin, debut_inversion, fin_inversion)) > 0:
                    nouveau_chemin = inversion(
                        meilleur_chemin, debut_inversion, fin_inversion)
                    nouvelle_distance = distance_trajet(
                        nouveau_chemin, matrice_distance)

                    if (nouvelle_distance < meilleur_distance):
                        meilleur_chemin = nouveau_chemin
                        meilleur_distance = nouvelle_distance
                        amelioration = True

    temps_calcul = time.time() - start_time
    return meilleur_chemin, temps_calcul


def main(matrice_distance: np.array, chemin_initial: list) -> pd.DataFrame:
    """Lancement de l'algorithme de recherche

    Parameters
    ----------
    matrice_distance : np.array
        matrice stockant l'integralité des distances inter villes
    chemin_initial : list
        suite de villes donnant le chemin parcouru. Ce chemin initial influ énormément
        sur la solution finale trouvée.

    Returns
    -------
    Dataframe
        variable stockant un ensemble de variables importantes pour analyser
        l'algorithme
    """
    # On récupère lechemin trouvé et le temps de résolution de l'algorithme
    itineraire, temps_calcul = deux_opt(chemin_initial, matrice_distance)

    # Calcul de la distance du trajet final trouvé par l'algorithme
    distance_chemin_sub_optimal = distance_trajet(itineraire, matrice_distance)
    # Chemin final trouvé
    solution = itineraire

    # Création du dataframe à retourner
    df_resultat_test = pd.DataFrame({
        'Algorithme': "2-opt",
        'Nombre de villes': len(chemin_initial),
        # Dans un tableau pour être sur une seule ligne du dataframe
        'Solution': [solution],
        # Erreur par rapport à la solution optimal de la TSPLIB
        'Distance': distance_chemin_sub_optimal,
        'Temps de calcul (en s)': temps_calcul
    })

    return df_resultat_test
