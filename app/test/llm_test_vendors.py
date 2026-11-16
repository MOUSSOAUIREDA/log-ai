from app.services.llm_service import ask_llm

prompt = """"
## Format et organisation du résultat

Voici l'objet `result` à analyser :

result = {
    "MikroTik": {
        "authentication": {
            "critical": [
                {
                    "template": "system,error,critical <*> login failure for user <*> from <*> via <*>",
                    "count": 1280,
                    "first_seen": "2026-08-09 18:00:17.520000",
                    "last_seen": "2026-08-09 23:59:09.992000",
                    "examples": [
                        "system,error,critical system: login failure for user admin from 51.75.91.45 via winbox",
                        "system,error,critical error: login failure for user admin from 51.75.91.45 via winbox",
                        "system,error,critical system: login failure for user guest from 103.137.179.158 via winbox"
                    ]
                },
                {
                    "template": "system,error,critical <*> login failure for user from <*> via web",
                    "count": 78,
                    "first_seen": "2026-08-09 22:29:06.690000",
                    "last_seen": "2026-08-09 23:09:18.566000",
                    "examples": [
                        "system,error,critical system: login failure for user from 154.50.24.240 via web",
                        "system,error,critical error: login failure for user from 213.77.99.140 via web",
                        "system,error,critical error: login failure for user from 103.137.179.158 via web"
                    ]
                }
            ],
            "warning": [
                {
                    "template": "system,warning <*> user <*> logged in successfully from <*> via <*>",
                    "count": 42,
                    "first_seen": "2026-08-09 19:12:03.120000",
                    "last_seen": "2026-08-09 23:42:18.450000",
                    "examples": [
                        "system,warning user admin logged in successfully from 192.168.1.10 via winbox",
                        "system,warning user operator logged in successfully from 192.168.1.15 via web",
                        "system,warning user admin logged in successfully from 192.168.1.10 via winbox"
                    ]
                }
            ]
        },
        "network": {
            "warning": [
                {
                    "template": "system,warning interface <*> link down",
                    "count": 35,
                    "first_seen": "2026-08-09 20:15:12.100000",
                    "last_seen": "2026-08-09 22:48:31.900000",
                    "examples": [
                        "system,warning interface ether1 link down",
                        "system,warning interface ether2 link down",
                        "system,warning interface ether1 link down"
                    ]
                },
                {
                    "template": "system,warning interface <*> link up",
                    "count": 31,
                    "first_seen": "2026-08-09 20:16:04.300000",
                    "last_seen": "2026-08-09 22:49:02.200000",
                    "examples": [
                        "system,warning interface ether1 link up",
                        "system,warning interface ether2 link up",
                        "system,warning interface ether1 link up"
                    ]
                }
            ]
        }
    },

    "Cisco": {
        "authentication": {
            "critical": [
                {
                    "template": "SECURITY-4-LOGIN_FAILED: Login failed for user <*> from <*>",
                    "count": 420,
                    "first_seen": "2026-08-09 21:10:11.200000",
                    "last_seen": "2026-08-09 23:55:42.700000",
                    "examples": [
                        "SECURITY-4-LOGIN_FAILED: Login failed for user admin from 45.22.18.10",
                        "SECURITY-4-LOGIN_FAILED: Login failed for user admin from 45.22.18.10",
                        "SECURITY-4-LOGIN_FAILED: Login failed for user operator from 91.44.12.21"
                    ]
                }
            ],
            "warning": [
                {
                    "template": "SECURITY-5-LOGIN_SUCCESS: User <*> logged in from <*>",
                    "count": 67,
                    "first_seen": "2026-08-09 21:20:12.400000",
                    "last_seen": "2026-08-09 23:50:18.900000",
                    "examples": [
                        "SECURITY-5-LOGIN_SUCCESS: User admin logged in from 192.168.10.5",
                        "SECURITY-5-LOGIN_SUCCESS: User operator logged in from 192.168.10.8",
                        "SECURITY-5-LOGIN_SUCCESS: User admin logged in from 192.168.10.5"
                    ]
                }
            ]
        },
        "network": {
            "critical": [
                {
                    "template": "LINK-3-UPDOWN: Interface <*> changed state to down",
                    "count": 15,
                    "first_seen": "2026-08-09 20:30:05.100000",
                    "last_seen": "2026-08-09 21:45:22.800000",
                    "examples": [
                        "LINK-3-UPDOWN: Interface GigabitEthernet0/1 changed state to down",
                        "LINK-3-UPDOWN: Interface GigabitEthernet0/2 changed state to down",
                        "LINK-3-UPDOWN: Interface GigabitEthernet0/1 changed state to down"
                    ]
                }
            ]
        }
    }
}

Structure de l'objet fourni

L'objet que tu reçois est un dictionnaire Python représentant une analyse hiérarchique de logs.

La structure suit toujours la hiérarchie suivante :

Vendor → Topic → Level → Clusters de logs

Le niveau le plus haut est un dictionnaire dont les clés représentent les Vendors.

Pour chaque Vendor, la valeur associée est un dictionnaire contenant les Topics de ce Vendor.

Pour chaque Topic, la clé représente le nom du Topic et sa valeur est un dictionnaire contenant les différents Levels observés dans ce Topic.

Pour chaque Level, la clé représente le nom du Level et sa valeur est une liste de dictionnaires.

Chaque dictionnaire de cette liste représente un cluster de logs, c'est-à-dire un ensemble de logs ayant une même forme générale extraite par le processus de parsing.

Chaque cluster contient les informations suivantes :

template : la forme générale commune aux logs du cluster. Les parties variables d'un log sont représentées par <*>.
count : le nombre de logs appartenant à ce cluster.
first_seen : la date et l'heure de la première occurrence observée pour ce cluster.
last_seen : la date et l'heure de la dernière occurrence observée pour ce cluster.
examples : quelques occurrences réelles du cluster. Les exemples sont sélectionnés chronologiquement parmi les occurrences, afin de représenter différentes positions dans la période d'observation, notamment le début, le milieu et la fin.

Les examples servent principalement à aider à comprendre la structure et les parties variables de la template. Ils ne représentent pas nécessairement l'ensemble des valeurs présentes dans les logs du cluster.

La hiérarchie doit toujours être respectée :

Vendor contient plusieurs Topics.

Topic contient plusieurs Levels.

Level contient plusieurs clusters.

Cluster contient une template, un count, un first_seen, un last_seen et des examples.

Lorsque tu analyses l'objet, ne confonds jamais ces différents niveaux de la hiérarchie.

Les valeurs de first_seen et last_seen du cluster constituent les références temporelles officielles pour l'analyse. Les dates éventuellement visibles à l'intérieur des exemples de logs ne doivent pas être utilisées à la place de ces métadonnées temporelles officielles.

Analyse cet objet en respectant **progressivement la hiérarchie suivante** :

**Template → ensemble des templates d'un Level → Level → ensemble des Levels d'un Topic → Topic → ensemble des Topics d'un Vendor → Vendor → ensemble des Vendors.**

L'objectif n'est pas de produire uniquement une description de chaque élément, mais de montrer **comment les informations deviennent plus générales à chaque niveau de la hiérarchie**.

### 1. Analyse de chaque Template

Pour chaque template, commence par expliquer :

* ce que décrit la partie fixe de la template ;
* quel est l'événement représenté ;
* ce que représentent les différentes variables `<*>` lorsque leur signification peut être déterminée à partir des données ;
* ce que les exemples permettent de confirmer ;
* ce qui reste incertain ou impossible à déterminer.

Utilise également les statistiques associées à la template :

* `count` représente le nombre de logs correspondant à cette template ;
* `first_seen` représente officiellement la première apparition de cette template ;
* `last_seen` représente officiellement la dernière apparition de cette template.

Utilise `first_seen` et `last_seen` pour caractériser la période d'apparition de l'événement. Ne qualifie pas une durée de « courte », « longue », « importante », etc. sans disposer d'une référence permettant de justifier cette qualification.

Ne considère jamais une hypothèse comme un fait. Distingue clairement :

* ce qui est directement observable ;
* ce qui peut être raisonnablement déduit ;
* ce qui reste hypothétique ou impossible à déterminer.

### 2. Analyse de l'ensemble des Templates d'un Level

Après avoir analysé individuellement les templates, analyse-les ensemble.

Cherche notamment :

* les événements communs ;
* les différences entre les templates ;
* les variations dans les événements, les utilisateurs, les sources, les méthodes ou autres éléments lorsqu'elles sont réellement présentes dans les données ;
* les éventuels regroupements ou relations entre les templates ;
* les périodes d'apparition à partir de `first_seen` et `last_seen` ;
* les éléments remarquables qui ressortent de leur comparaison.

Ne crée pas de relation entre deux templates simplement parce qu'elles apparaissent dans le même Level ou à des périodes qui se chevauchent.

Une relation ou une comparaison doit être fondée uniquement sur les informations réellement présentes dans les données.

### 3. Analyse du Level

À partir de l'ensemble des templates qui appartiennent au Level, explique :

* quelle catégorie générale d'événements ce Level semble regrouper ;
* quels sont les principaux types d'événements observés ;
* quelles différences importantes existent entre ces événements ;
* quelles tendances peuvent être observées à partir des données disponibles ;
* quelles informations restent impossibles à déterminer.

L'analyse du Level doit être construite à partir de l'analyse des templates et non à partir d'une interprétation indépendante qui ignorerait celles-ci.

### 4. Analyse de l'ensemble des Levels d'un Topic

Une fois chaque Level analysé, compare les différents Levels du Topic.

Identifie :

* leurs points communs ;
* leurs différences ;
* les types d'événements associés à chaque Level ;
* les éventuels liens entre les événements observés dans différents Levels, uniquement lorsqu'ils sont supportés par les données ;
* les périodes d'apparition en utilisant `first_seen` et `last_seen` ;
* les caractéristiques générales du Topic qui apparaissent lorsqu'on considère ses Levels ensemble.

Ne suppose pas qu'un Level est nécessairement plus grave, plus fréquent ou plus important qu'un autre uniquement à partir de son nom. Utilise les informations réellement présentes dans l'objet.

### 5. Analyse du Topic

À partir de l'ensemble de ses Levels, détermine ce que le Topic représente globalement.

Explique :

* les principaux types d'événements observés ;
* les caractéristiques communes aux différents Levels ;
* les différences entre les catégories d'événements ;
* les tendances ou comportements remarquables que les données permettent réellement d'identifier ;
* les limites de l'analyse.

L'analyse du Topic doit être une généralisation des analyses des Levels, et non une simple répétition de leurs descriptions.

### 6. Analyse de l'ensemble des Topics d'un Vendor

Après avoir analysé chaque Topic, compare-les entre eux.

Cherche notamment :

* les domaines ou types d'événements représentés par les différents Topics ;
* les différences et similitudes entre les Topics ;
* les éventuelles relations entre certains événements appartenant à des Topics différents, uniquement lorsqu'elles sont démontrables à partir des données ;
* les périodes d'activité observées ;
* les caractéristiques générales qui émergent lorsque les Topics sont considérés ensemble.

Ne déduis pas une relation causale entre deux Topics uniquement parce que leurs événements apparaissent pendant des périodes similaires.

### 7. Analyse du Vendor

À partir de l'ensemble de ses Topics, donne une vision globale du Vendor.

Explique :

* quels types d'événements sont principalement observés ;
* quels comportements ou caractéristiques ressortent de l'ensemble des Topics ;
* quelles catégories d'événements semblent particulièrement représentées, sans utiliser de jugement subjectif ou de référence externe non fournie ;
* quelles observations peuvent être faites sur les périodes d'activité ;
* quelles informations restent inconnues.

Cette analyse doit être une synthèse construite progressivement à partir des Topics, des Levels et des Templates.

### 8. Analyse de l'ensemble des Vendors

Enfin, lorsque plusieurs Vendors sont présents dans `result`, compare-les ensemble.

Analyse :

* les caractéristiques communes ;
* les différences entre les Vendors ;
* les types d'événements observés chez chacun ;
* les éventuels événements ou comportements communs ;
* les différences de périodes d'apparition lorsqu'elles sont présentes dans les données ;
* les éventuelles relations entre Vendors, uniquement lorsqu'elles sont supportées par les données.

Ne considère jamais que deux événements appartenant à deux Vendors différents sont liés uniquement parce qu'ils sont similaires ou temporellement proches.

### Règles générales d'interprétation

Respecte toujours les règles suivantes :

1. **Ne présente jamais une hypothèse comme un fait.**
2. **N'invente aucune information absente de `result`.**
3. **Ne donne pas de signification à une variable `<*>` si les données ne permettent pas raisonnablement de l'identifier.**
4. **Utilise `count`, `first_seen` et `last_seen` comme les statistiques officielles de l'analyse.**
5. **Utilise `first_seen` et `last_seen` pour analyser les périodes d'apparition.**
6. **Ne qualifie jamais une durée, une fréquence ou un volume de « faible », « élevé », « court », « long », etc. sans référence explicite permettant de le justifier.**
7. **Ne déduis pas une attaque, une anomalie, une cause ou une relation causale uniquement à partir d'un nombre élevé d'occurrences ou d'un chevauchement temporel.**
8. **Une comparaison entre deux éléments est autorisée uniquement lorsque les informations nécessaires à cette comparaison sont présentes dans les données.**
9. **Les exemples servent à mieux comprendre la structure des templates, mais ne doivent pas être considérés comme représentatifs de toutes les occurrences lorsque cela n'est pas démontré.**
10. **À chaque niveau, distingue les observations certaines, les déductions raisonnables et les informations indéterminées.**
11. **L'analyse doit progresser du particulier vers le général : Template → Templates → Level → Levels → Topic → Topics → Vendor → Vendors.**
12. **Évite les répétitions : chaque niveau supérieur doit apporter une analyse supplémentaire et ne doit pas simplement répéter le niveau inférieur.**

Règle de portée des comparaisons : 

Les comparaisons doivent toujours respecter le niveau hiérarchique actuellement analysé.

Lors de l’analyse des templates d’un même Level, compare uniquement les templates appartenant à ce Level. Ne compare jamais une template avec une template provenant d’un autre Level, même si elles décrivent des événements similaires.

Si un Level contient une seule template, analyse cette template individuellement, puis utilise uniquement les informations déjà établies sur cette template pour décrire le Level. Il n’est pas nécessaire de chercher une comparaison avec une template appartenant à un autre Level.

La même règle s’applique aux niveaux supérieurs :

Si un Topic contient plusieurs Levels, l’analyse du Topic peut comparer ces Levels entre eux, mais uniquement à ce niveau.
Si un Topic contient un seul Level, décris le Topic à partir de ce Level sans le comparer avec des Levels appartenant à d’autres Topics.
Si un Vendor contient plusieurs Topics, l’analyse du Vendor peut comparer ses Topics entre eux, mais uniquement à ce niveau.
Si un Vendor contient un seul Topic, décris le Vendor à partir de ce Topic sans le comparer avec des Topics appartenant à d’autres Vendors.
La comparaison entre plusieurs Vendors n'est autorisée qu'au niveau de l'analyse de l'ensemble des Vendors.

Autrement dit, une information provenant d'un niveau voisin ou d'un autre élément de la hiérarchie peut être utilisée comme contexte lorsqu'elle devient pertinente à son propre niveau d'analyse, mais elle ne doit pas être utilisée prématurément pour effectuer une comparaison.

Respecte donc cette progression :

Template → templates du même Level → Level → Levels du même Topic → Topic → Topics du même Vendor → Vendor → Vendors.

À chaque étape, utilise d'abord les informations déjà établies au niveau inférieur pour construire une compréhension plus générale. Ne saute pas prématurément vers un autre élément situé au même niveau hiérarchique mais appartenant à une autre branche de l'objet.

Si un élément est unique dans son parent, il n'y a simplement aucune comparaison à effectuer à ce niveau : il faut le décrire à partir de son contenu et des informations disponibles dans ses enfants.

## Format Markdown obligatoire

Retourne directement le résultat final en Markdown.

Utilise la hiérarchie suivante :

# Analyse des logs

## Vendor : ...

### Topic : ...

#### Level : ...

##### Template : ...

Analyse de la template.

##### Template : ...

Analyse de la template.

##### Analyse des templates

Analyse collective des templates du Level.

#### Analyse du Level

Analyse globale du Level.

### Topic : ...

...

### Analyse des Topics

Analyse collective des Topics du Vendor.

## Analyse du Vendor

Analyse globale du Vendor.

## Vendor : ...

...

# Analyse globale des Vendors

Analyse comparative de l'ensemble des Vendors.

Respecte strictement cette hiérarchie de titres Markdown afin que la structure du document reflète la hiérarchie des données.

N'utilise **aucun tableau Markdown**.

Utilise uniquement des **titres, paragraphes et listes** lorsque cela améliore la lisibilité.

Retourne uniquement le contenu Markdown final, sans commentaire supplémentaire et sans balises de code autour du résultat.

"""

answer = ask_llm(prompt)

print(answer)