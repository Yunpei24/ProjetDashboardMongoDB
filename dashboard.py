import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu
from numerize.numerize import numerize
from models.country import Country
import requests


#####################################################################################################################

# Definition de l'URL de l'API
api_url = "https://josh-mongodb-api.onrender.com"



#####################################################################################################################
######################################### DEFINITION DES ENDPOINT DE L'API ##########################################

# L'endpoint pour l'insertion d'un pays à travers l'API
def insert_country(country: Country):
    """
    Insère un nouveau document de pays dans la collection MongoDB.

    Parameters:
    - country (Country): Un objet Country contenant les informations du pays à insérer.

    Returns:
    dict: Un dictionnaire contenant un message de confirmation et les données insérées.
    """
    country_dict = dict(country)
    response = requests.post(f"{api_url}/insert_country/", json=country_dict)
    if response.status_code == 200:
        return response.json()
    else:
        print("Error inserting data.")
        return None
    
# L'endpoint pour la mise à jour d'un pays à travers l'API
def update_country(id: str, country: Country):
    """
    Met à jour les informations d'un pays dans la collection MongoDB.

    Parameters:
    - id (str): L'ID du document de pays à mettre à jour.
    - country (Country): Un objet Country contenant les nouvelles informations du pays.

    Returns:
    dict: Un dictionnaire contenant un message de confirmation et les données mises à jour.
    """
    country_dict = dict(country)
    response = requests.put(f"{api_url}/update_country/{id}", json=country_dict)
    if response.status_code == 200:
        return response.json()
    else:
        print("Erreur lors de la mise à jour des données.")
        return None

# L'endpoint pour la suppression d'un pays à travers l'API
def delete_country(id: str):
    """
    Supprime un document de pays de la collection MongoDB.

    Parameters:
    - id (str): L'ID du document de pays à supprimer.

    Returns:
    dict: Un dictionnaire contenant un message de confirmation et les données supprimées.
    """
    response = requests.delete(f"{api_url}/delete_country/{id}")
    if response.status_code == 200:
        return response.json()
    else:
        print("Erreur lors de la suppression des données.")
        return None

# Definition de l'endpoint pour recuperer toutes les informations de tous les pays
def get_countries():
    """
    Récupère toutes les informations des pays depuis la collection MongoDB à travers l'API et les renvoie au format d'un dataframe.

    Returns:
    DataFrame: Un objet DataFrame contenant les données des pays.
    """
    response = requests.get(f"{api_url}/countries_info/")
    if response.status_code == 200:
        df = pd.DataFrame(response.json())
        colonnes_a_convertir = ["area", "landAreaKm", "netChange", "growthRate", "worldPercentage", "density"]
        for colonne in colonnes_a_convertir:
            # si df[colonne] est non vide
            if not df[colonne].isnull().all():
                df[colonne] = df[colonne].astype(float) # on applique la fonction numerize à la colonne pour convertir les valeurs en chiffres 
        return df
    else:
        print("Erreur lors de la récupération des données.")
        return None

    
# Definition de l'endpoint pour recuperer les pays dont la densité est comprise entre deux valeurs
def get_countries_density_between(min_density: float, max_density: float):
    """
    Récupère les noms des pays et leurs densités comprises entre deux valeurs depuis la collection MongoDB à travers l'API et les renvoie au format d'un dataframe.

    Parameters:
    - min_density (float): La valeur minimale de la densité.
    - max_density (float): La valeur maximale de la densité.

    Returns:
    DataFrame: Un objet DataFrame contenant les noms des pays et leurs densités comprises entre deux valeurs.
    """
    response = requests.get(f"{api_url}/countries_density/{min_density}/{max_density}")
    if response.status_code == 200:
        df = pd.DataFrame(response.json())
        return df
    else:
        print("Erreur lors de la récupération des données.")
        return None
    
# Definition de l'endpoint pour recuperer le pays le plus peuplé suivant l'année sélectionnée
def get_most_populated_country(year: int):
    """
    Récupère le pays le plus peuplé suivant l'année sélectionnée depuis la collection MongoDB à travers l'API et le renvoie au format d'un dataframe.

    Returns:
    DataFrame: Un objet DataFrame contenant le pays le plus peuplé.
    """
    response = requests.get(f"{api_url}/country_most_populated/{year}")
    if response.status_code == 200:
        df = pd.DataFrame(response.json())
        return df
    else:
        print("Erreur lors de la récupération des données.")
        return None

