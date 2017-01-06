Nidia Hernández - Yizhe Wang - Xianfan Zhang


/ cartes:
- carte_monuments_tournages : visualisation localisation monuments et tous les tournages 2002-2010.
- carte_monuments_tournages_filtres : visualisation localisation monuments et tournages proches.


/data
Données de départ :
- film2011.xml : information des tournages de films à Paris entre 2002 et 2010 (source https://opendata.paris.fr).
- monuments.json : liste monuments français avec géolocalisation (source www.data.gouv.fr) 
- monuments.ods : liste monuments français avec géolocalisation (source www.data.gouv.fr)
- liste_de_monuments.txt : monuments parisiens choisis pour le projet (sélection basé sur proposition de http://monumentsdeparis.net/).


/doc
Divers :
- carnetdebord.txt : seánces de travail.
- doc.txt : documentation.
- sources.txt : liste de sites consultés.


/grammaire
Grammaires de validation pour les documents xml.


/json
- film.geojson (obsolète) : géocoordonnées des tournages de films à Paris entre 2002 et 2010 (source https://opendata.paris.fr). Abandonné pour modélisation en xml.
- monuments.geojson (obsolète) : géocoordonnées des monuments choisis. Abandonné pour monuments_coord.xml.


/script
- enlever_sans_coord_film.py : nettoyage données des films.
- filter_new.py : élimine les tournages qui ne sont proches d'aucun monument.
- geojson_film.py (obsolète) 
- get_info_film.py : obtention de plus d'informations sur les tournages qui sont à proximité des monuments
- modelis_film.py : modélisation des données des films.
- project_carte : projection des monuments et des tournages dans une carte OpenStreetMap.
- tableau_resultat.py : construction du tableau de résultats.
- traite_monuments.py : obtention et modélisation des géocoordonnées des monuments.


/web
Site web.


/xml
Données modélisés pour l'analyse de notre problématique.
- film_changed.xml : information des tournages nettoyée (élimination films sans géolocalisation).
- film_final.xml : information des tournages modélisée (données des coordonnées divisées en deux éléments différents).
- films_genre_pays.xml : ajout information supplémentaire sur les tournages (genre et pays d'origine)
- filter_coord_films.xml : tournages filtrés (élimination des films qui ne sont pas proches d'un monument).
- filter_coord_films_new.xml : ajout information du monument le plus proche. 
- monuments_coord.xml : monuments avec poids (attribut "espace") et géocoordonnées.
