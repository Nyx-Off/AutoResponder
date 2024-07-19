import os
import subprocess
import requests
import zipfile
from gtts import gTTS
from pydub import AudioSegment

FFMPEG_URL = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
FFMPEG_DIR = "ffmpeg"

def installer_dependances():
    try:
        import gtts
        import pydub
        import requests
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "gtts", "pydub", "requests"])

def verifier_ffmpeg():
    try:
        subprocess.run(['ffmpeg', '-version'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("FFmpeg est déjà installé.")
    except (subprocess.CalledProcessError, FileNotFoundError):
        chemin_ffmpeg = trouver_ffmpeg()
        if chemin_ffmpeg:
            print("FFmpeg est déjà téléchargé mais n'est pas trouvé dans PATH. Ajout à PATH.")
            ajouter_au_path(chemin_ffmpeg)
        else:
            print("FFmpeg n'est pas installé. Téléchargement en cours...")
            telecharger_ffmpeg()

def trouver_ffmpeg():
    for root, dirs, files in os.walk(FFMPEG_DIR):
        if 'ffmpeg.exe' in files:
            return root
    return None

def telecharger_ffmpeg():
    local_zip = "ffmpeg.zip"
    with requests.get(FFMPEG_URL, stream=True) as r:
        r.raise_for_status()
        with open(local_zip, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    print("Téléchargement de FFmpeg terminé. Décompression en cours...")
    with zipfile.ZipFile(local_zip, 'r') as zip_ref:
        zip_ref.extractall(FFMPEG_DIR)
    os.remove(local_zip)
    chemin_ffmpeg = trouver_ffmpeg()
    if chemin_ffmpeg:
        ajouter_au_path(chemin_ffmpeg)
        print("FFmpeg a été installé et configuré.")
    else:
        print("Erreur : FFmpeg n'a pas pu être trouvé après le téléchargement.")

def ajouter_au_path(chemin):
    os.environ["PATH"] += os.pathsep + chemin
    print(f"Le chemin {chemin} a été ajouté au PATH.")
    with open("add_to_path.bat", "w") as bat_file:
        bat_file.write(f'setx PATH "%PATH%;{chemin}"\n')
    subprocess.run("add_to_path.bat", shell=True)
    os.remove("add_to_path.bat")

def lire_fichier(fichier_chemin):
    with open(fichier_chemin, 'r', encoding='utf-8') as fichier:
        return fichier.read()

def diviser_texte(texte, taille_max=1024):
    return [texte[i:i+taille_max] for i in range(0, len(texte), taille_max)]

def texte_to_parole(texte, sortie_fichier):
    tts = gTTS(text=texte, lang='fr')
    tts.save(sortie_fichier)
    son = AudioSegment.from_file(sortie_fichier)
    return son

def ajouter_musique(son_texte, musique_chemin, sortie_finale, texte_volume=0, musique_volume=0):
    musique = AudioSegment.from_file(musique_chemin)
    duree_cible = len(son_texte) + 3000  # en millisecondes
    son_texte = son_texte + texte_volume
    musique = musique + musique_volume
    musique = musique[:duree_cible]
    mix = musique.overlay(son_texte)
    mix.export(sortie_finale, format='mp3')

def traiter_fichier(fichier_texte, fichier_musique, texte_volume=0, musique_volume=0):
    texte = lire_fichier(fichier_texte)
    nom_fichier_txt = os.path.basename(fichier_texte)
    nom_base = os.path.splitext(nom_fichier_txt)[0]
    dossier_sortie = os.path.join(".", nom_base)
    os.makedirs(dossier_sortie, exist_ok=True)
    
    morceaux = diviser_texte(texte)
    fichiers_audio = []
    for index, morceau in enumerate(morceaux):
        fichier_son_texte = os.path.join(dossier_sortie, f"{nom_base}_voix_{index}.mp3")
        son = texte_to_parole(morceau, fichier_son_texte)
        fichiers_audio.append(son)
    
    son_combine = fichiers_audio[0]
    for son in fichiers_audio[1:]:
        son_combine += son
    
    fichier_sortie_combine = os.path.join(dossier_sortie, f"{nom_base}_combine.mp3")
    son_combine.export(fichier_sortie_combine, format='mp3')
    
    fichier_sortie = os.path.join(dossier_sortie, f"{nom_base}_final.mp3")
    ajouter_musique(son_combine, fichier_musique, fichier_sortie, texte_volume, musique_volume)
    print(f"Fichier audio final généré : {fichier_sortie}")

def main():
    installer_dependances()
    verifier_ffmpeg()
    repertoire_racine = "."  # Spécifiez le répertoire racine
    fichier_musique = "Musique.mp3"
    fichiers_txt = [f for f in os.listdir(repertoire_racine) if f.endswith('.txt')]
    
    texte_volume = 0  # Ajustez le volume du texte ici
    musique_volume = 2  # Ajustez le volume de la musique ici
    
    for fichier_txt in fichiers_txt:
        chemin_fichier_txt = os.path.join(repertoire_racine, fichier_txt)
        traiter_fichier(chemin_fichier_txt, fichier_musique, texte_volume, musique_volume)

if __name__ == "__main__":
    main()