# Definition de l'endpoint pour recuperer le pays le moins peuplé suivant l'année sélectionnée
def get_least_populated_country(year: int):
    """
    Récupère le pays le moins peuplé suivant l'année sélectionnée depuis la collection MongoDB à travers l'API et le renvoie au format d'un dataframe.

    Returns:
    DataFrame: Un objet DataFrame contenant le pays le moins peuplé.
    """
    response = requests.get(f"{api_url}/country_least_populated/{year}")
    if response.status_code == 200:
        df = pd.DataFrame(response.json())
        return df
    else:
        print("Erreur lors de la récupération des données.")
        return None


# Definition de l'endpoint pour recuperer les pays et leurs populations de 1980 à 2050
def get_countries_pop():
    """
    Récupère les noms des pays et leurs populations de 1980 à 2050 depuis la collection MongoDB à travers l'API et les renvoie au format d'un dataframe.

    Returns:
    DataFrame: Un objet DataFrame contenant les noms des pays et leurs populations de 1980 à 2050.
    """
    response = requests.get(f"{api_url}/countries_pop/")
    if response.status_code == 200:
        df = pd.DataFrame(response.json())
        return df
    else:
        print("Erreur lors de la récupération des données.")
        return None

# Definition de l'endpoint pour recuperer un pays et ses informations grace à son nom
def get_country_by_name(country_name: str):
    """
    Récupère les informations d'un pays depuis la collection MongoDB à travers l'API et les renvoie au format d'un dataframe.

    Parameters:
    - country_name (str): Le nom du pays à récupérer.

    Returns:
    DataFrame: Un objet DataFrame contenant les informations du pays.
    """
    response = requests.get(f"{api_url}/country/{country_name}")
    if response.status_code == 200:
        df = pd.DataFrame(response.json())
        return df
    else:
        print("Country not found.")
        return None

# Definition de l'endpoint pour recuperer la moyenne de la population mondiale par année (de 1980 à 2050)
def get_world_pop_avg():
    """
    Récupère la moyenne de la population mondiale par année (de 1980 à 2050) depuis la collection MongoDB à travers l'API et les renvoie au format d'un dataframe.

    Returns:
    DataFrame: Un objet DataFrame contenant la moyenne de la population mondiale par année.
    """
    response = requests.get(f"{api_url}/average_pop/")
    if response.status_code == 200:
        df = pd.DataFrame(response.json())
        return df
    else:
        print("Erreur lors de la récupération des données.")
        return None

# Definition de l'endpoint pour recuperer les pays dont la superficie est comprise entre deux valeurs
def get_countries_area_between(min_area: float, max_area: float):
    """
    Récupère les noms des pays et leurs superficies comprises entre deux valeurs depuis la collection MongoDB à travers l'API et les renvoie au format d'un dataframe.

    Parameters:
    - min_area (float): La valeur minimale de la superficie.
    - max_area (float): La valeur maximale de la superficie.

    Returns:
    DataFrame: Un objet DataFrame contenant les noms des pays et leurs superficies comprises entre deux valeurs.
    """
    response = requests.get(f"{api_url}/countries_areas_sup1_sup2/{min_area}/{max_area}")
    if response.status_code == 200:
        df = pd.DataFrame(response.json())
        return df
    else:
        print("Erreur lors de la récupération des données.")
        return None

# Définition de l'endpoint pour pour exécuter une requête personnalisée d'agrégation
def get_custom_aggregation(query: str):
    """
    Exécute une requête personnalisée d'agrégation sur la collection MongoDB à travers l'API et renvoie le résultat au format d'un dataframe.

    Parameters:
    - query (str): La requête d'agrégation à exécuter.

    Returns:
    DataFrame: Un objet DataFrame contenant le résultat de la requête d'agrégation.
    """
    response = requests.get(f"{api_url}/custom_aggregation/{query}")
    if response.status_code == 200:
        df = pd.DataFrame(response.json())
        return df
    else:
        print("Erreur lors de l'exécution de la requête.")
        return None

