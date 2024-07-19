# AutoResponder

AutoResponder est un script Python qui génère automatiquement des réponses audio à partir de fichiers texte en utilisant la synthèse vocale. Il combine la voix générée avec une piste musicale spécifique et permet d'ajuster les volumes de la voix et de la musique.

## Fonctionnalités

- Convertit le texte en parole avec `gTTS` (Google Text-to-Speech).
- Combine la parole générée avec une piste musicale.
- Ajuste le volume de la voix et de la musique.
- Télécharge et installe automatiquement FFmpeg si nécessaire.
- Installe automatiquement les dépendances Python requises (`gtts`, `pydub`, `requests`).

## Prérequis

- Python 3.x
- pip (gestionnaire de paquets pour Python)

## Installation

1. Clonez le dépôt GitHub :
    ```sh
    git clone https://github.com/votre-utilisateur/AutoResponder.git
    cd AutoResponder
    ```

2. Exécutez le script Python :
    ```sh
    python start.py
    ```

Le script vérifiera et installera automatiquement les dépendances nécessaires.

## Utilisation

1. Placez vos fichiers `.txt` dans le même répertoire que le script `start.py`.
2. Placez votre fichier musical (par exemple, `musique.mp3`) dans le même répertoire que le script.
3. modifier cette ligne pour inclure le fichier musical au programme : 
```python
fichier_musique = "Musique.mp3"
```
4. Modifiez les paramètres de volume dans le script `start.py` si nécessaire :
    ```python
    texte_volume = 0  # Ajustez le volume du texte ici (en dB)
    musique_volume = 1  # Ajustez le volume de la musique ici (en dB)
    ```

5. Exécutez le script :
    ```sh
    python start.py
    ```

Les fichiers audio générés seront placés dans des dossiers portant le même nom que les fichiers texte d'origine.

## Contribuer

Les contributions sont les bienvenues ! Veuillez soumettre une pull request ou ouvrir une issue pour discuter des modifications que vous souhaitez apporter.

## Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

## Auteurs

- [Nyx-Off](https://github.com/Nyx-Off)

---

**Note :** Assurez-vous d'avoir une connexion Internet active lors de la première exécution du script pour permettre le téléchargement des dépendances et de FFmpeg.

