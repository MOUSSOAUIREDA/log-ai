from app.services.chat_service import handle_question

question = "Pourquoi un serveur Linux peut-il refuser une connexion ?"

response = handle_question(question)

print("Question :", question)
print("\nRéponse :", response)
print("\nType :", type(response))