# Définition de l'endpoint pour pour exécuter une requête personnalisée find
def get_custom_find(query: str):
    """
    Exécute une requête personnalisée find sur la collection MongoDB à travers l'API et renvoie le résultat au format d'un dataframe.

    Parameters:
    - query (str): La requête find à exécuter.

    Returns:
    DataFrame: Un objet DataFrame contenant le résultat de la requête find.
    """
    response = requests.get(f"{api_url}/custom_find/{query}")
    if response.status_code == 200:
        df = pd.DataFrame(response.json())
        return df
    else:
        print("Erreur lors de l'exécution de la requête.")
        return None

#Définition de l'endpoint pour pour exécuter une requête personnalisée distinct
def get_custom_distinct(query: str):
    """
    Exécute une requête personnalisée distinct sur la collection MongoDB à travers l'API et renvoie le résultat au format d'un dataframe.

    Parameters:
    - query (str): La requête distinct à exécuter.

    Returns:
    DataFrame: Un objet DataFrame contenant le résultat de la requête distinct.
    """
    response = requests.get(f"{api_url}/custom_distinct/{query}")
    if response.status_code == 200:
        df = pd.DataFrame(response.json())
        return df
    else:
        print("Erreur lors de l'exécution de la requête.")
        return None

# Definition de l'endpoint pour avoir ne nombre de pays qui ont une population supérieure à la moyenne mondiale par année
def get_countries_pop_sup_avg(year: int):
    """
    Récupère le nombre de pays qui ont une population supérieure à la moyenne mondiale par année depuis la collection MongoDB à travers l'API et les renvoie au format d'un dataframe.

    Returns:
    DataFrame: Un objet DataFrame contenant le nombre de pays qui ont une population supérieure à la moyenne mondiale par année et la moyenne de la population.
    """
    response = requests.get(f"{api_url}/nb_countries_supavg/{year}")
    if response.status_code == 200:
        #df = pd.DataFrame()
        return response.json()
    else:
        print("Erreur lors de la récupération des données.")
        return None

# Definition de l'endpoint pour avoir le nombre de pays qui ont une population inférieure à la moyenne mondiale par année
def get_countries_pop_inf_avg(year: int):
    """
    Récupère le nombre de pays qui ont une population inférieure à la moyenne mondiale par année depuis la collection MongoDB à travers l'API et les renvoie au format d'un dataframe.

    Returns:
    DataFrame: Un objet DataFrame contenant le nombre de pays qui ont une population inférieure à la moyenne mondiale par année et la moyenne de la population.
    """
    response = requests.get(f"{api_url}/nb_countries_infavg/{year}")
    if response.status_code == 200:
        
        return response.json()
    else:
        print("Erreur lors de la récupération des données.")
        return None

#####################################################################################################################
############################################ CONSTRUCTION DU DASHBOARD ##############################################

# Fonction pour recupéerer tous les dataframes
def get_all_kinde_of_df():
    df_all = get_countries()
    df_countries_pop = get_countries_pop()

    return df_all, df_countries_pop


def Filter(df_all):
    st.sidebar.header("🔍  Filter by")
    country = st.sidebar.multiselect(
        "Select Country",
        options=df_all["country"].unique(),
        #default=df_all["country"].unique()[:4],
    )
    place = st.sidebar.multiselect(
        "Select Place",
        options=df_all["place"].unique(),
        #default=df_all["place"].unique()[:4],
    )
    density = st.sidebar.multiselect(
        "Select Density",
        options=df_all["density"].unique(),
        #default=df_all["density"].unique()[:4],
    )

    df_selection_in_col = df_all.query(
        "country == @country | (place == @place & density == @density)"
    )

    # compter le nombre d'éléments filtrés
    cpt = len(df_selection_in_col)

    return df_selection_in_col, cpt


