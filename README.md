# Extracteur de commentaires SPIP

Un script Python permettant de récupérer et d'exporter des commentaires du site `consultations-publiques.developpement-durable.gouv.fr`. Les données exportées peuvent être sauvegardées au format CSV et au format HTML avec une mise en page stylisée et une pagination.

## Pré-requis

- Python 3.x
- Bibliothèque `requests`
- Bibliothèque `BeautifulSoup4`

## Installation
Clonez ce dépôt sur votre machine locale.

```bash
git clone https://github.com/eclipseo/comments_extractor/
```

Accédez au répertoire contenant le script.

```bash
cd comments_extractor
```

Installez les paquets nécessaires avec pip, ou votre gestionnaire de paquets.

```bash
pip3 install beautifulsoup4 requests
```

Sous Fedora :

```bash
sudo dnf install python3-beautifulsoup4 python3-requests
```

Sous Ubuntu :

```bash
sudo apt install python3-bs4 python3-requests
```

Sous Arch :

```bash
sudo pacman -S python-beautifulsoup4 python-requests
```

## Utilisation

Exécutez le script depuis le terminal :

```bash
python3 comments_extractor.py
```

Suivez les instructions à l'écran pour entrer l'ID de l'article obtenu dans ;'URL et la valeur max des commentaires obtenue sur la pagination des commentaires. Le script récupérera ensuite les commentaires et les sauvegardera.

## Licence

Ce script est licencié sous la [license Unlicense](https://github.com/eclipseo/comments_extractor/blob/main/LICENSE).
