import re
from PyPDF2 import PdfReader

def extract_data_from_pdf(file_storage):
    import tempfile
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
        file_storage.save(tmp.name)
        reader = PdfReader(tmp.name)
        text = "\n".join(page.extract_text() or '' for page in reader.pages)


    print("--- TEXTE EXTRAIT DU PDF ---")
    if not text or text.strip() == "":
        print("[ERREUR] Aucun texte extrait du PDF. PyPDF2 n'a rien trouvé. Vérifie que le PDF n'est pas une image scannée ou corrompue.")
    else:
        print(text)
    print("---------------------------")

    # Regex adaptées au PDF de test
    date_match = re.search(r"(\d{4}-\d{2}-\d{2})", text)
    total_match = re.search(r"Total ?[:]? ?([0-9]+[\.,][0-9]{2})", text, re.IGNORECASE)
    client_match = re.search(r"Client ?[:]? ?([\w]+)", text, re.IGNORECASE)
    num_match = re.search(r"Facture ?[:]? ?([\w\-]+)", text, re.IGNORECASE)

    return {
        "date": date_match.group(1) if date_match else None,
        "total": float(total_match.group(1).replace(",", ".")) if total_match else None,
        "client": client_match.group(1) if client_match else None,
        "num": num_match.group(1) if num_match else None
    }