def graph_Collection(df_selection, nombre_elmt):

    # Top nombre_elmt des pays les plus peuplés
    st.subheader(f"📊 Top {nombre_elmt} most densely populated countries in 2023")

    # On récupère les 10 pays les plus peuplés en 2023
    df_top = df_selection.sort_values(by="pop2023", ascending=False).head(nombre_elmt)
    # On affiche le graphique
    fig_top = px.bar(
        df_top,
        x="country",
        y="pop2023",
        color="country",
        orientation="v",
        title=f"Top {nombre_elmt} most densely populated countries in 2023",
        template="plotly_white",
    )
    fig_top.update_layout(
        xaxis_title="Pays",
        yaxis_title="Population",
        legend_title="Pays",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=(dict(showgrid=False)),
        width=1000,
        height=400
    )
    st.write(fig_top)

    # Tendance démographique pour certains pays
    st.subheader("📊 Demographic trends for some countries")

    # Recuperer les pays à partir du dataframe
    countries = df_selection["country"].unique().tolist()

    # Les pays à selectionner
    #countries = ['India', 'China', 'United States', 'United Kingdom', 'Japan', 'Australia']

    years = ['pop1980', 'pop2000', 'pop2010', 'pop2023','pop2030','pop2050']  

    # Créer un sous-ensemble des données pour les pays sélectionnés
    country_data = df_selection[df_selection['country'].isin(countries)]

    # Transformer les données pour avoir les années et les populations dans un format tabulaire
    df = country_data.melt(id_vars=['country'], value_vars=years, var_name='Year', value_name='Population')

    # Utiliser Plotly Express pour créer le graphique
    fig_tendance = px.line(
        df,
        x='Year',
        y='Population',
        color='country',
        labels={"Year": "Year", "Population": "Population", "Country": "Country"},
        title="Population Trend for Selected Countries",
        template="plotly_white",
    )
    fig_tendance.update_layout(
        xaxis_title="Years",
        yaxis_title="Population",
        legend_title="Pays",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=(dict(showgrid=False)),
        width=1000,
        height=400
    )
    # Afficher le graphique interactif avec Streamlit
    st.plotly_chart(fig_tendance)
    #st.write(fig_tendance)

def all_Collection(df_selection, cpt):
    with st.expander("⏰ My MongoDB's Collection WorkBook"):
        showData = st.multiselect('Filter: ', df_selection.columns, default=df_selection.columns.tolist())
        st.dataframe(df_selection[showData], use_container_width=True)
    
    total_population = float(df_selection["pop2023"].sum())
    population_mode = float(df_selection["pop2023"].mode().iloc[0]) if not df_selection["pop2023"].mode().empty else 0.0
    population_mean = float(df_selection["pop2023"].mean()) if not df_selection["pop2023"].empty else 0.0
    population_median = float(df_selection["pop2023"].median()) if not df_selection["pop2023"].empty else 0.0

    total1, total2, total3, total4 = st.columns(4, gap='large')

    with total1:
        st.info("Total Population in 2023", icon="📌")
        st.metric(label="Total Population", value=f"{total_population:,.0f}")
    
    with total2:
        st.info("Population Mode in 2023", icon="📌")
        st.metric(label="Population Mode", value=f"{population_mode:,.0f}")

    with total3:
        st.info("Population Mean in 2023", icon="📌")
        st.metric(label="Population Mean", value=f"{population_mean:,.0f}")
    
    with total4:
        st.info("Population Median in 2023", icon="📌")
        st.metric(label="Population Median", value=f"{population_median:,.0f}")

    st.markdown("""---""")

    graph_Collection(df_selection, cpt)

# Fonction pour la page permettant d'inserer, mettre à jour et supprimer un pays dans la collection MongoDB grace à l'API declenché par des boutons
def formulaire_country():
    country = st.text_input("Country")
    rank = st.number_input("Rank", min_value=0, max_value=250)
    area = st.number_input("Area", min_value=1.0)
    landAreaKm = st.number_input("Land Area (km²)", min_value=0.0)
    cca2 = st.text_input("CCA2")
    cca3 = st.text_input("CCA3")
    netChange = st.number_input("Net Change", min_value=0.0)
    growthRate = st.number_input("Growth Rate", min_value=-1.1, max_value=1.0)
    worldPercentage = st.number_input("World Percentage", min_value=0.0, max_value=1.0)
    density = st.number_input("Density", min_value=0.0)
    densityMi = st.number_input("Density (mi²)", min_value=0.0)
    place = st.number_input("Place", min_value=0)
    pop1980 = st.number_input("Population in 1980", min_value=0)
    pop2000 = st.number_input("Population in 2000", min_value=0)
    pop2010 = st.number_input("Population in 2010", min_value=0)
    pop2022 = st.number_input("Population in 2022", min_value=0)
    pop2023 = st.number_input("Population in 2023", min_value=0)
    pop2030 = st.number_input("Population in 2030", min_value=0)
    pop2050 = st.number_input("Population in 2050", min_value=0)

    area = 0 if area == 1 else area
    growthRate = 0 if growthRate == -1.1 else growthRate


    # On crée l'objet Country
    country = Country(
        country=country,
        rank=rank,
        area=area,
        landAreaKm=landAreaKm,
        cca2=cca2,
        cca3=cca3,
        netChange=netChange,
        growthRate=growthRate,
        worldPercentage=worldPercentage,
        density=density,
        densityMi=densityMi,
        place=place,
        pop1980=pop1980,
        pop2000=pop2000,
        pop2010=pop2010,
        pop2022=pop2022,
        pop2023=pop2023,
        pop2030=pop2030,
        pop2050=pop2050
    )

    return country


