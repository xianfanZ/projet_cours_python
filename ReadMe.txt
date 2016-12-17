Nidia Hernández - Yizhe Wang - Xianfan Zhang


/data
Données de départ :

- film2011.xml : information des tournages de films à Paris entre 2002 et 2010 (source https://opendata.paris.fr).
- monuments.json : liste monuments français avec géolocalisation (source www.data.gouv.fr) 
- monuments.ods : liste monuments français avec géolocalisation (source www.data.gouv.fr)


/doc

- carnetdebord.txt : seánces de travail.
- doc.txt : documentation.
- liste_de_monuments.txt : monuments parisiens choisis pour le projet (sélection basé sur proposition de http://monumentsdeparis.net/).
- sources.txt : liste de sites consultés.


/grammaire
Grammaires de validation pour les documents xml.


/script
- enlever_sans_coord_film.py : nettoyage données des films.
- modelis_film.py : modélisation des données des films.


/transformation



/web



/xml
Données modélisés pour l'analyse de notre problématique.
- film_changed.xml : information des tournages nettoyée (élimination films sans géolocalisation).
- film_final.xml : information des tournages modélisée (données des coordonnées divisées en deux éléments différents).
