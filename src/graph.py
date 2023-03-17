import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px

from init_test_data import trajet_en_df


def representation_itineraire_back(data: pd.DataFrame):
    """Affichage des N villes par des points ainsi que le parcours réalisé
       Le parcours est donné par l'ordre des villes dans le dataframe

    Parameters
    ----------
    data : DataFrame
        Dataframe stockant l'intégralité des coordonnées des villes à parcourir
    reseau_neurones : list
        list stockant un réseau de neurone de kohonen
    """
    # Affichage des points
    plt.scatter(data.iloc[:, 1], data.iloc[:, 2], zorder=1)
    # Repérage du point initial par un cercle rouge
    plt.scatter(data.iloc[0, 1], data.iloc[0, 2], zorder=1,
                color="red", marker='o', label='Point de Départ')
    plt.legend(loc="upper right")

    plt.show()


def representation_itineraire_web(data: pd.DataFrame) -> px:
    """Affichage des N villes par des points ainsi que le parcours réalisé
       Le parcours est donné par l'ordre des villes dans le dataframe

    Parameters
    ----------
    data : DataFrame
        Dataframe stockant l'intégralité des informations sur un algorithme

    Returns
    -------
    px
        Graphique de visualisation plolty
    """
    fig = px.line(data, x='x', y='y',
                  title='Chemin parcouru par le marchand', markers=True)
    return fig


def representation_temps_calcul(data: pd.DataFrame) -> px:
    """Affichage des du temps de calcul d'un algorithme en fonction
    du nombre de ville qu'il a traité

    Parameters
    ----------
    data : DataFrame
        Dataframe stockant l'intégralité des informations sur un algorithme

    Returns
    -------
    px
        Graphique de visualisation plolty
    """
    fig = px.line(data, x='Nombre de villes',
                  y='Temps de calcul (en s)', title='Représentation du temps de calcul en fonction du nombre de ville à explorer', markers=True)
    return fig


def affichage(df_resolution: pd.DataFrame, data: pd.DataFrame):
    """Affichage d'un trajet et des performances d'un algorithme

    Parameters
    ----------
    df_resolution : Dataframe
        variable stockant un ensemble de variables importantes pour analyser
        l'algorithme
    data : DataFrame
        Dataframe stockant l'intégralité des coordonnées des villes à parcourir

    Returns
    -------
    fig
        Graphique de visualisation plolty
    """
    df_meilleur_trajet = trajet_en_df(
        df_resolution['Solution'][0], data)
    # fig = representation_itineraire(df_meilleur_trajet)
    fig = representation_itineraire_web(df_meilleur_trajet)

    print("=============================================")
    print("Nombre de ville : ", df_resolution["Nombre de villes"][0])
    print("Distance : ", df_resolution["Distance"][0])
    print("Temps de calcul (en s): ",
          df_resolution["Temps de calcul (en s)"][0])
    print("=============================================")

    return fig