def insert_update_delete_country(): # IUDC
    st.subheader("📝 Insert, Update and Delete a Country")

    # On récupère l'action à effectuer
    action = st.radio("Action", ["Insert", "Update", "Delete"])

    # Si l'action est "Insert"
    if action == "Insert":
        # On récupère les informations du pays à insérer
        country = formulaire_country()

        # On récupère le bouton soumis
        if st.button(action):
        # On insère le pays
            response = insert_country(country)
            # Si la réponse est valide
            if response is not None:
                # On affiche un message de confirmation
                st.success("Successfully inserted data.")
                # Créer un dataframe avec les données insérées (country)
                df = pd.DataFrame([country.__dict__])
                # On affiche les données insérées dans un tableau vertical
                st.table(df.T)
                
            else:
                # On affiche un message d'erreur
                st.error("Error inserting data.")
    # Si l'action est "Update"
    elif action == "Update":
        # On récupère l'ID du document à mettre à jour
        id = st.text_input("ID")
        # On récupère les informations du pays à mettre à jour
        country = formulaire_country()

        if st.button(action):
            # On met à jour le pays
            response = update_country(id, country)
            # Si la réponse est valide
            if response is not None:
                # On affiche un message de confirmation
                st.success("Successfully updated data.")
                df = pd.DataFrame([country.__dict__])
                # On affiche les données insérées dans un tableau vertical
                st.table(df.T)
            else:
                # On affiche un message d'erreur
                st.error("Error updating data.")
    # Si l'action est "Delete"
    elif action == "Delete":
        # On récupère l'ID du pays à supprimer
        id = st.text_input("ID")

        if st.button(action):
            # On supprime le pays
            response = delete_country(id)
            # Si la réponse est valide
            if response is not None:
                # On affiche un message de confirmation
                st.success("Successfully deleted data.")
                df = pd.DataFrame([country.__dict__])
                # On affiche les données insérées dans un tableau vertical
                st.table(df.T)
            else:
                # On affiche un message d'erreur
                st.error("Error deleting data.")
           
# Graphe superficie des pays
def graph_area(df_area):
    st.subheader("📊 Area of countries")
    # On affiche le graphique
    fig_area = px.bar(
        df_area,
        x="country",
        y="area",
        color="country",
        title="Area of countries"
    )
    fig_area.update_layout(
        xaxis_title="Countries",
        yaxis_title="Area (km²)",
        legend_title="Countries",
        font=dict(
            family="Courier New, monospace",
            size=15, # revoir la taille de la police
            color="RebeccaPurple"
        ),
        width=1000,
        height=600
    )
    st.write(fig_area)

# Fonction pour la page permettant de recuperer les pays et leurs superficies et de les afficher dans un tableau ainsi qu'un graphique
def countries_area(df_area):
    st.subheader("📝 Countries and their area")

    # Saisr le nombre de pays à afficher
    nombre_elmt = st.number_input("Number of countries to display", min_value=1, max_value=250, value=10)

    # On récupère les nombre_elmt premiers éléments du dataframe
    df_area_new = df_area.head(nombre_elmt)

    # Creation d'un dataframe avec le nom du pays et sa superficie
    df_area_new = pd.DataFrame({
        "country": df_area_new["country"],
        "area": df_area_new["area"]
    })

    # On affiche les données (nom du pays et sa superficie) dans un tableau
    st.dataframe(df_area_new, use_container_width=True)

    # On affiche le graphique
    graph_area(df_area_new)

