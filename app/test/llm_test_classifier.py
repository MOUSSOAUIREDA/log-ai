from app.services.chat_service import classify_question

questions = [
    "Que signifie cette template : DHCP lease renewed for client <IP> ?",
    "Les utilisateurs n’arrivent plus à accéder au serveur depuis le réseau interne. Qu’est-ce qui pourrait expliquer cette situation ?",
    "Quelles actions peut-on entreprendre lorsqu’un serveur Linux refuse les connexions sur un service ?",
    "Quelle est la différence entre le routage statique et le routage dynamique dans un réseau IP ?",
    "Quelle est la capitale de l’Australie ?"
]

for i, question in enumerate(questions, 1):
    result = classify_question(question)

    print(f"\nQuestion {i} : {question}")
    print(f"Catégorie : {result}")