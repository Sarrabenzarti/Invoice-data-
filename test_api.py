import requests # Importe la bibliothèque pour faire des requêtes HTTP
import os       # Importe le module pour interagir avec le système d'exploitation
import json     # Importe le module JSON pour traiter la réponse du serveur

# --- Configuration de la requête ---
# NOTE : Vérifiez que le port (5000 ou 8080) correspond à celui configuré dans votre serveur
url = "http://localhost:5000/extract" 

# Chemin vers votre PDF de test
pdf_file_path = "temp_facture3.pdf"

# --- Vérification de l'existence du fichier PDF ---
if not os.path.exists(pdf_file_path):
    print(f"Erreur : Le fichier PDF n'a pas été trouvé : {pdf_file_path}")
else:
    print(f"INFO: Fichier PDF trouvé : {pdf_file_path}")

    try:
        # --- Ouverture du fichier en mode binaire ---
        with open(pdf_file_path, 'rb') as f:
            # Préparation des fichiers
            files = {
                'file': (os.path.basename(pdf_file_path), f, 'application/pdf')
            }
            
            # Préparation des données textuelles (le prompt attendu par request.form.get("prpt"))
            data = {
                'prpt': "Extraire les informations du dossier dentaire sous forme de JSON."
            }

            # --- Envoi de la requête POST ---
            print(f"INFO: Envoi de la requête POST à {url}...")
            # Note : on passe 'files' pour le PDF et 'data' pour le prompt textuel
            response = requests.post(url, files=files, data=data)

        # --- Traitement de la réponse ---
        print(f"INFO: Réponse reçue. Code HTTP : {response.status_code}")

        if response.status_code == 200:
            try:
                response_json = response.json()
                print("\n--- Données extraites avec succès ---")
                print(json.dumps(response_json, indent=2, ensure_ascii=False))
            except json.JSONDecodeError:
                print("Erreur : Réponse JSON invalide.")
                print(response.text)
        else:
            print(f"Erreur Serveur ({response.status_code}) :")
            print(response.text)

    except requests.exceptions.ConnectionError:
        print(f"ERREUR : Impossible de se connecter au serveur sur {url}. Est-il lancé ?")
    except Exception as e:
        print(f"ERREUR INATTENDUE : {e}")
        import traceback # Pour afficher le détail de l'erreur Python
        traceback.print_exc()