# Map suivant la population de 2000, 2010 et 2023
def map_population(df_selection):
    # On affiche la carte
    fig_map_00 = px.choropleth(
        df_selection,
        locations="country",
        locationmode="country names",
        color="pop2000",
        hover_name="country",
        title="Map of the population in 2000",
        color_continuous_scale='Viridis',
    )
    fig_map_00.update_layout(
        legend_title="Pays",
        font=dict(
            family="Franklin Gothic",
            size=15,
            color="RebeccaPurple"
        ),
        width=1000,
        height=600
    )
    st.write(fig_map_00)

    fig_map_10 = px.choropleth(
        df_selection,
        locations="country",
        locationmode="country names",
        color="pop2010",
        hover_name="country",
        title="Map of the population in 2010",
        color_continuous_scale='Viridis',
    )
    fig_map_10.update_layout(
        legend_title="Pays",
        font=dict(
            family="Franklin Gothic",
            size=15,
            color="RebeccaPurple"
        ),
        width=1000,
        height=600
    )
    st.write(fig_map_10)

    fig_map_23 = px.choropleth(
        df_selection,
        locations="country",
        locationmode="country names",
        color="pop2023",
        hover_name="country",
        title="Map of the population in 2023",
        color_continuous_scale='Viridis',
    )
    fig_map_23.update_layout(
        legend_title="Pays",
        font=dict(
            family="Franklin Gothic",
            size=15,
            color="RebeccaPurple"
        ),
        width=1000,
        height=600
    )
    st.write(fig_map_23)

# Fonction pour créer la page où sera affiché la map
def map_page(df_selection):
    # Bouton pour afficher les cartes
    submitted = st.button("Show Maps")

    # Si le bouton est soumis
    if submitted:
        # On affiche le dataframe
        st.dataframe(df_selection, use_container_width=True)

        # On affiche les cartes
        map_population(df_selection)


