import os
import glob
from PIL import Image

# Pour lire les fichiers HEIC, installer pillow-heif : pip install pillow-heif
try:
    import pillow_heif
    pillow_heif.register_heif_opener()  # Active l'ouverture des fichiers HEIC avec PIL
except ImportError:
    print("Module pillow-heif non installé. Les fichiers HEIC ne seront pas convertis.")

def convert_image_to_jpg(input_file, output_file):
    try:
        with Image.open(input_file) as img:
            # Convertir en mode RGB si nécessaire (certains formats PNG ou HEIC peuvent être en mode RGBA ou autre)
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")
            img.save(output_file, "JPEG")
            print(f"Converti : {input_file} -> {output_file}")
    except Exception as e:
        print(f"Erreur lors de la conversion de {input_file} : {e}")

def convert_images_in_folder(input_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Liste des extensions à convertir (on inclut jpeg, jpg, png et heic)
    extensions = ["*.jpeg", "*.jpg", "*.png", "*.heic"]
    files_to_convert = []
    for ext in extensions:
        files_to_convert.extend(glob.glob(os.path.join(input_dir, ext)))

    print(f"{len(files_to_convert)} fichiers trouvés dans {input_dir}")

    for file_path in files_to_convert:
        # Nom du fichier sans extension
        base_name = os.path.splitext(os.path.basename(file_path))[0]
        output_file = os.path.join(output_dir, base_name + ".jpg")
        convert_image_to_jpg(file_path, output_file)

if __name__ == "__main__":
    # Répertoire contenant les images d'entrée
    input_directory = "RectAdjust/UYLE/Sample/Images/Image_terrain_luminaire_V2"
    # Répertoire où sauvegarder les images converties
    output_directory = "RectAdjust/UYLE/Sample/Images"

    convert_images_in_folder(input_directory, output_directory)
