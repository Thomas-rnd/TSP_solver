import time

import numpy as np

from distance import distance_trajet
from graph import representation_itineraire, affichage
from testData import data_TSPLIB, tour_optimal, trajet_en_df


def plus_proche_voisin(data, matrice_distance):
    """Retourne le trajet trouvé en se déplacement de proche en proche.
    La ville de départ étant arbitraire je choisis la ville d'index 0"""
    start_time = time.time()

    chemin_explore = []
    itineraire = [0]
    while len(data.loc['x']) != len(itineraire):
        # A chaque itération on cherche la ville la plus proche de la ville actuelle
        # la ville actuelle étant la dernière de l'itinéraire

        # Liste trié dans l'ordre croissant des distances entre la ville actuelle et le reste
        distances = sorted(matrice_distance[itineraire[-1]])

        # On enlève la distance qui correspond à rester sur la même ville
        distances.remove(0)

        i = 0
        # On recherche la ville la plus proche encore inexplorée
        while matrice_distance[itineraire[-1]].index(distances[i]) in itineraire:
            i += 1
        itineraire.append(
            matrice_distance[itineraire[-1]].index(distances[i]))
        chemin_explore.append(itineraire)
    itineraire.append(itineraire[0])

    temps_calcul = time.time() - start_time
    return chemin_explore, temps_calcul


def main(data, matrice_distance, chemin_optimal=[]):
    """Lancement de l'algorithme de recherche 

    Parameters
    ----------
    matrice_distance : list
        matrice stockant l'integralité des distances inter villes
    chemin_initial : list
        suite de villes donnant le chemin parcouru. Ce chemin initial influ énormément 
        sur la solution finale trouvée.
    chemin_optimal : list
        résulat optimal donné par la TSPLIB

    Returns
    -------
    dict
        variable stockant un ensemble de variables importantes pour analyser
        l'algorithme
    """
    if chemin_optimal != []:
        distance_chemin_optimal = distance_trajet(
            chemin_optimal, matrice_distance)

    resolution = {
        'Nombre de villes': 0,
        'Algorithme': 'Algorithme du plus proche voisin',
        'Distance': 'Euclidienne-2D',
        'Chemins': [],
        'Chemin optimal': chemin_optimal,
        'Erreur (en %)': 0,
        'Temps de calcul (en s)': 0
    }

    chemin_explore, temps_calcul = plus_proche_voisin(
        data, matrice_distance)

    resolution['Chemins'].extend(chemin_explore)
    distance_chemin_sub_optimal = distance_trajet(
        resolution['Chemins'][-1], matrice_distance)
    if chemin_optimal != []:
        erreur = 100*(distance_chemin_sub_optimal -
                      distance_chemin_optimal)/distance_chemin_optimal
        resolution['Erreur (en %)'] = erreur

    resolution['Nombre de villes'] = len(resolution['Chemins'][-1])
    resolution['Temps de calcul (en s)'] = temps_calcul
    return resolution