# Page pour des requêtes spécifique sur la collection MongoDB
def specific_request():
    # Trouver un pays par son nom
    country_name = st.text_input("Country Name")
    btn_cn = st.button("Find Country")
    # On récupère le bouton soumis
    if btn_cn:
        # On récupère les informations du pays
        df_country = get_country_by_name(country_name)
        # Si le pays existe
        if df_country is not None:
            # On affiche un message de confirmation
            st.success("The data has been successfully recovered.")
            # On affiche les données récupérées
            st.dataframe(df_country)
        else:
            # On affiche un message d'erreur
            st.error("Country not found!")
    st.markdown("""---""")
    # Saisr l'année (1980, 2000, 2010, 2023, 2030, 2050)
    year = st.radio("Year", [1980, 2000, 2010, 2023, 2030, 2050])
    # Trouver le pays le plus peuplé
    st.subheader("📝 Find the most populated country following the year")
    btn_mpc = st.button("Shearch The Most Populated Country")
    # On récupère le bouton soumis
    if btn_mpc:
        # On récupère les informations du pays
        df_mpc = get_most_populated_country(int(year))
        # Si le pays existe
        if df_mpc is not None:
            # On affiche un message de confirmation
            st.success("The data has been successfully recovered.")
            # On affiche les données récupérées
            st.dataframe(df_mpc)
        else:
            # On affiche un message d'erreur
            st.error("Error when recovering data!")
    st.markdown("""---""")
    # Trouver le pays le moins peuplé
    st.subheader("📝 Find the least populated country following the year")
    # Saisr l'année (1980, 2000, 2010, 2023, 2030, 2050)
    btn_lpc = st.button("Shearch The Least Populated Country")
    # On récupère le bouton soumis
    if btn_lpc:
        # On récupère les informations du pays
        df_lpc = get_least_populated_country(int(year))
        # Si le pays existe
        if df_lpc is not None:
            # On affiche un message de confirmation
            st.success("The data has been successfully recovered.")
            # On affiche les données récupérées
            st.dataframe(df_lpc)
        else:
            # On affiche un message d'erreur
            st.error("Error when recovering data!")
    st.markdown("""---""")
    # Trouver les pays dont la superficie est comprise entre deux valeurs
    st.subheader("📝 Find countries whose area is between two values")
    # Saisr la valeur minimale
    min_area = st.number_input("Minimum value", min_value=10.0)
    # Saisr la valeur maximale
    max_area = st.number_input("Maximum value", min_value=20.0)
    btn_ca = st.button("Shearch Countries", key="ca")
    # On récupère le bouton soumis
    if btn_ca:
        if min_area < max_area:
            # On récupère les informations des pays
            df_ca = get_countries_area_between(min_area, max_area)
            # Si les pays existent
            if df_ca is not None:
                # On affiche un message de confirmation
                st.success("The data has been successfully recovered.")
                # On affiche les données récupérées
                st.dataframe(df_ca)
            else:
                # On affiche un message d'erreur
                st.error("Error when recovering data!")
        else:
            # On affiche un message d'erreur
            st.error("The minimum value must be less than the maximum value!")
    st.markdown("""---""")
    # Trouver les pays dont la densité est comprise entre deux valeurs
    st.subheader("📝 Find countries whose density is between two values")
    # Saisr la valeur minimale
    min_density = st.number_input("Minimum value", min_value=0.0)
    # Saisr la valeur maximale
    max_density = st.number_input("Maximum value", min_value=0.0)
    btn_cd = st.button("Shearch Countries", key="cd")
    # On récupère le bouton soumis
    if btn_cd:
        if min_density < max_density:
            # On récupère les informations des pays
            df_cd = get_countries_density_between(min_density, max_density)
            # Si les pays existent
            if df_cd is not None:
                # On affiche un message de confirmation
                st.success("The data has been successfully recovered.")
                # On affiche les données récupérées
                st.dataframe(df_cd)
            else:
                # On affiche un message d'erreur
                st.error("Error when recovering data!")
        else:
            # On affiche un message d'erreur
            st.error("The minimum value must be less than the maximum value!")
    st.markdown("""---""")
    # Afficher la moyenne de la population mondiale de chaque année (1980, 2000, 2010, 2023, 2030, 2050)
    st.subheader("📝 Display the average world population for each year")
    btn_ap = st.button("Shearch Average Population")
    # On récupère le bouton soumis
    if btn_ap:
        # On récupère les informations des pays
        df_ap = get_world_pop_avg()
        # Si les pays existent
        if df_ap is not None:
            # On affiche un message de confirmation
            st.success("The data has been successfully recovered.")
            # On affiche les données récupérées
            st.dataframe(df_ap)
        else:
            # On affiche un message d'erreur
            st.error("Error when recovering data!")
    st.markdown("""---""")
    # Selection entre inférieur ou supérieur à l'aide de sidebar
    st.sidebar.subheader("📝 Selection between less than or greater than")
    # Selection entre inférieur ou supérieur
    select = st.selectbox("", ["select", "Less than", "Greater than"])
    
    if select == "select":
        st.write("Please select an option")
    
    elif select == "Less than":
        st.subheader("📝 Find number of countries with a population less than average")
        # Saisr l'année (1980, 2000, 2010, 2023, 2030, 2050)
        valid_years = [1980, 2000, 2010, 2023, 2030, 2050]
        selected_years = st.selectbox("Select years", valid_years)
        btn_popavgl = st.button("Enter", key="popavgl")
        # On récupère le bouton soumis
        if btn_popavgl:
            # On récupère les informations des pays
            popavgl = get_countries_pop_inf_avg(int(selected_years))
            # Si les pays existent
            if popavgl is not None:
                # On affiche un message de confirmation
                st.success("The data has been successfully recovered.")
                # On affiche les données récupérées
                for key, value in popavgl.items():
                    st.write(f"{key}: {value}")
            else:
                # On affiche un message d'erreur
                st.error("Error when recovering data!")
    elif select == "Greater than":
        st.subheader("📝 Find number of countries with a population greater than average")
        # Saisr l'année (1980, 2000, 2010, 2023, 2030, 2050)
        valid_years = [1980, 2000, 2010, 2023, 2030, 2050]
        selected_yearsg = st.selectbox("Select years", valid_years)
        
        btn_popavgg = st.button("Enter", key="popavgg")
        # On récupère le bouton soumis
        if btn_popavgg:
            # On récupère les informations des pays
            popavgg = get_countries_pop_sup_avg(int(selected_yearsg))
            # Si les pays existent
            if popavgg is not None:
                # On affiche un message de confirmation
                st.success("The data has been successfully recovered.")
                # On affiche les données récupérées
                for key, value in popavgg.items():
                    st.write(f"{key}=  {value}")
            else:
                # On affiche un message d'erreur
                st.error("Error when recovering data!")

