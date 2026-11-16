from app.knowledge.retreiver import search_knowledge

question = "Pourquoi un serveur Linux peut-il refuser une connexion ?"

results = search_knowledge(question)

print("Question :", question)
print("\nRésultats de la recherche :")

for i, result in enumerate(results, 1):
    print(f"\nRésultat {i}")
    print("Texte :", result["text"])
    print("Score :", result["score"])
