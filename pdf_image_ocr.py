#import pytesseract


#chnw ya3ml hetha l kol  w chnw l role mt3ou
# ki bch yjina pdf mch bthroura bch njmou n3mloulou copier coller bc njmou n5thou text eli fih
# yjm yjina pdf w howa a la base tswira mskaninou m3neha fl 7ala hethi nmjouch n3mloulou copier coller
# bch njmou nb3thouh ll llama w tfhmou lzmna n7wlou l pdf eli je ll text njmou nselctionih m3neha



# from pdf2image import convert_from_path
# from paddleocr import PaddleOCR
# import numpy as np


# #ti mw l ocr mt5dm kn 3ala tswr donc lzm n7wlou pdf ll image donc nst3mlou  from pdf2image import convert_from_path

# def extract_text_from_scanned_pdf(pdf_path):
#     #assert os.path.exists(pdf_path), "PDF file not found!"



# # poppler outil fondamental pour lire et manipuler les PDF (houa eli yconverti en image)

# #1.hthi l partie eli tconvertie pdf l image

#     poppler_path = r"C:\Program Files\poppler-24.08.0\Library\bin"
#     images = convert_from_path(pdf_path, poppler_path=poppler_path)
#     # image t5rjlk liste fiha des images



#     extracted_text = ""
#     ocr = PaddleOCR(use_angle_cls=True)
#     # hka demarrer lancer l OCR

#     # tst3ml hethi use_angle_cls     bch ykounou les documents parfaitement alignes

#     for img in images:
#         img_np = np.array(img).copy()  # Ensure correct format

#         # t7wwl kol pixel mt3 l image ll valeur numerique represente couleur et l intensite
#         #t5th les valeur w t7thom di tableau
#         # w 3mlna copy bch l original mttmsch
#         result = ocr.ocr(img_np)

#         #.ocr(ima_np) permet de lire le tableau eli fih des valeurs numerique eli 3tithoulha w trj3li restat sous formr de liste de liste


#         for line in result:
#             for word_info in line:
#                 extracted_text += word_info[1][0] + "\n"  # Extract text

#     return extracted_text.strip() if extracted_text else None

#print(extract_text_from_scanned_pdf("temp_facture3.pdf"))


#Il analyse les pixels de l'image.
#Il essaie de trouver des motifs qui ressemblent à des caractères (lettres, chiffres, symboles).
#Il regroupe ces caractères en mots ou segments de texte.
#Pour chaque mot/segment qu'il identifie, il stocke :
# hiya liste   [ [coordonnées_du_mot], ('LeMotReconnu', 0.98) ]
#Ses coordonnées (où il est).
#La chaîne de caractères qu'il pense avoir reconnue.
#Son score de confiance.




#type de result de l OCR  (explication detaille)
## 'result' est une LISTE

    # Premier élément de 'result' : C'est la PREMIÈRE LIGNE de texte détectée sur l'image

        # Premier élément de cette ligne : C'est le PREMIER MOT/SEGMENT de texte de la ligne
        #[ [coordonnées_du_mot1_ligne1], ('LeMot1', 0.99) ],

        # Deuxième élément de cette ligne : C'est le DEUXIÈME MOT/SEGMENT de texte de la ligne
        #[ [coordonnées_du_mot2_ligne1], ('Mot2', 0.98) ],

        # ... et ainsi de suite pour tous les mots/segments de cette première ligne ...
from pdf2image import convert_from_path
from paddleocr import PaddleOCR
import numpy as np
from PIL import Image

# Initialisation de l'OCR (une seule fois pour gagner du temps)
ocr_engine = PaddleOCR(use_angle_cls=True, lang='fr',enable_mkldnn=False) 

def extract_text_from_scanned_pdf(pdf_path):
    """Convertit un PDF en images puis extrait le texte."""
    poppler_path = r"C:\Program Files\poppler-24.08.0\Library\bin"
    images = convert_from_path(pdf_path, dpi=300, poppler_path=poppler_path)
    
    extracted_text = ""
    for img in images:
        img_gray = img.convert('L')
        img_np = np.array(img_gray.convert('RGB')).copy()
        
        result = ocr_engine.ocr(img_np)
        if  result and result[0] is not None: # Vérifie que Paddle a trouvé quelque chose
            for line in result:
                for word_info in line:
                    extracted_text += word_info[1][0] + " "
            extracted_text += "\n" # Saut de ligne après chaque page
            
    return extracted_text.strip()

def extract_text_from_image(image_path):
    """Extrait le texte directement d'une image (JPG, PNG, etc.)."""
    # 1. Charger l'image avec PIL
    img = Image.open(image_path).convert('RGB')
    # 2. Convertir en tableau numpy pour PaddleOCR
    img_np = np.array(img).copy()
    
    # 3. Lancer l'OCR
    result = ocr_engine.ocr(img_np)
    
    extracted_text = ""
    if result[0] is not None:
        for line in result:
            for word_info in line:
                # word_info[1][0] contient le texte reconnu
                extracted_text += word_info[1][0] + " "
                
    return extracted_text.strip()