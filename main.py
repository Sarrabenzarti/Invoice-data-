from flask import Flask, request, jsonify
from waitress import serve
import pdfplumber
import json
import re
import torch
from langdetect import detect
import pdf2Image
from collections import Counter

from transformers import AutoTokenizer
import traceback
#model_name = "mistralai/Mistral-7B-Instruct-v0.2"
#model_name = "lahirum/Llama-3.2-3B-Instruct-Q4_0-GGUF"
#tokenizer = AutoTokenizer.from_pretrained(model_name)
#model = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype=torch.float16, device_map="auto")
#text_generator = pipeline("text-generation", model=model_name)
from llama_cpp import Llama
import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
llm = None # Initialiser llm à None au cas où le chargement échoue
try:
    print("INFO: Tentative de chargement du modèle Llama...") # <-- Here

    llm = Llama(model_path="models/llama-3-8b-Instruct.Q4_K_M.gguf", tn_cx=8192,n_gpu_layers=-1)
    print("SUCCESS: Modèle Llama chargé avec succès !") # <-- Here
    print(f"DEBUG: Taille réelle de la fenêtre de contexte LLM (n_ctx()): {llm.n_ctx()} tokens")
except Exception as e:
    print(f"CRITICAL ERROR: Impossible de charger le modèle Llama (fichier GGUF).") # <-- Here
    print(f"Détails de l'erreur: {e}")
    exit(1)
# l modifaction

from langchain.text_splitter import RecursiveCharacterTextSplitter
from transformers import AutoTokenizer

# Generate text




app = Flask(__name__)

# l modification (better solution)

def split_text_into_chunks_langchain(text: str, chunk_size_tokens: int, chunk_overlap_tokens: int):
    print(f"DEBUG: Entrée dans split_text_into_chunks_langchain avec une longueur de texte de {len(text)}.")  # <-- Here
    if not text or chunk_size_tokens <= 0 or chunk_overlap_tokens < 0 or chunk_overlap_tokens >= chunk_size_tokens:
        print("Erreur: Paramètres d'entrée invalides.")
        return []

    #tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-3.2-3B-Instruct")
    if llm is None:  # Ajoutez cette vérification au cas où le modèle Llama n'ait pas chargé
        print("WARNING: LLM model (llm) not loaded, using character length for token count fallback.")
        length_function = lambda txt: len(txt.encode('utf-8'))  # Fallback simple
    else:
        # LlamaCpp's tokenize attend un texte encodé en bytes (utf-8)
        length_function = lambda txt: len(llm.tokenize(txt.encode('utf-8')))
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size_tokens,
        chunk_overlap=chunk_overlap_tokens,
        length_function=length_function,
        separators=["\n\n", "\n", " ", ""],
    )
    print("DEBUG: Utilisation du tokenizer LLM pour le découpage du texte en tokens.")

    chunks = text_splitter.split_text(text)
    print(f"DEBUG: Texte découpé en {len(chunks)} chunks.")  # <-- Here

    return chunks

# tnsch l initialiasation mt3 hunk_size_tokens, chunk_overlap_tokens  w l appel mt3 l fonction hthi


#les deux modules hethom zydin houma des solutions mch bhin kima awelin 3thmli bdlyhom b split text into chunks 


