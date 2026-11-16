from app.services.llm_service import ask_llm

prompt = """"
Tu es un assistant spécialisé dans l’analyse technique des logs.

Tu vas recevoir un objet représentant un Vendor organisé selon la hiérarchie :

Vendor → Topics → Levels → Templates

Chaque template représente la forme générale commune à un ensemble de logs appartenant au même cluster.

Une template peut contenir :

template : la structure générale du cluster ;
count : le nombre exact d'occurrences du cluster ;
first_seen : la première apparition officielle du cluster dans l'analyse ;
last_seen : la dernière apparition officielle du cluster dans l'analyse ;
examples : quelques logs réels appartenant au cluster ;
<*> : une position dynamique dans la template.

Ton objectif est d'analyser l'ensemble du Vendor depuis les templates jusqu'au niveau Vendor, en construisant progressivement la compréhension des données.

La progression obligatoire est :

Template → Level → Topic → Vendor

1. Analyse individuelle de chaque template

Pour chaque template, détermine :

ce que le contenu fixe décrit ;
quel type d'événement elle représente ;
ce que les positions <*> semblent représenter ;
ce que les exemples permettent réellement d'observer ;
ce que count, first_seen et last_seen permettent d'observer ;
ce qui reste indéterminé.

Les exemples sont uniquement des échantillons.

Ne généralise jamais une valeur observée dans un exemple à l'ensemble des occurrences du cluster.

Le fait qu'une position soit représentée par <*> signifie qu'elle est dynamique dans le cluster. Cela ne signifie pas nécessairement que les valeurs observées dans les exemples sont différentes.

2. Analyse des templates ensemble au niveau de chaque Level

Après avoir analysé individuellement les templates, considère ensemble les templates appartenant au même Level.

Pour chaque Level, détermine :

les similitudes entre les templates ;
leurs différences ;
les types d'événements représentés ;
les relations qui peuvent raisonnablement être établies ;
les différences statistiques ;
les périodes d'apparition ;
les éventuels chevauchements temporels ;
ce que l'ensemble des templates permet de comprendre du Level.

Distingue toujours :

simple similarité ;
relation sémantique ;
coexistence temporelle ;
relation plausible ;
causalité.

Un chevauchement temporel ne prouve pas une causalité.

Des templates similaires ne prouvent pas une origine commune.

3. Analyse des différents Levels ensemble dans chaque Topic

Après avoir compris les Levels individuellement, considère les Levels appartenant au même Topic ensemble.

Pour chaque Topic, détermine :

les caractéristiques communes aux différents Levels ;
leurs différences ;
les principaux types d'activité représentés ;
les relations possibles entre les événements de différents Levels ;
les comportements temporels communs ou différents ;
les informations qui deviennent visibles uniquement lorsqu'on combine plusieurs Levels ;
ce que l'ensemble permet de comprendre du Topic.

Ne suppose pas qu'un Level est intrinsèquement plus important ou plus grave qu'un autre uniquement à partir de son nom.

Ne déduis pas de causalité entre deux Levels sans preuve.

4. Analyse des différents Topics ensemble dans le Vendor

Une fois chaque Topic compris individuellement, considère les Topics ensemble afin de comprendre le Vendor.

Analyse :

les domaines ou types d'activité représentés par les différents Topics ;
les similitudes entre les Topics ;
les différences importantes ;
les événements ou comportements communs ;
les relations possibles entre les Topics ;
les périodes temporelles communes ou distinctes ;
les caractéristiques qui apparaissent uniquement lorsqu'on considère plusieurs Topics ensemble ;
ce que l'ensemble des Topics révèle sur le Vendor.

Ne considère pas deux Topics comme liés simplement parce qu'ils appartiennent au même Vendor.

Une coexistence temporelle ne suffit pas à établir une relation causale.

5. Analyse globale du Vendor

Après avoir analysé les templates, les Levels et les Topics, construis une compréhension globale du Vendor.

Explique :

quels types d'activités sont représentés ;
quels événements dominent la représentation ;
quelles caractéristiques sont communes à plusieurs Topics ;
quelles différences importantes existent entre les domaines d'activité ;
quelles relations peuvent être raisonnablement établies ;
quels comportements temporels sont observables ;
quelles informations émergent uniquement à ce niveau global ;
quelles informations restent inconnues.

Cette partie doit apporter une compréhension globale nouvelle.

Elle ne doit pas simplement recopier les analyses précédentes.

Règle temporelle

first_seen et last_seen sont les références temporelles officielles de l'analyse.

Utilise-les pour :

déterminer la période d'apparition d'un cluster ;
calculer sa durée ;
comparer les périodes entre templates ;
identifier les chevauchements temporels ;
comparer les activités entre Levels, Topics et Vendor.

Les timestamps présents à l'intérieur des examples servent uniquement à comprendre le contenu des logs.

Ils ne doivent jamais remplacer first_seen et last_seen dans l'analyse temporelle.

Règle statistique

Considère les statistiques fournies comme des faits.

Tu peux :

présenter les valeurs ;
comparer les valeurs ;
calculer des valeurs directement dérivables ;
comparer les fréquences entre éléments ;
comparer les périodes d'apparition.

Mais ne qualifie jamais une valeur de :

élevée ;
faible ;
importante ;
rare ;
fréquente ;
courte ;
longue ;
intense ;
anormale ;
inhabituelle ;

sans disposer d'une référence explicite permettant cette comparaison.

Une comparaison relative entre des valeurs fournies est autorisée.

Règle sur les exemples

Les exemples représentent seulement une partie des occurrences.

Ne transforme jamais :

valeur observée dans un exemple

en :

caractéristique de tout le cluster

et encore moins en caractéristique de tout le Level, Topic ou Vendor.

Lorsqu'une observation vient uniquement des exemples, indique clairement qu'elle provient des exemples.

Règle d'interprétation

Base l'analyse principalement sur les données fournies.

Une connaissance technique générale peut aider à comprendre un terme, mais ne doit pas être utilisée pour ajouter des informations non présentes dans les données.

Ne transforme pas automatiquement :

un terme technique en diagnostic ;
un événement en attaque ;
une activité en comportement malveillant ;
une statistique en anomalie ;
un chevauchement temporel en causalité.

Lorsque plusieurs interprétations sont possibles, indique l'incertitude.

Distinction obligatoire

À chaque niveau de l'analyse, distingue :

Observations
Informations directement présentes dans les données.

Déductions
Informations raisonnablement déductibles des observations.

Hypothèses
Interprétations possibles mais non démontrées.

Inconnus
Informations qui ne peuvent pas être déterminées.

Une hypothèse ne doit jamais être présentée comme un fait.

Format de réponse

N'utilise aucun tableau Markdown.

Présente uniquement des titres, sous-titres et paragraphes.

Structure la réponse ainsi :

1. Analyse individuelle des templates
2. Analyse des templates par Level
3. Analyse des Levels par Topic
4. Analyse des Topics dans le Vendor
5. Compréhension globale du Vendor
6. Informations indéterminées

L'objectif est de tester la capacité du modèle à construire progressivement une compréhension complète d'un Vendor à partir des données brutes, sans perdre la distinction entre observations, statistiques, déductions, hypothèses et inconnus.

Voici le Vendor à analyser :
vendor = {
    "vendor": "vps-906bc5ef",
    "topics": {
        "web": {
            "INFO": {
                "templates": [
                    {
                        "template": "<133>1 <*> vps-906bc5ef nginx - - - <*> - - <*> +0000] \"GET <*> HTTP/1.1\" <*> <*> \"-\" <*>",
                        "count": 9865,
                        "first_seen": "2026-08-15T16:09:03.385000",
                        "last_seen": "2026-08-15T23:59:58.023000",
                        "examples": [
                            "<133>1 2026-08-15T23:59:56.172865+00:00 vps-906bc5ef nginx - - - 162.19.116.201 - - [15/Aug/2026:23:59:56 +0000] \"GET / HTTP/1.1\" 404 153 \"-\" \"Uptime-Kuma/1.23.3\"",
                            "<133>1 2026-08-15T16:09:01.055422+00:00 vps-906bc5ef nginx - - - 162.19.116.201 - - [15/Aug/2026:14:55:47 +0000] \"GET / HTTP/1.1\" 404 153 \"-\" \"Uptime-Kuma/1.23.3\""
                        ]
                    }
                ]
            },

            "ERROR": {
                "templates": [
                    {
                        "template": "<133>1 <*> vps-906bc5ef nginx - - - 2026/08/15 <*> [error] 767578#767578: <*> directory index of \"/var/www/html/cloutik/public/vendor/\" is forbidden, client: <*>, server: <*>, request: \"GET /vendor/ HTTP/1.1\", host: <*>" ,
                        "count": 5,
                        "first_seen": "2026-08-15T16:09:03.385000",
                        "last_seen": "2026-08-15T16:09:03.385000",
                        "examples": [
                            "<133>1 2026-08-15T16:09:00.965238+00:00 vps-906bc5ef nginx - - - 2026/08/15 02:31:20 [error] 767578#767578: *15288901 directory index of \"/var/www/html/cloutik/public/vendor/\" is forbidden, client: 20.169.136.165, server: api.app.cloutik.asia, request: \"GET /vendor/ HTTP/1.1\", host: \"api.app.cloutik.asia\""
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
                            "<133>1 2026-08-15T21:44:25.351797+00:00 vps-906bc5ef nginx - - - 107.150.117.121 - - [15/Aug/2026:21:44:25 +0000] \"SSL_do_handshake() failed ... client: 107.150.117.121, server: 0.0.0.0:443\""
                        ]
                    }
                ]
            }
        },

        "cron": {
            "INFO": {
                "templates": [
                    {
                        "template": "<86>1 <*> vps-906bc5ef CRON <*> - - pam_unix(cron:session): session opened for user root(uid=0) by (uid=0)",
                        "count": 3272,
                        "first_seen": "2026-08-15T00:00:01.351000",
                        "last_seen": "2026-08-15T23:59:01.701000",
                        "examples": [
                            "<86>1 2026-08-15T00:00:01.274725+00:00 vps-906bc5ef CRON 3007993 - - pam_unix(cron:session): session opened for user root(uid=0) by (uid=0)",
                            "<86>1 2026-08-15T23:59:01.476811+00:00 vps-906bc5ef CRON 3866513 - - pam_unix(cron:session): session opened for user root(uid=0) by (uid=0)"
                        ]
                    }
                ]
            },

            "COMMAND": {
                "templates": [
                    {
                        "template": "<78>1 <*> vps-906bc5ef CRON <*> - - (root) CMD (cd /var/www/html/cloutik && php artisan schedule:run >> /dev/null 2>&1)",
                        "count": 1440,
                        "first_seen": "2026-08-15T00:00:01.396000",
                        "last_seen": "2026-08-15T23:59:01.701000",
                        "examples": [
                            "<78>1 2026-08-15T00:00:01.279071+00:00 vps-906bc5ef CRON 3007997 - - (root) CMD (cd /var/www/html/cloutik && php artisan schedule:run >> /dev/null 2>&1)",
                            "<78>1 2026-08-15T23:59:01.478015+00:00 vps-906bc5ef CRON 3866516 - - (root) CMD (cd /var/www/html/cloutik && php artisan schedule:run >> /dev/null 2>&1)"
                        ]
                    }
                ]
            }
        }
    }
}
"""
answer = ask_llm(prompt)

print(answer)