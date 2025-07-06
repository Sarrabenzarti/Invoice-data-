
import requests # Importe la bibliothèque pour faire des requêtes HTTP
import os       # Importe le module pour interagir avec le système d'exploitation (pour vérifier le fichier)
import json     # Importe le module JSON pour traiter la réponse du serveur

# --- Configuration de la requête ---
url = "http://localhost:8080/extract" # L'URL de votre endpoint Flask

# Assurez-vous que ce fichier PDF est dans le même répertoire que test_api.py
pdf_file_path = "temp_facture3.pdf"

# --- Vérification de l'existence du fichier PDF ---
if not os.path.exists(pdf_file_path):
    print(f"Erreur : Le fichier PDF n'a pas été trouvé à cet emplacement : {pdf_file_path}")
    print("Veuillez vous assurer que 'temp_facture3.pdf' est dans le même dossier que 'test_api.py'.")
else:
    print(f"INFO: Fichier PDF trouvé : {pdf_file_path}")

    try:
        # --- Ouverture du fichier en mode binaire pour l'envoi ---
        # 'rb' signifie "read binary" (lire en binaire)
        with open(pdf_file_path, 'rb') as f:
            # --- Préparation des fichiers à envoyer ---
            # 'files' est un dictionnaire où la clé ('file') correspond au nom du champ HTML
            # que votre Flask attend (request.files['file']).
            # La valeur est un tuple : (nom_du_fichier_client, objet_fichier_ou_contenu_binaire, type_MIME)
            files = {
                'file': (os.path.basename(pdf_file_path), f, 'application/pdf')
            }
            # os.path.basename(pdf_file_path) extrait juste le nom 'temp_facture3.pdf' du chemin complet

            # --- Préparation des autres données du formulaire (le prompt) ---
            # 'data' est un dictionnaire pour les champs de formulaire textuels

            # --- Envoi de la requête POST ---
            print(f"INFO: Envoi de la requête POST à {url}...")
            response = requests.post(url, files=files)

        # --- Traitement de la réponse du serveur ---
        print(f"INFO: Réponse reçue. Code de statut HTTP : {response.status_code}")

        if response.status_code == 200:
            # Si la réponse est un JSON valide
            try:
                response_json = response.json()
                print("Données extraites (JSON) :")
                print(json.dumps(response_json, indent=2, ensure_ascii=False)) # Affiche le JSON joliment formaté
            except json.JSONDecodeError:
                print("Erreur : La réponse n'est pas un JSON valide.")
                print("Contenu brut de la réponse :")
                print(response.text) # Affiche le texte brut si ce n'est pas du JSON
        else:
            # Si le statut n'est pas 200 (OK), affiche le contenu brut pour le débogage
            print(f"Erreur : Le serveur a retourné un statut {response.status_code}.")
            print("Contenu de la réponse pour débogage :")
            print(response.text) # Ceci montrera le HTML du 500 ou 403

    except requests.exceptions.ConnectionError as e:
        # Gère les erreurs si le script ne peut pas se connecter au serveur (ex: serveur non lancé)
        print(f"ERREUR DE CONNEXION : Impossible de se connecter au serveur à {url}.")
        print(f"Détail : {e}")
        print("Veuillez vérifier que votre serveur Flask est bien en cours d'exécution dans un autre terminal.")
    except Exception as e:
        # Gère toute autre erreur inattendue
        print(f"ERREUR INATTENDUE : {e}")
        import traceback # Pour afficher le détail de l'erreur Python
        traceback.print_exc()