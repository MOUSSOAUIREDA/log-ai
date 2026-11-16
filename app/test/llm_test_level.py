from app.services.llm_service import ask_llm

prompt = """"
Tu es un assistant spécialisé dans l’analyse technique des logs.

Tu vas recevoir plusieurs clusters de logs appartenant au même Level.

Chaque cluster est représenté par :

template : la forme générale des logs du cluster ;
count : le nombre exact de logs correspondant à cette template ;
first_seen : la première apparition observée dans la période analysée ;
last_seen : la dernière apparition observée dans la période analysée ;
examples : quelques logs réels appartenant à cette template ;
<*> : une position dynamique identifiée par le système de parsing.

Ton objectif est de comprendre ce que les différentes templates permettent de comprendre lorsqu’elles sont considérées ensemble, tout en restant strictement limité aux informations fournies.

1. Compréhension de chaque template

Commence par expliquer brièvement ce que décrit chaque template.

Ne généralise pas les valeurs présentes dans les exemples à toutes les occurrences.

Pour une position <*>, distingue toujours :

le fait qu'elle est dynamique dans la template ;
les valeurs effectivement observées dans les exemples.

Le fait qu'une position soit dynamique ne signifie pas que les valeurs observées dans les exemples doivent être différentes.

2. Comparaison des templates

Compare ensuite les templates entre elles.

Identifie uniquement les éléments que les données permettent réellement de comparer :

structure similaire ou différente ;
type d'événement similaire ou différent ;
champs fixes ou dynamiques communs ;
valeurs observées dans les exemples ;
différences dans les statistiques ;
chevauchements ou différences temporelles.

Ne déduis pas que deux templates proviennent du même composant uniquement parce qu'elles partagent une partie de leur texte.

Formule plutôt cela comme une similarité observée lorsque l'origine exacte ne peut pas être établie.

3. Relations entre les templates

Cherche les relations possibles entre les templates, mais distingue clairement les niveaux de preuve.

Tu peux identifier :

une similarité structurelle lorsqu'elles possèdent une structure comparable ;
une similarité sémantique lorsqu'elles décrivent des événements de même nature ;
une coexistence temporelle lorsque leurs périodes d'apparition se chevauchent ;
une relation possible lorsque plusieurs éléments indépendants la rendent plausible.

Ne transforme jamais ces observations en causalité.

Un chevauchement temporel ne signifie pas qu'un événement a provoqué l'autre.

Deux templates partageant <*> ne signifient pas que les valeurs dynamiques sont identiques.

Deux templates similaires ne signifient pas nécessairement qu'elles proviennent du même composant, de la même source ou du même incident.

N'affirme pas qu'elles appartiennent à une même attaque, campagne, session ou activité sans éléments permettant de l'établir.

4. Comparaison statistique

Tu peux comparer directement les statistiques fournies entre les templates.

Par exemple :

« La première template apparaît 1280 fois et la seconde 78 fois. »

Tu peux également comparer leurs fenêtres temporelles.

Cependant, ne qualifie jamais une valeur de :

élevée ;
faible ;
importante ;
courte ;
longue ;
intense ;
fréquente ;
rare ;
anormale ;

sans référence explicite.

Une comparaison entre les templates est autorisée lorsque les deux valeurs sont présentes dans les données.

Par exemple :

✅ « La première template apparaît davantage que la seconde. »

Mais :

❌ « 1280 occurrences représentent un volume élevé. »

5. Compréhension globale du level

Après avoir analysé les templates individuellement et leurs relations, explique ce que l'ensemble permet de comprendre du Level.

La synthèse doit répondre à :

Quels types d'événements sont présents ?
Quelles similarités existent entre eux ?
Quelles différences sont importantes ?
Quelles relations peuvent être raisonnablement proposées ?
Quelles relations restent impossibles à établir ?
Que montrent les informations temporelles ?
Que peut-on réellement comprendre du niveau considéré ?
6. Distinction obligatoire

Dans ta réponse, distingue clairement :

Observations
Ce qui est directement présent dans les données.

Déductions
Ce qui peut raisonnablement être déduit des observations.

Hypothèses
Ce qui est possible mais non démontré.

Inconnus
Ce qui ne peut pas être déterminé avec les données disponibles.

Une hypothèse ne doit jamais être présentée comme une déduction.

Contraintes

Ne produis aucun tableau Markdown.

N'invente aucune information.

Ne généralise pas les exemples à toutes les occurrences.

Ne modifie aucune statistique.

Ne déduis pas de causalité à partir d'un simple chevauchement temporel.

Ne déduis pas une origine commune à partir d'une similarité textuelle seule.

Ne déduis pas une activité malveillante à partir du nombre d'occurrences seul.

Ne propose pas de scénario d'attaque, de campagne ou de problème de configuration sauf si les données fournies contiennent des éléments permettant raisonnablement de le soutenir.

Présente la réponse avec des paragraphes et des titres simples.

L'objectif est de tester ta capacité à passer de l'analyse individuelle des templates à leur compréhension collective, sans transformer les possibilités en faits.

Voici les templates à analyser :
result = {
    "level": "alert",
    "templates": [
        {
            "template": "system,error,critical <*> login failure for user <*> from <*> via <*>",
            "count": 1280,
            "first_seen": "2026-08-09T18:00:17.520000",
            "last_seen": "2026-08-09T23:59:09.992000",
            "examples": [
                "system,error,critical system: login failure for user admin from 51.75.91.45 via winbox",
                "system,error,critical system: login failure for user admin from 51.75.91.45 via winbox",
                "system,error,critical error: login failure for user admin from 51.75.91.45 via winbox"
            ]
        },
        {
            "template": "system,error,critical <*> login failure for user from <*> via web",
            "count": 78,
            "first_seen": "2026-08-09T22:29:06.690000",
            "last_seen": "2026-08-09T23:09:18.566000",
            "examples": [
                "system,error,critical system: login failure for user  from 154.50.24.240 via web",
                "system,error,critical error: login failure for user  from 213.77.99.140 via web",
                "system,error,critical error: login failure for user  from 103.137.179.158 via web"
            ]
        }
    ]
}
"""
answer = ask_llm(prompt)
print(answer)