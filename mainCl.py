import requests
import json
import os
import sys

# Configuration de l'URL du serveur TABIBI
# Port 5000 par défaut pour Flask
SERVER_URL = "http://localhost:5000/extract"

def run_tabibi_analysis(file_path):
    """
    Fonction principale pour envoyer une fiche de soins au serveur
    et récupérer les données structurées.
    """
    
    # 1. Vérification du fichier local
    if not os.path.exists(file_path):
        print(f"ERREUR : Le fichier '{file_path}' est introuvable.")
        return

    # 2. Définition du Prompt Client (Instruction spécifique pour TABIBI)
    # On demande explicitement au LLM d'extraire les soins dentaires
    client_prompt = """
    Tu es l'assistant IA de TABIBI. Analyse cette fiche de soins dentaires.
    Extrais les informations suivantes en JSON :
    - patient_name : Le nom du patient.
    - date : La date de la visite.
    - treatments : Une liste d'objets contenant {act, tooth, price}.
    - total : Le montant total de la fiche.

    Réponds uniquement par un objet JSON valide.
    """

    print(f"\n--- 🦷 TABIBI AI : Analyse en cours ---")
    print(f"Fichier : {file_path}")

    try:
        # 3. Ouverture et envoi du fichier
        with open(file_path, "rb") as f:
            files = {"file": (os.path.basename(file_path), f)}
            data = {"prpt": client_prompt}

            # On utilise un timeout long (180s) car l'OCR + Llama 3 prend du temps sur PC
            response = requests.post(SERVER_URL, files=files, data=data, timeout=600)

        # 4. Traitement de la réponse du serveur
        if response.status_code == 200:
            result = response.json()
            
            print("\n ANALYSE RÉUSSIE")
            print("="*40)
            print(f" Patient : {result.get('patient_name', 'Inconnu')}")
            print(f" Date    : {result.get('date', 'Inconnue')}")
            print("-"*40)
            print(f"{'ACTE DENTAIRE':<25} | {'DENT':<5} | {'PRIX':<10}")
            print("-"*40)
            
            for t in result.get("treatments", []):
                act = t.get("act", "N/A")
                tooth = t.get("tooth", "-")
                price = t.get("price", "0")
                print(f"{str(act):<25} | {str(tooth):<5} | {str(price):<10}")
            
            print("-"*40)
            print(f" TOTAL : {result.get('total', 0.0)} TND/EUR")
            print("="*40)

        else:
            print(f"\n ERREUR SERVEUR ({response.status_code})")
            print(f"Détails : {response.text}")

    except requests.exceptions.Timeout:
        print("\n ERREUR : Le serveur a mis trop de temps à répondre (Timeout).")
    except requests.exceptions.ConnectionError:
        print("\n ERREUR : Impossible de se connecter au serveur. Lancez 'app.py' d'abord.")
    except Exception as e:
        print(f"\n ERREUR INATTENDUE : {str(e)}")

if __name__ == "__main__":
    # --- CONFIGURATION DU TEST ---
    # Remplace par le nom de ton fichier actuel (PDF ou JPG)
    fichier_a_traiter = "temp_facture3.pdf" 
    
    # Lancement de l'analyse
    run_tabibi_analysis(fichier_a_traiter)