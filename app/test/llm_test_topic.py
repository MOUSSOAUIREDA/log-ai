from app.services.llm_service import ask_llm

prompt = """"
Tu es un assistant spécialisé dans l’analyse technique de logs.

Tu vas recevoir un objet représentant un Topic organisé selon la hiérarchie :

Topic → Levels → Templates

Chaque template représente la forme générale commune à un ensemble de logs appartenant au même cluster.

Pour chaque template, les informations disponibles peuvent inclure :

template : la structure générale commune aux logs du cluster ;
count : le nombre d'occurrences du cluster ;
first_seen : première apparition officielle du cluster dans l'analyse ;
last_seen : dernière apparition officielle du cluster dans l'analyse ;
examples : quelques logs réels appartenant au cluster ;
<*> : une position dynamique dans la template.

Ton objectif est de construire progressivement une compréhension du Topic :

Template → Templates d'un Level → Level → Levels d'un Topic → Topic

1. Analyse individuelle de chaque template

Pour chaque template, commence par déterminer :

ce que le contenu fixe décrit ;
quel type d'événement il représente ;
ce que les parties <*> semblent représenter ;
ce que les exemples permettent d'observer ;
ce que les statistiques permettent d'observer ;
ce qui reste indéterminé.

Les exemples servent uniquement à comprendre la structure et les valeurs concrètes présentes dans certains logs.

Ne généralise jamais une information provenant d'un exemple à l'ensemble du cluster, sauf si cette information est explicitement fournie comme statistique ou comme propriété agrégée.

Par exemple, si trois exemples présentent la même adresse IP, tu peux dire :

« Les exemples fournis contiennent cette adresse IP. »

Tu ne peux pas conclure :

« Le cluster concerne cette adresse IP. »

sauf si les données agrégées le permettent explicitement.

Le fait qu'une position soit représentée par <*> signifie que cette position est dynamique dans le cluster. Cela ne signifie pas nécessairement que les valeurs observées dans les exemples sont différentes.

2. Règle temporelle fondamentale

first_seen et last_seen sont les références temporelles officielles de l'analyse du cluster.

Utilise toujours first_seen et last_seen pour déterminer :

la période d'apparition du cluster ;
sa durée d'observation ;
les comparaisons temporelles avec d'autres templates ou Levels ;
les chevauchements temporels.

Les timestamps éventuellement présents à l'intérieur des examples servent uniquement à comprendre les logs eux-mêmes.

Ne remplace jamais first_seen ou last_seen par les timestamps trouvés dans les exemples pour analyser la période du cluster.

Ne considère pas que les timestamps des exemples représentent nécessairement toute la distribution temporelle du cluster.

Si les timestamps des exemples sont différents de first_seen ou last_seen, utilise quand même first_seen et last_seen comme référence officielle pour l'analyse temporelle.

3. Analyse statistique

Utilise count, first_seen et last_seen comme des faits fournis par le système d'analyse.

Tu peux :

rapporter les valeurs ;
calculer la durée entre first_seen et last_seen ;
calculer une fréquence moyenne si cela est directement dérivable ;
comparer les valeurs entre templates ou entre Levels.

Mais ne qualifie jamais une valeur de :

élevée ;
faible ;
importante ;
rare ;
fréquente ;
intense ;
courte ;
longue ;
anormale ;
inhabituelle ;

sans référence explicite permettant cette comparaison.

Par exemple :

« La template apparaît 9865 fois entre first_seen et last_seen. »

est correct.

Mais :

« 9865 occurrences représentent un volume très élevé. »

n'est pas justifié sans référence.

Une comparaison relative entre deux valeurs fournies est autorisée :

« Cette template apparaît plus souvent que cette autre template. »

4. Compréhension des templates ensemble

Après l'analyse individuelle, considère les templates appartenant au même Level ensemble.

Cherche :

les similitudes ;
les différences ;
les types d'événements communs ;
les relations sémantiques possibles ;
les chevauchements temporels selon first_seen et last_seen ;
les différences de fréquence ;
ce que l'ensemble permet de comprendre du Level.

Pour chaque relation proposée, explique sur quelles informations elle repose.

Distingue toujours :

similarité ;
relation plausible ;
coexistence temporelle ;
causalité.

Un chevauchement temporel ne prouve pas une causalité.

Deux templates similaires ne prouvent pas qu'elles proviennent de la même source, du même acteur ou du même incident.

Deux templates appartenant au même Level ne signifient pas nécessairement qu'elles sont directement liées.

5. Compréhension des Levels ensemble

Après avoir compris chaque Level à partir de ses templates, considère les différents Levels du Topic ensemble.

Analyse :

les similitudes entre les Levels ;
leurs différences ;
les types d'événements représentés ;
les relations possibles entre les événements de différents Levels ;
les chevauchements temporels selon les first_seen et last_seen officiels ;
les différences statistiques ;
ce qui devient visible uniquement lorsqu'on considère plusieurs Levels ensemble.

Ne déduis pas un ordre de gravité entre les Levels uniquement à partir de leur nom.

Ne déduis pas qu'un Level est plus important qu'un autre sans information permettant cette comparaison.

Ne déduis pas de causalité entre les Levels sans preuve.

6. Compréhension globale du Topic

Après l'analyse des templates puis des Levels, explique ce que l'ensemble permet de comprendre du Topic.

La compréhension globale doit être construite à partir des analyses précédentes.

Elle doit faire ressortir :

les principaux types d'événements ;
les caractéristiques communes ;
les différences entre les Levels ;
les relations raisonnablement établies ;
les comportements temporels observables ;
les informations qui émergent uniquement au niveau du Topic ;
les limites de ce qui peut être conclu.

Ne te contente pas de répéter les données brutes.

7. Connaissances externes et interprétation

Base prioritairement l'analyse sur les informations fournies dans l'objet.

Tu peux utiliser une connaissance technique générale pour comprendre un terme ou une technologie, mais ne transforme pas automatiquement cette connaissance en fait concernant les données observées.

Si une interprétation dépend d'une information qui n'est pas fournie, présente-la comme une possibilité ou indique qu'elle ne peut pas être déterminée.

Ne transforme pas automatiquement :

un terme technique en diagnostic ;
un code ou un mot en cause exacte ;
un événement en attaque ;
une activité réseau en comportement malveillant ;
un chevauchement temporel en relation causale.
8. Distinction obligatoire

À chaque niveau de l'analyse, distingue :

Observations
Ce qui est directement présent dans les données.

Déductions
Ce qui est raisonnablement déductible des observations.

Hypothèses
Ce qui est possible mais non démontré.

Inconnus
Ce qui ne peut pas être déterminé avec les données disponibles.

Une hypothèse ne doit jamais être présentée comme un fait.

9. Format

N'utilise aucun tableau Markdown.

Présente la réponse uniquement sous forme de titres, sous-titres et paragraphes.

Structure la réponse ainsi :

1. Analyse individuelle des templates
2. Analyse des templates ensemble par Level
3. Analyse des Levels ensemble
4. Compréhension globale du Topic
5. Informations indéterminées

L'objectif est de construire progressivement une compréhension du Topic tout en conservant une distinction stricte entre les données observées, les statistiques officielles, les déductions et les hypothèses.

Voici l'objet à analyser :

topic_analysis = {
    "topic": "web",
    "levels": {
        "INFO": {
            "templates": [
                {
                    "template": "<133>1 <*> vps-906bc5ef nginx - - - <*> - - <*> +0000] \"GET <*> HTTP/1.1\" <*> <*> \"-\" <*>",
                    "count": 9865,
                    "first_seen": "2026-08-15T16:09:03.385000",
                    "last_seen": "2026-08-15T23:59:58.023000",
                    "examples": [
                        "<133>1 2026-08-15T23:59:56.172865+00:00 vps-906bc5ef nginx - - - 162.19.116.201 - - [15/Aug/2026:23:59:56 +0000] \"GET / HTTP/1.1\" 404 153 \"-\" \"Uptime-Kuma/1.23.3\"",
                        "<133>1 2026-08-15T16:09:01.055422+00:00 vps-906bc5ef nginx - - - 162.19.116.201 - - [15/Aug/2026:14:55:47 +0000] \"GET / HTTP/1.1\" 404 153 \"-\" \"Uptime-Kuma/1.23.3\"",
                        "<133>1 2026-08-15T23:59:25.687506+00:00 vps-906bc5ef nginx - - - 162.19.116.201 - - [15/Aug/2026:23:59:25 +0000] \"GET / HTTP/1.1\" 404 153 \"-\" \"Uptime-Kuma/1.23.3\""
                    ]
                }
            ]
        },

        "ERROR": {
            "templates": [
                {
                    "template": "<133>1 <*> vps-906bc5ef nginx - - - 2026/08/15 <*> [error] 767578#767578: <*> directory index of \"/var/www/html/cloutik/public/vendor/\" is forbidden, client: <*>, server: <*>, request: \"GET /vendor/ HTTP/1.1\", host: <*>",
                    "count": 5,
                    "first_seen": "2026-08-15T16:09:03.385000",
                    "last_seen": "2026-08-15T16:09:03.385000",
                    "examples": [
                        "<133>1 2026-08-15T16:09:00.965238+00:00 vps-906bc5ef nginx - - - 2026/08/15 02:31:20 [error] 767578#767578: *15288901 directory index of \"/var/www/html/cloutik/public/vendor/\" is forbidden, client: 20.169.136.165, server: api.app.cloutik.asia, request: \"GET /vendor/ HTTP/1.1\", host: \"api.app.cloutik.asia\"",
                        "<133>1 2026-08-15T16:09:00.966615+00:00 vps-906bc5ef nginx - - - 2026/08/15 10:45:44 [error] 767578#767578: *15432692 directory index of \"/var/www/html/cloutik/public/vendor/\" is forbidden, client: 20.163.43.14, server: api-interf.app.cloutik.asia, request: \"GET /vendor/ HTTP/1.1\", host: \"api-interf.app.cloutik.asia\"",
                        "<133>1 2026-08-15T16:09:00.966701+00:00 vps-906bc5ef nginx - - - 2026/08/15 14:18:45 [error] 767578#767578: *15494884 directory index of \"/var/www/html/cloutik/public/vendor/\" is forbidden, client: 20.169.136.165, server: api.app.cloutik.asia, request: \"GET /vendor/ HTTP/1.1\", host: \"api.app.cloutik.asia\""
                    ]
                }
            ]
        },

        "CRIT": {
            "templates": [
                {
                    "template": "<133>1 <*> vps-906bc5ef nginx - - - 2026/08/15 <*> [crit] 767578#767578: <*> SSL_do_handshake() failed (SSL: error:141CF06C:SSL routines:tls_parse_ctos_key_share:bad key share) while SSL handshaking, client: <*>, server: 0.0.0.0:443",
                    "count": 5,
                    "first_seen": "2026-08-15T16:09:03.385000",
                    "last_seen": "2026-08-15T21:44:25.547000",
                    "examples": [
                        "<133>1 2026-08-15T16:09:00.965511+00:00 vps-906bc5ef nginx - - - 2026/08/15 03:03:23 [crit] 767578#767578: *15298722 SSL_do_handshake() failed (SSL: error:141CF06C:SSL routines:tls_parse_ctos_key_share:bad key share) while SSL handshaking, client: 64.62.156.182, server: 0.0.0.0:443",
                        "<133>1 2026-08-15T16:09:00.965654+00:00 vps-906bc5ef nginx - - - 2026/08/15 09:22:10 [crit] 767578#767578: *15408602 SSL_do_handshake() failed (SSL: error:141CF06C:SSL routines:tls_parse_ctos_key_share:bad key share) while SSL handshaking, client: 24.199.121.87, server: 0.0.0.0:443",
                        "<133>1 2026-08-15T21:44:25.351797+00:00 vps-906bc5ef nginx - - - 2026/08/15 21:44:25 [crit] 767578#767578: *15624544 SSL_do_handshake() failed (SSL: error:141CF06C:SSL routines:tls_parse_ctos_key_share:bad key share) while SSL handshaking, client: 107.150.117.121, server: 0.0.0.0:443"
                    ]
                }
            ]
        },

        "ALERT": {
            "templates": [
                {
                    "template": "<133>1 <*> vps-906bc5ef nginx - - - 2026/08/15 <*> [alert] 767578#767578: <*> could not allocate new session in SSL session shared cache \"le_nginx_SSL\" while SSL handshaking, client: <*>, server: 0.0.0.0:443",
                    "count": 12,
                    "first_seen": "2026-08-15T16:09:03.385000",
                    "last_seen": "2026-08-15T16:09:03.385000",
                    "examples": [
                        "<133>1 2026-08-15T16:09:00.965523+00:00 vps-906bc5ef nginx - - - 2026/08/15 04:38:50 [alert] 767578#767578: *15326407 could not allocate new session in SSL session shared cache \"le_nginx_SSL\" while SSL handshaking, client: 122.63.103.241, server: 0.0.0.0:443",
                        "<133>1 2026-08-15T16:09:00.965689+00:00 vps-906bc5ef nginx - - - 2026/08/15 09:52:16 [alert] 767578#767578: *15417370 could not allocate new session in SSL session shared cache \"le_nginx_SSL\" while SSL handshaking, client: 103.212.193.28, server: 0.0.0.0:443",
                        "<133>1 2026-08-15T16:09:00.966634+00:00 vps-906bc5ef nginx - - - 2026/08/15 11:40:11 [alert] 767578#767578: *15449091 could not allocate new session in SSL session shared cache \"le_nginx_SSL\" while SSL handshaking, client: 122.63.101.246, server: 0.0.0.0:443"
                    ]
                }
            ]
        }
    }
}
"""

answer = ask_llm(prompt)

print(answer)