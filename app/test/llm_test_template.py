from app.services.llm_service import ask_llm

prompt = """"
Tu es un assistant spécialisé dans l’analyse de logs.

Tu vas recevoir la représentation agrégée d’un cluster de logs. Plusieurs logs ayant une structure similaire sont regroupés sous une même template afin de représenter leur forme générale.

L’objet contient :

template : la structure générale commune aux logs du cluster ;
count : le nombre exact de logs correspondant à cette template ;
first_seen : la première apparition observée dans la période analysée ;
last_seen : la dernière apparition observée dans la période analysée ;
examples : quelques logs réels appartenant à cette template ;
<*> : une partie dynamique du message identifiée par le parser. Une même position peut contenir différentes valeurs selon les occurrences du cluster.

Pour cette étape, analyse uniquement cette template, sans la comparer à d’autres templates et sans chercher à expliquer la cause de l’événement.

1. Ce que la template décrit

Explique simplement ce que le texte fixe de la template indique et quel type d’événement il décrit.

Ne donne que les informations directement supportées par le contenu de la template.

2. Compréhension des parties dynamiques

Analyse chaque <*> séparément.

Utilise les exemples pour expliquer ce que chaque position semble représenter lorsque cela peut être déterminé.

Attention :

les exemples sont seulement un échantillon du cluster ;
une valeur observée dans les exemples ne doit pas être généralisée à toutes les occurrences ;
si une même valeur apparaît dans plusieurs exemples, indique simplement qu’elle apparaît dans les exemples fournis ;
le fait qu’une position soit représentée par <*> signifie qu’elle est dynamique dans le cluster, mais ne signifie pas que les valeurs doivent être différentes dans les exemples.
3. Ce que les exemples permettent de comprendre

Explique uniquement ce que les exemples montrent réellement.

Distingue les éléments communs aux exemples des éléments qui varient.

Ne déduis pas d’informations sur les autres occurrences du cluster à partir de ces seuls exemples.

4. Ce que les statistiques indiquent

Explique uniquement les informations quantitatives directement disponibles :

le nombre d’occurrences ;
la première apparition ;
la dernière apparition ;
la durée entre first_seen et last_seen si elle est calculable.

Tu peux également calculer une fréquence moyenne si elle est directement dérivable de ces valeurs.

Cependant, tu ne dois donner aucune qualification subjective ou comparative aux statistiques.

Ne dis pas qu’une valeur est :

élevée ;
faible ;
importante ;
insignifiante ;
courte ;
longue ;
intense ;
fréquente ;
rare ;
anormale ;
inhabituelle.

sauf si une référence explicite permettant cette comparaison est fournie dans les données.

Par exemple :

✅ « La template apparaît 1280 fois sur une période d’environ 6 heures. »

✅ « La fréquence moyenne calculée est d’environ 3,56 occurrences par minute. »

❌ « 1280 occurrences représentent une fréquence élevée. »

❌ « Six heures constituent une courte période. »

Sans référence, décris uniquement les valeurs.

De même, first_seen et last_seen décrivent uniquement les limites observées dans la période analysée. Ils ne permettent pas de conclure que l’événement n’existait pas avant ou après cette période.

5. Ce qui reste indéterminé

Indique les informations qui ne peuvent pas être déterminées à partir de la template, des exemples et des statistiques fournis.

Ne propose pas encore d’explication sur :

la cause de l’événement ;
une attaque éventuelle ;
un comportement malveillant ;
un problème de configuration ;
l’intention de l’utilisateur ;
une causalité avec un autre événement ;
l’importance ou la gravité réelle du phénomène.

Ces questions seront étudiées à un niveau d’analyse supérieur.

Règles importantes

Ne modifie aucune valeur fournie.

Ne généralise pas les exemples à l’ensemble du cluster.

Ne transforme pas une observation en conclusion sans preuve.

Ne transforme pas une statistique en jugement qualitatif sans référence.

Ne présente pas d’hypothèse ou de possibilité qui n’est pas nécessaire à la compréhension de la template.

Si une information ne peut pas être déterminée, indique-le clairement.

Format de réponse

N’utilise aucun tableau Markdown.

Présente uniquement des paragraphes avec des titres simples :

1. Compréhension de la template
2. Parties dynamiques
3. Ce que montrent les exemples
4. Informations statistiques
5. Informations indéterminées

L’objectif de cette étape est uniquement de vérifier si tu peux comprendre correctement une template et utiliser ses statistiques pour la décrire sans surinterprétation.

Voici la template à analyser :
{
    'template': 'system,error,critical <*> login failure for user <*> from <*> via <*>',
    'count': 1280,
    'first_seen': datetime.datetime(2026, 8, 9, 18, 0, 17, 520000),
    'last_seen': datetime.datetime(2026, 8, 9, 23, 59, 9, 992000),
    'examples': [
        'system,error,critical system: login failure for user admin from 51.75.91.45 via winbox',
        'system,error,critical system: login failure for user admin from 51.75.91.45 via winbox',
        'system,error,critical error: login failure for user admin from 51.75.91.45 via winbox'
    ]
}
            """

answer = ask_llm(prompt)

print(answer) 