def adjust_text_length(text, max_length):
    """
    Ajuste la longueur du texte en supprimant des caractères du milieu
    pour qu'il corresponde exactement à `max_length`.
    """
    current_length = len(text)
    
    # Vérifier si une réduction est nécessaire
    if current_length <= max_length:
        return text  # Pas besoin de modification


    
    # Calcul de la réduction nécessaire
    excess_length = current_length - max_length
    middle_index = len(text) // 2
    
    # Supprimer des caractères du milieu
    adjusted_text = text[:middle_index - excess_length // 2] + text[middle_index + excess_length // 2:]
    
    return adjusted_text

# hthi une solution kn jet l facture fiha barcha donnes llama mtnjmch traite ces donnes la donc l7al lw7id eni n9s des informations ml wst 5tr dima les donnes l mouhmin ybdew mloul w ml5r




def get_text_segments(text, num_chars=300):
    """Extracts the first and last 'num_chars' from the text."""
    first_part = text[:num_chars]  # First 100 characters
    last_part = text[-num_chars:]  # Last 100 characters

    return first_part + last_part

# hthi solution o5ra textracti awl w e5r text w trj3hom



#import re
def clean_text(text):
    """Removes extra spaces and blank lines."""
    cleaned_text = re.sub(r'\s+', ' ', text).strip()
    #\s hiya kol espace kol  fara8 fi text
    #.strip() tn7i les espaces eli mloul w mle5r mt3 text
    return cleaned_text


#\s : Ce caractère spécial représente n'importe quel caractère d'espace blanc. Cela inclut :
#l'espace normal ()
#la tabulation (\t)
#le saut de ligne (\n)
#le retour chariot (\r)
#le saut de page (\f)
#la tabulation verticale (\v)
#Et tout autre caractère Unicode d'espace blanc.


#re.sub(r'\s+', ' ', text) : l r m3neha chnw t7b t3wth





def detect_language(text):
    return detect(text)

#import pdfplumber
def extract_text_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        return " ".join([page.extract_text() for page in pdf.pages if page.extract_text()])
#"".join() permet de concatiner deux chaine en mettant entre eux ""
# if page.extract_text() hthi t3tik kn fama page fi wst l pdf fr8a tt3adeha ex page one  page three





#import re
#from collections import Counter # You'd need this import at the top of your file

# Assuming adjust_text_length and llm are defined elsewhere
# def adjust_text_length(text, max_length): ...
# llm = Llama(...)
def fix_json_braces(json_str):
    open_braces = json_str.count('{')
    close_braces = json_str.count('}')
    if open_braces > close_braces:
        json_str += '}' * (open_braces - close_braces)
    elif close_braces > open_braces:
        # Tenter de tronquer la fin si trop d'accolades fermantes non appariées
        # Ceci est une heuristique et peut ne pas fonctionner pour tous les cas
        balance = 0
        fixed_str = ""
        for char in json_str:
            if char == '{':
                balance += 1
            elif char == '}':
                balance -= 1
            fixed_str += char
            if balance == 0 and char == '}':  # Found a balanced object
                break
        json_str = fixed_str
    return json_str

def extract_invoice_data(full_prompt_for_llm, chunk_text_for_debug):
    # NOUVELLE LIGNE DE DÉBOGAGE ICI:
    print(f"DEBUG: Contenu du chunk envoyé au LLM (premiers 500 chars):\n{chunk_text_for_debug[:500]}...")

    #hthi l basee
    #print(len(text))
    #print(f"DEBUG: Longueur du texte avant ajustement : {len(text)}")
    #words = text.lower().split() # Convert to lowercase & split by spaces
    #.split() t9slk chaine w t7thlk fi liste  bl espace kol win fama espace rahi hk element w7dou fi liste

    # 93din n7throu txt  pour une analyse et traitement facile efficaces ( ki trod lkol miniscules bch ywli y3tbr  majus w mius nfs l klma mch 7aja o5ra
    # w hne bdlna chaine ll liste des mots )



    #rit ekl liste hki mch bch ttb3th ll llama rw bch ttb3th chaine ama l but mn liste hki l developpeur bch ytthbr fl donnes eli wslou l facture w kn m5dmtch w e

    #word_count = Counter(words)
    #print(word_count)
    #print(f"DEBUG: Compte de mots : {word_count}")
    ## counter calcule l occurence de chaque mot dans la liste




                                       # prmpt_base_content = ""


                                        #if not prpt_from_client:  # If the client (test_api.py) sent an empty prompt
                                         #  You are an expert at extracting structured data from documents.
                                          #  Your task is to extract specific invoice details from the text provided below.
                                           # You MUST respond ONLY with a valid JSON object. Do NOT include any other text, explanations, or conversational phrases.
                                            #If a field is not found, its value must be `null`.

                                            #Invoice Text:
                                            #---
                                            #{text}
                                            #---

                                            #Return the extracted fields in the following JSON format.
                                            #Strictly adhere to this format, including the markdown code block.

                                            #```json
                                   # {{
                                    #  "vendor_name": null,
                                     # "invoice_date": null,
                                      #"total_amount": null,
                                      #"invoice_number": null,
                                      #"total_tax_percentage": null,
                                      #"devise": null,
                                      #"debit_note": null
                                    #}}
                                    #```
                                     #   """
                                        #else: # If the client sent a custom prompt (like your detailed 'txt')
                                            # Use the client's prompt as base and replace the {text} placeholder
                                            #if "{text}" in prpt_from_client:
                                             #   prmpt_base_content = prpt_from_client.replace("{text}", text)
                                           # else:
                                                # Fallback if client's prompt doesn't have {text} (shouldn't happen with your current txt)
                                              #  prmpt_base_content = f"{prpt_from_client}\n\nInvoice Text:\n---\n{text}\n---"

                                             # Always append the crucial "primer" for JSON output
                                        #prmpt_final = f"""{prmpt_base_content}

                                    #**Response:**
                                    #```json
                                   #"""





                    # ken l utlisateur ma9al chy (prpt=="")  w md5l ken l facture rahou l prompt chtkoun automatique hethi eli mwjouda hne w tad5il l text eli tb3th b3d msrlou modification w kol rahou chysir hka  (prmpt = f""" {text})
                    # kn l utilisteur da5al 7aja  prt (eli mwjouda fi mainCl ) rahou hka chtd5l ( prmpt=text+" "+prpt )  m3neha juste  tktefi bli b3thou l utilisateur tzidch 3lih l automatique


                   # print(f"DEBUG: Prompt final envoyé au LLM : {prmpt_final}")
                 #This section of your code is the core of how you communicate with the intelligent assistant

                    # etape1:preparation
                    #json_str=""

                    # etape 2  bch tb3th l prompt ll lama  (base mt3 communication bin l client w llama
                    #textP=prpt
                    #print(textP)



    response = llm.create_completion(full_prompt_for_llm,
    temperature=0.0,
    #For strict data extraction, factual questions, or consistent, machine-readable output (like JSON), keep temperature low (0.1 to 0.3).
    #For creative tasks, brainstorming, diverse responses, or more conversational interactions, set temperature higher (0.7 to 1.0 or even above, depending on the model's range)
    max_tokens=4096,
    stop=["```", "\nOutput:", "\n\nOutput:", "\n```json"]
    )


    # etape 3: recevoir la reponse de llama

    print(f"DEBUG: Réponse brute du LLM : {response}")
    response_text = response["choices"][0]["text"].strip()
    print(f"DEBUG: Texte brut de la réponse (strip) : {response_text}")  # Affichez ceci pour vérifier !

    match = re.search(r'(\{[\s\S]*\})', response_text, re.DOTALL)
    parsed_data = None
    if match:
        json_str = match.group(0)  # group(0) récupère toute la correspondance
        json_str = fix_json_braces(json_str)  # Tentative de réparer les accolades
        try:
            parsed_data = json.loads(json_str)
            print(f"DEBUG: JSON parsé avec succès : {parsed_data}")
        except json.JSONDecodeError as e:
            print(f"Erreur de parsing JSON même après réparation : {e}")
            return {"error": f"Erreur de format JSON: {e}"}
    else:
        print("WARNING: Aucun bloc JSON trouvé par regex dans la réponse du LLM.")
        return {"error": "Aucun bloc JSON trouvé"}

    return parsed_data
    #if match:
            #json_str = match.group(1)
            #json_str = fix_json_braces(json_str)  # <--- Appel ici
            #try:
                #parsed_data = json.loads(json_str)
            #except Exception as e:
                #print("Erreur de parsing JSON même après réparation :", e)
                #return {"error": "Erreur de format JSON"}
            #return parsed_data
    #return {"error": "Erreur de format JSON"}

    # finding and extracting the json

    # match = re.search(r'```json\s*(\{.*?\})\s*```', response_text, re.DOTALL) # Step 1

    # hne 93din nlwjou 3ala json (ybda w youfa b }) re.dotall l role mt3heha tchouf les ligne lkol m3neha  {.*?\}     5tr hthi mstnsi nverifiw biha ligne khw
    # m3neha nverifiw text eli rj3 json w ela le

    #json_str = ""
    #if match:
        #json_str = match.group(1)
        #print(f"DEBUG: Chaîne JSON extraite par regex : {json_str}")
    #return json_str

def validate_invoice_data(data):
    # Étape 1 : parser le JSON si besoin
    if isinstance(data, dict):
        parsed_data = data
    else:
        try:
            parsed_data = json.loads(data)
        except json.JSONDecodeError:
            return jsonify({"error": "Erreur de format JSON"}), 400

    # Étape 2 : valider le champ "Numéro de facture"
    if "Numéro de facture" in parsed_data:
        match = re.match(r'^\d{5,10}$', parsed_data.get("Numéro de facture"))
        if not match:
            parsed_data["Numéro de facture"] = "Corriger manuellement"

    return parsed_data


##  ti mw llama par defaut trj3 chaine  l but mt3 validate_invoice_data  hiya tverifie eli llama rj3t json mch juste chaine w b3d json hka hiya t7wlou ll dictionnaire bch njmou nt3mlou m3aha w kol fi 7ajet o5ra








@app.route('/extract', methods=['POST'])









# extract hthi mwjouda fl backend ama hiya awl w7da tt3ml m3a l API (serveur t3 restau ) ttsma endpoint (point dentree de l api )
def extract():
    print("\nINFO: Requête /extract reçue.")

    #1: recevoir un pdf
    #print(request.files)
    if 'file' not in request.files:
        print("ERROR: Aucun fichier fourni dans la requête.")
        return jsonify({"error": "Aucun fichier fourni"}), 400

    file = request.files['file']
    prpt_from_client_str=request.form.get("prpt","")


    #2: save un pdf
    pdf_path = "temp_facture.pdf"
    file.save(pdf_path)

    #3.extract text mn pdf
    #text = extract_text_from_pdf(pdf_path)

    try:
        # Tente d'extraire le texte du PDF scanné
        text = pdf2Image.extract_text_from_scanned_pdf(pdf_path)
        if not text:
            print("WARNING: Le texte extrait du PDF est vide.")
            return jsonify({"error": "Aucun texte extractible du PDF"}), 400

    except Exception as e:
        print(f"CRITICAL ERROR: Échec de l'extraction de texte à partir du PDF scanné : {e}")
        traceback.print_exc()
        return jsonify({"error": "Échec de l'extraction de texte du PDF"}), 500

    # ce que j ai modifie
    # Try a chunk size that leaves room for the prompt overhead:
   # MAX_PROMPT_OVERHEAD_TOKENS = 200
    # Estimate the length of your static prompt parts
    #MAX_GENERATION_TOKENS = 200
    #EFFECTIVE_CONTEXT_WINDOW = 512  # This is what the error message says is being used

    # Maximum tokens available for the actual text chunk
    #OPTIMAL_CHUNK_SIZE_TOKENS = EFFECTIVE_CONTEXT_WINDOW - MAX_PROMPT_OVERHEAD_TOKENS

    # Ensure it's not negative if prompt overhead is too large


    # Llama 3 a souvent un context_size de 8192, ce qui permet des prompts plus longs.
    # Votre prompt est d'environ 300-400 tokens, la réponse JSON peut être 100-500 tokens.
    # Laissez beaucoup de marge.
    MAX_OUTPUT_TOKENS_PER_CHUNK = 100  # Espace pour la réponse JSON
    MAX_PROMPT_TOKENS = llm.n_ctx()- MAX_OUTPUT_TOKENS_PER_CHUNK

    # Estimation de la longueur de la partie fixe du make_prompt()
    # Cela doit être mesuré précisément si possible, mais c'est une bonne estimation de départ
    STATIC_PROMPT_OVERHEAD = len(llm.tokenize(
        "Extract the following fields from the invoice text below. If a field is not present, set it to null.\n\nText:\n---\n\n---\n\nReturn only a valid JSON object with these fields:\nvendor_name, invoice_date, total_amount, invoice_number, total_tax_percentage, devise, debit_note, amount, total, items\n\nExample:\n{{\n  \"vendor_name\": \"ACME Corp\",\n  \"invoice_date\": \"2024-01-01\",\n  \"total_amount\": 1000.0,\n  \"invoice_number\": \"INV-12345\",\n  \"total_tax_percentage\": 20.0,\n  \"devise\": \"EUR\",\n  \"debit_note\": null,\n  \"amount\": [],\n  \"total\": 1200.0,\n  \"items\": [\n    {{\n      \"description\": \"Service A\",\n      \"quantity\": 2,\n      \"unit_price\": 500.0,\n      \"line_total\": 1000.0\n    }}\n  ]\n}}\nDo not write any code, do not write any explanation, do not use markdown. Output only the JSON object.".encode(
            'utf-8')))

    chunk_size_tokens = MAX_PROMPT_TOKENS - STATIC_PROMPT_OVERHEAD  # Espace restant pour le texte de la facture




    if chunk_size_tokens <= 0:

        chunk_size_tokens= 50 # Fallback to a small chunk size
    elif chunk_size_tokens < 100:  # Optionally enforce a minimum reasonable chunk size
        print(
            f"WARNING: Calculated chunk_size_tokens ({chunk_size_tokens}) is very small. Consider reducing prompt or output size.")

        print(f"WARNING: `chunk_size_tokens` calculé était trop bas, forcé à {chunk_size_tokens}.")

    chunk_overlap_tokens = int(chunk_size_tokens * 0.1)
    # A reasonable overlap (e.g., 10% of chunk size)
    print(f"WARNING: `chunk_size_tokens` calculé était trop bas, forcé à {chunk_size_tokens}.")

    invoice_chunks = split_text_into_chunks_langchain(
        text,
        chunk_size_tokens,
        chunk_overlap_tokens

    )
    if not invoice_chunks:
        print("Aucun chunk généré. Le texte d'entrée est-il trop court ou invalide ?")
        return jsonify({"error": "Aucun chunk généré à partir du texte du PDF."}), 400
    print(f"   -> Texte découpé en {len(invoice_chunks)} chunks.")






    all_extracted_data_from_chunks = []
    #traitement de chaque chunk par le modele LLama
    def make_prompt(chunk):
        return f"""
    Extract the following fields from the invoice text below. If a field is not present, set it to null.

    Text:
    ---
    {chunk}
    ---

    Return only a valid JSON object with these fields:
    vendor_name, invoice_date, total_amount, invoice_number, total_tax_percentage, devise, debit_note, amount, total, items

    Example:
    {{
      "vendor_name": "ACME Corp",
      "invoice_date": "2024-01-01",
      "total_amount": 1000.0,
      "invoice_number": "INV-12345",
      "total_tax_percentage": 20.0,
      "devise": "EUR",
      "debit_note": null,
      "amount": [],
      "total": 1200.0,
      "items": [
        {{
          "description": "Service A",
          "quantity": 2,
          "unit_price": 500.0,
          "line_total": 1000.0
        }}
      ]
    }}
    Do not write any code, do not write any explanation, do not use markdown. Output only the JSON object.
    """



    for i, chunk in enumerate(invoice_chunks):

        # ou bien ca : for chunk in invoice_chunks:
        current_llm_prompt = make_prompt(chunk)
        extracted_info_from_chunk = extract_invoice_data(current_llm_prompt , chunk)
        print(f"DEBUG: Raw extracted info from chunk {i + 1}: {extracted_info_from_chunk}")
        parsed_data=validate_invoice_data(extracted_info_from_chunk)

        print(f"DEBUG: validate_invoice_data a retourné Type: {type(parsed_data)}, Contenu: {parsed_data}")  # C'est le dictionnaire retourné !

        # C'est la ligne clé qui UTILISE ce dictionnaire
        print(f"printed parsed data: {parsed_data}")
        if isinstance(parsed_data, dict) and "error" not in parsed_data:
            all_extracted_data_from_chunks.append(parsed_data)
            print(f"DEBUG: Ajout de dictionnaire valide du chunk {i + 1} à la liste de consolidation.")
        else:

            # Check if parsed_data is None first
            if parsed_data is None:
                error_msg = 'Aucune donnée (parsed_data est None)'
            elif isinstance(parsed_data, dict):
                error_msg = parsed_data.get('error', 'Inconnu')
            else:
                # Fallback for other unexpected types if parsed_data is not dict or None
                error_msg = f"Type de donnée inattendu: {type(parsed_data).__name__}"

            print(f"WARNING: Aucune donnée structurée valide extraite du Chunk {i + 1} ou erreur de validation: {error_msg}")


     # l mochkla tw chniaaa : enou   hthi  all_extracted_data_from_chunks liste fi wstha des dictionaires 5tr kol chunk yrj3 dictionaire   ama eni m7chtich kol chunk yrj3 dictionnaire 7chti fl5r b dictionnaire w7d w en plus  fama mochkla o5ra enou tl9a 7ajet yt3dou (d apres principe de chevauchement )

    # solution: # 4. Si la valeur n'est pas vide ET que la clé n'est pas encore dans notre dictionnaire
            #                         # if value mch fr8a w el key mch mwjouda f dictionnaire jdid
             # 1. On commence avec un dictionnaire vide pour les résultats finaux
    all_values_per_key = {}
            # htha m7tou fih les valeur lkol   mt3 kol key lwt3wdin w eli mch kifkif w lkol
            # exmple {'invoice_number': ['INV-123', 'INV-000123'], 'total_amount': ['100.00 EUR', '€100.00'], 'client_name': ['Acme Corp', 'Acme Corporation']}

            # rit hetha houa eli ylm resultat mt3 kol chunk
    EXPECTED_SCHEMA = {
        "vendor_name": None,
        "invoice_date": None,
        "total_amount": None,
        "invoice_number": None,
        "total_tax_percentage": None,
        "devise": None,
        "debit_note": None,
        "amount": [],  # Default for a list
        "total": None,  # Default for a number
        "items": []  # Default for a list of items
        # Add any other fields you expect to ALWAYS be in the final output
    }

    consolidated_data = EXPECTED_SCHEMA.copy()
        # htha l final  win bch n5liw lkol key valeur w7da  w htha b3d mywli json houwa eli yrj3



    for data_dict in all_extracted_data_from_chunks:
          print(f"DEBUG: Consolidation - Traitement de data_dict: {data_dict}, Type: {type(data_dict)}")
          for key, value in data_dict.items():
                if value  is not None and value != [] and value != {}:  # S'assurer que la valeur n'est pas vide
                    if isinstance(value, (list, dict)):
                        # Convert the list/dict to a JSON string representation
                        # This makes it hashable for Counter
                        value_to_store = json.dumps(value,sort_keys=True)
                    else:
                        value_to_store = value


                    if key not in all_values_per_key:
                        all_values_per_key[key] = []
                    all_values_per_key[key].append(value_to_store)

    for key, values in all_values_per_key.items():
          if values:
                # Utilise Counter pour trouver la valeur la plus commune
                most_common_value = Counter(values).most_common(1)[0][0]

                try:
                    # Si c'est un JSON string, on le reconvertit
                    if key in [ "items"]:
                        consolidated_data[key] = json.loads(most_common_value)
                    else:
                        consolidated_data[key] = most_common_value
                except  (json.JSONDecodeError, TypeError):
                    consolidated_data[key] = most_common_value
          elif key in EXPECTED_SCHEMA and EXPECTED_SCHEMA[key] is not None:
                # Si aucune valeur valide n'a été trouvée pour une clé, assurez-vous qu'elle est à son défaut (null ou [])
                consolidated_data[key] = EXPECTED_SCHEMA[key]


    print(f"INFO: Données consolidées avec succès : {consolidated_data}")

    return jsonify(consolidated_data)




# l mochkla hne chnia mithl ynjm y3tik kol mara date fi kol chunk date fl cas hetha m3tch bch n5ou awl date donc nmchi nchouf l frequence w enehi akthr w7da 93da tt3wd
            # donc twli m3tch (final_consolidated_data[key] = value) twli= most_common



# donc tw twli tsn3 liste fi kol valeur




            #4.bch tst3ml l fct extract voice data (eli hiiya l base t3 hetha eli st3mlna fiha llama )
   # hthi twli m3tch : extracted_data = extract_invoice_data(prpt,text)

    #validated_data = validate_invoice_data(extracted_data)



#jsonify hiya type de retour
import time
from huggingface_hub import hf_hub_download, HfApi, HfFileSystem


# l module hetha juste bch njm nb3thou l hne 

def download_model():
    model_path = "models/llama-3-8b-Instruct.Q4_K_M.gguf"

    # Vérifier si le modèle existe déjà localement
    if os.path.exists(model_path):
        print("Modèle déjà présent localement.")
        return model_path

    print("Tentative de téléchargement du modèle...")

    # Configuration du téléchargement
    repo_id = "Sarrabenzarti/llama-3-8b-instruct-gguf"
    filename = "llama-3-8b-Instruct.Q4_K_M.gguf"

    max_retries = 5
    wait_time = 30  # secondes entre les tentatives

    for attempt in range(max_retries):
        try:
            # Vérifier l'état du serveur
            fs = HfFileSystem()
            repo_status = fs.ls(repo_id)

            if any(file['name'] == filename for file in repo_status):
                print(f"Tentative {attempt + 1}/{max_retries}...")
                return hf_hub_download(
                    repo_id=repo_id,
                    filename=filename,
                    local_dir="models",
                    local_dir_use_symlinks=False,
                    resume_download=True
                )
            else:
                print("Fichier introuvable sur le Hub. Vérifiez le repo_id et filename.")
                break

        except Exception as e:
            print(f"Erreur: {str(e)}")
            print(f"Nouvelle tentative dans {wait_time} secondes...")
            time.sleep(wait_time)

    # Solution de secours si toutes les tentatives échouent
    print("\nÉchec du téléchargement automatique. Veuillez:")
    print("1. Télécharger manuellement depuis: https://huggingface.co/Sarrabenzarti/llama-3-8b-instruct-gguf")
    print("2. Placer le fichier dans le dossier 'models'")
    print("3. Relancer le programme")

    # Créer le dossier si nécessaire
    os.makedirs("models", exist_ok=True)
    return None
if __name__ == '__main__':
    print("🚀 Serveur en cours d'exécution avec Waitress sur le port 8080...")
    serve(app, host="0.0.0.0", port=8080)

    # w hetha zeda l kol juste bch njm nb3thou 
    model_path = download_model()

    if model_path:
        print(f"Modèle chargé: {model_path}")
        # Votre code de traitement ici...
    else:
        # Vérifier si le fichier a été placé manuellement
        manual_path = "models/llama-3-8b-Instruct.Q4_K_M.gguf"
        if os.path.exists(manual_path):
            print("Modèle manuel détecté. Lancement du traitement...")
            # Votre code de traitement ici...
        else:
            print("Modèle non disponible. Le programme s'arrête.")
