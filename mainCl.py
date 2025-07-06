import requests
# c est la base de la communication avec l API
# API Endpoint
url = "http://localhost:8080/extract"
# l adresse url (complete) de l API m3neha win script /utilisateur yb3th facture w el prompt

txt="""

You are an expert at extracting structured data from documents.
Your task is to extract specific invoice details from the text provided below.
You MUST respond ONLY with a valid JSON object. Do NOT include any other text, explanations, or conversational phrases.
If a field is not found, its value must be `null`.

Invoice Text:
---
{text}  
---

Return the extracted fields in the following JSON format.
Strictly adhere to this format, including the markdown code block.


```json
{{
  "vendor_name": null,
  "invoice_date": null,
  "total_amount": null,
  "invoice_number": null,
  "total_tax_percentage": null,
  "devise": null,
  "debit_note": null
}}
"""




files = {"file": open("temp_facture3.pdf", "rb")}  # Upload file
# lzm fl pc eli cht3ml bih tkoun esm l facture temp_facture3.pdf w l serveur bch yjih un dictionaire l cle esmou file :
data = {"prpt": txt}

# Préparer les données textuelles (le prompt) à envoyer au serveur.

response = requests.post(url, files=files, data=data)
# response bch trj3lk resultat t3 l envoi
# post() : Indique que c'est une requête HTTP POST m3neha bch tsir modification ll information eli tb3tht mch kima .get() juste t5ou des donnes  kima t3tini page web
if response.status_code == 200:  # l 200 hki 3ibara 3ala API raja3 reponse mch m3neha llama  a bien extrait la facture
    print("Extracted Data:", response.json())
else:
    print("Error:", response.status_code, response.text)

