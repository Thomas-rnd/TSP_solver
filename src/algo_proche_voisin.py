import time

import numpy as np
import pandas as pd

from src.distance import distance_trajet


def plus_proche_voisin(matrice_distance: np.ndarray):
    """Retourne le trajet trouvé en se déplacement de proche en proche.

    La ville de départ étant arbitraire on choisit la ville d'index 0

    Parameters
    ----------
    matrice_distance : np.array
        matrice stockant l'integralité des distances inter villes

    Returns
    -------
    itineraire : list
        le chemin finalement trouvé
    temps_calcul : float
        temps necessaire à la résolution du problème
    chemins_explores : list
        stockage de l'ensemble des chemins explorés
    """
    start_time = time.time()

    # Initialiation du matrice booléenne d'état de visite des villes
    visite = np.zeros(len(matrice_distance)) != 0

    # Initialisation de l'itinéraire
    itineraire = [0]
    visite[0] = True

    # Stockage de l'ensemble des trajets explorés
    chemins_explores = [itineraire.copy()]

    while False in visite:
        # A chaque itération on cherche la ville la plus proche de la ville actuelle
        # la ville actuelle étant la dernière de l'itinéraire

        # Pour ne pas modifier les valeurs de matrice_distance
        distance_a_ville = np.copy(matrice_distance[itineraire[-1], :])

        for index in range(len(distance_a_ville)):
            if visite[index]:
                distance_a_ville[index] = np.Inf

        # Récupération de l'index de la ville la plus proche
        plus_proche = np.argmin(distance_a_ville)

        # On donne l'état visité à la ville
        visite[plus_proche] = True

        itineraire.append(int(plus_proche))
        # On copie la liste pour palier au type référence
        chemins_explore = itineraire.copy()

        chemins_explores.append(chemins_explore)

    # On fait attention à fermer le cycle
    itineraire.append(itineraire[0])

    temps_calcul = time.time() - start_time
    return itineraire, temps_calcul, chemins_explores


def main(matrice_distance: np.ndarray, nom_dataset="") -> pd.DataFrame:
    """Lancement de l'algorithme de recherche 

    Parameters
    ----------
    matrice_distance : np.array
        matrice stockant l'integralité des distances inter villes
    nom_dataset : str (optionnel)
        Nom du dataset à traiter

    Returns
    -------
    Dataframe
        variable stockant un ensemble de variables importantes pour analyser
        l'algorithme
    """
    # On récupère le chemin trouvé et le temps de résolution de l'algorithme
    itineraire, temps_calcul, chemins_explores = plus_proche_voisin(
        matrice_distance)

    # Calcul de la distance du trajet final trouvé par l'algorithme
    distance_chemin_sub_optimal = distance_trajet(itineraire, matrice_distance)

    # Chemin final trouvé
    solution = itineraire

    # Création du dataframe à retourner
    df_resultat_test = pd.DataFrame({
        'Algorithme': "plus_proche_voisin",
        'Nom dataset': nom_dataset,
        'Nombre de villes': len(solution),
        # Dans un tableau pour être sur une seule ligne du dataframe
        'Solution': [solution],
        'Chemins explorés': [chemins_explores],
        # Distance du trajet final
        'Distance': distance_chemin_sub_optimal,
        'Temps de calcul (en s)': temps_calcul
    })

    return df_resultat_test