# Page pour des requêtes personnalisées sur la collection MongoDB
def personalized_request():

    # Pour les requêtes personnalisées d'aggregation
    st.subheader("📝 Custom aggregation request")

    # On récupère la requête d'aggregation avec un texte en arrière plan
    query = st.text_area("", key="query_agg")

    # On récupère le bouton soumis
    btn_agg = st.button("Search_Agg")

    # On récupère les données
    if btn_agg:
        # On récupère les données
        df_ar = get_custom_aggregation(query)
        # Si les données existent
        if df_ar is not None:
            # On affiche un message de confirmation
            st.success("The data has been successfully recovered.")
            # On affiche les données récupérées
            st.dataframe(df_ar)
        else:
            # On affiche un message d'erreur
            st.error("Error when recovering data!")
    st.markdown("""---""")

    # Pour les requêtes personnalisées find
    st.subheader("📝 Custom find request")

    # On récupère la requête find
    query = st.text_area("", key="query_find")

    # On récupère le bouton soumis
    btn_find = st.button("Search_Find")

    # On récupère les données
    if btn_find:
        # On récupère les données
        df_fr = get_custom_find(query)
        # Si les données existent
        if df_fr is not None:
            # On affiche un message de confirmation
            st.success("The data has been successfully recovered.")
            # On affiche les données récupérées
            st.dataframe(df_fr)
        else:
            # On affiche un message d'erreur
            st.error("Error when recovering data!")
    st.markdown("""---""")

    # Pour les requêtes personnalisées distinct
    st.subheader("📝 Custom distinct request")

    # On récupère la requête distinct
    query = st.text_area("", key="query_distinct")

    # On récupère le bouton soumis
    btn_distinct = st.button("Search_Distinct")

    # On récupère les données
    if btn_distinct:
        # On récupère les données
        df_dr = get_custom_distinct(query)
        # Si les données existent
        if df_dr is not None:
            # On affiche un message de confirmation
            st.success("The data has been successfully recovered.")
            # On affiche les données récupérées
            st.dataframe(df_dr)
        else:
            # On affiche un message d'erreur
            st.error("Error when recovering data!")


def sidebBar():
    with st.sidebar:
        selected = option_menu(
            menu_title="Main Menu",
            options=["Home", "IUDC", "Countries and their area", "Map of the population in 2000, 2010 and 2023", "Specific Requests", "Personalized Requests"],
            icons=["house", "pencil", "globe", "map", "search", "search"],
            menu_icon="cast",
            default_index=0
        )
    return selected

def main():
    st.set_page_config(page_title="Dashboard",page_icon="🌍",layout="wide")
    st.header("🔔Analytics Dashboard of World Population Dataset EDA & MAP VISULZATION")
    st.markdown("#")

    with open("static/style/style.css") as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

    st.sidebar.image("static/image/Logo1.png", caption="Developed by Joshua Juste Emmanuel Yun Pei NIKIEMA joshuanikiema24@gmail.com")

    # Récupération des dataframes
    df_all, df_countries_pop = get_all_kinde_of_df()

    

    if "start_btn_clicked" not in st.session_state:
        # Initialiser la variable avec la valeur par défaut (False)
        st.session_state.start_btn_clicked = False

    # Vérifier si le bouton "Start" a été cliqué
    if not st.session_state.start_btn_clicked:
        start_btn = st.button("Start")
        if start_btn:
            # Une fois le bouton cliqué, on met à jour
            st.session_state.start_btn_clicked = True

    # Vérifier si le bouton "Start" a été cliqué avant d'afficher les autres parties de l'application
    if st.session_state.start_btn_clicked:
        selected = sidebBar()

        if selected == "Home":
            df_selection, cpt=Filter(df_all)
            all_Collection(df_selection, cpt)
        elif selected == "IUDC":
            insert_update_delete_country()
        elif selected == "Countries and their area":
            st.header("📊 Countries and their area")
            countries_area(df_all)
        elif selected == "Map of the population in 2000, 2010 and 2023":
            st.header("🗺️ Map of the population in 2000, 2010 and 2023")
            map_page(df_countries_pop)
        elif selected == "Specific Requests":
            st.header("🖋 Specific Requests")
            specific_request()
        elif selected == "Personalized Requests":
            st.header("🖋 Personalized Requests")
            st.markdown("""---""")
            personalized_request()


if __name__ == "__main__":
    main()