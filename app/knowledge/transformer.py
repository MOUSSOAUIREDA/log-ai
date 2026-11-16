
from .loader import load_knowledge_file , get_knowledge_files
def knowledge_to_text(knowledge: dict) -> str:

    text = ""

    text += f"Title: {knowledge.get('title', '')}\n\n"

    text += f"Vendor: {knowledge.get('vendor', '')}\n"
    text += f"Topic: {knowledge.get('topic', '')}\n"
    text += f"Component: {knowledge.get('component', '')}\n\n"

    text += f"Error:\n{knowledge.get('error', '')}\n\n"

    text += f"Meaning:\n{knowledge.get('meaning', '')}\n\n"

    text += "Possible causes:\n"
    for cause in knowledge.get("possible_causes", []):
        text += f"- {cause}\n"

    text += "\nSymptoms:\n"
    for symptom in knowledge.get("symptoms", []):
        text += f"- {symptom}\n"

    text += "\nSolutions:\n"
    for solution in knowledge.get("solutions", []):
        text += f"- {solution}\n"

    text += "\nVerification:\n"
    for verification in knowledge.get("verification", []):
        text += f"- {verification}\n"

    text += "\nKeywords:\n"
    text += ", ".join(knowledge.get("keywords", []))

    return text.strip()

