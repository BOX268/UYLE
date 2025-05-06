from ultralytics import YOLO
import cv2
import os
import glob
import json


model_path = ""
paths = None
try :

    with open("paths.txt") as file :
        paths = json.load(file.read())
        model_path = paths["autolabel_model_path"]

except Exception as e :

    raise e
# Charger le modèle YOLOv8 entraîné


if not os.path.exists(model_path):
    raise FileNotFoundError(f"Erreur : Le fichier '{model_path}' n'existe pas.")
else:
    model = YOLO(model_path)
    print("✅ Modèle chargé avec succès.")

# Dossier contenant les images à auto-labelliser
image_folder = paths["images_folder"]
if not os.path.exists(image_folder):
    raise FileNotFoundError(f"Erreur : Le dossier '{image_folder}' n'existe pas.")

# Dossier où enregistrer les annotations
annotation_folder = paths["labels_folder"]
if not os.path.exists(image_folder):
    raise FileNotFoundError(f"Erreur : Le dossier '{annotation_folder}' n'existe pas.")

# Obtenir la liste des images
image_files = glob.glob(os.path.join(image_folder, "*.jpg"))

if not image_files:
    raise FileNotFoundError(f"Erreur : Aucune image '.jpg' trouvée dans '{image_folder}'.")

print(f"🔍 {len(image_files)} images trouvées pour l'auto-labellisation.")

# Processus d'annotation automatique
for image_path in image_files:
    print(f"\n🔹 Traitement de l'image : {image_path}")

    # Charger l'image
    image = cv2.imread(image_path)
    if image is None:
        print(f"⚠️ Erreur : Impossible de lire '{image_path}', fichier corrompu ou format non supporté.")
        continue

    height, width, _ = image.shape

    # Faire la détection avec YOLOv8
    results = model(image_path, conf=0.25)

    # Vérifier s'il y a bien des détections
    if not results:
        print(f"⚠️ Aucune détection trouvée pour '{image_path}'.")
        continue

    # Préparer le fichier d'annotation (nom identique à l’image, mais avec .txt)
    annotation_path = os.path.join(annotation_folder, os.path.basename(image_path).replace(".jpg", ".txt"))

    with open(annotation_path, "w") as f:
        for result in results:
            if result.boxes is not None and len(result.boxes) > 0:  # Vérifie s'il y a des boîtes détectées
                for i, box in enumerate(result.boxes):
                    x_center, y_center, bbox_width, bbox_height = box.xywhn.tolist()[0]  # Convertir en liste
                    class_id = int(box.cls.tolist()[0])  # Convertir en entier
                    confidence = float(box.conf.tolist()[0])  # Confiance de la prédiction

                    print(f"   📦 Boîte {i+1}: Classe {class_id}, Confiance {confidence:.2f}, Coordonnées {x_center:.3f}, {y_center:.3f}, {bbox_width:.3f}, {bbox_height:.3f}")

                    # Sauvegarder dans le format YOLO : class_id x_center y_center width height
                    f.write(f"{class_id} {x_center} {y_center} {bbox_width} {bbox_height}\n")

    print(f"✅ Annotation générée : {annotation_path}")

print("\n🎉 Auto-annotation terminée !")
