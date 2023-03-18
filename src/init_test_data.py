import numpy
import pandas as pd

# http://comopt.ifi.uni-heidelberg.de/software/TSPLIB95/tsp/


def data_TSPLIB(fichier: str) -> pd.DataFrame:
    """
    Lecture d'un fichier au format .tsp en copiant les informations dans 
    un dataframe pandas

    Parameters
    ----------
    fichier : string 
        nom du fichier à traiter

    Returns
    -------
    DataFrame
        L'ensemble des villes ainsi crées depuis le fichier .tsp
    """
    with open(fichier) as f:
        noeud_coord_debut = None
        dimension = None
        lignes = f.readlines()

        # Lecture des informations du fichier .tsp
        i = 0
        while not dimension or not noeud_coord_debut:
            ligne = lignes[i]
            if ligne.startswith('DIMENSION :'):
                dimension = int(ligne.split()[-1])
            if ligne.startswith('NODE_COORD_SECTION'):
                noeud_coord_debut = i
            i = i+1

        # Définit le point de référence au début du fichier
        f.seek(0)

        # Read a data frame out of the file descriptor
        villes = pd.read_csv(
            f,
            # On commence la lecture du fichier au bon endroit
            skiprows=noeud_coord_debut + 1,
            # Le séparateur
            sep=' ',
            # Définition des colonnes du dataframe
            names=['Ville', 'x', 'y'],
            # Type des colonnes
            dtype={'Ville': str, 'x': np.float64, 'y': np.float64},
            header=None,
            nrows=dimension
        )

        return villes


def trajet_en_df(trajet: list, data: pd.DataFrame) -> pd.DataFrame:
    """Convertion d'un trajet en un dataframe

    Parameters
    ----------
    trajet : list
        list ordonne de villes
    data : DataFrame
        Dataframe stockant l'intégralité des coordonnées des villes à parcourir

    Returns
    -------
    DataFrame
        DataFrame ordonnées pour afficher le trajet
    """
    # Récupération des coordonnées des villes pour pouvoir les afficher
    x = []
    y = []
    index = []
    for i in trajet:
        x.append(data.iloc[i, 1])
        y.append(data.iloc[i, 2])
        index.append(i)
    # Un dataframe d'une ligne par ville
    df_res = pd.DataFrame({'Ville': index, 'x': x, 'y': y})
    return df_res


def tour_optimal(fichier='../data/ulysses22_opt_tour.txt'):
    """Lecture d'un jeu de données depuis un fichier .txt

    Lecture du chemin optimal

    Parameters
    ----------
    fichier : string
        nom du fichier à traiter

    Returns
    -------
    list
        liste optimale du parcours des villes
    """
    # Ouverture et lecture du fichier ligne par ligne
    with open(fichier, 'r') as input:
        data = [line.replace('\n', '') for line in input.readlines()]
    # -1 pour rester en correspondance avec le dataframe ville de 0 à n-1
    tour_optimal = [int(i)-1 for i in data]
    # On revient à la ville initiale
    tour_optimal.append(tour_optimal[0])
    return tour_optimal
