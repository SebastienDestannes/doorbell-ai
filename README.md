# doorbell-ai

Proof of concept — reconnaissance faciale en temps réel sur le flux vidéo d'une ESP32-CAM.

Un script Python lit le stream MJPEG de la caméra, détecte les visages frame par frame et les compare à un jeu de photos de référence. Les visages connus sont encadrés en vert, les inconnus en rouge.

```
[ESP32-CAM :81/stream] ──(MJPEG)──► doorbell.py ──► affichage cv2
                                          │
                                    face_recognition
                                    (dlib, local)
```

> **État actuel :** prototype fonctionnel. Pas encore de déclenchement sur sonnette, pas d'intégration Home Assistant.

## Stack

- `face_recognition` — détection et encodage (dlib sous le capot)
- `opencv-python` — lecture du stream MJPEG et affichage
- `numpy`
- ESP32-CAM en mode stream (serveur MJPEG sur le port 81)

## Utilisation

### Prérequis

- Python 3.10+
- ESP32-CAM flashée et accessible sur le réseau local
- `cmake` et `dlib` buildables (voir note ci-dessous)

### Installation

```bash
git clone https://github.com/your-username/doorbell-ai
cd doorbell-ai
python -m venv venv && source venv/bin/activate
pip install face_recognition opencv-python numpy
```

> **Note dlib :** la compilation prend plusieurs minutes. Sur Raspberry Pi, compter 15–20 min. Utiliser `--no-build-isolation` si pip échoue sur ARM.

### Ajouter des visages connus

```bash
# Un fichier = une personne. Le nom du fichier devient le label affiché.
cp photo_alice.jpg known_faces/alice.jpg
```

### Lancer

Mettre à jour l'IP de la caméra dans `doorbell.py` :

```python
ESP32_URL = "http://192.168.1.45:81/stream"  # adapter à votre réseau
```

```bash
python doorbell.py
```

Appuyer sur `q` pour quitter.

### Tester le stream seul

```bash
python test_stream.py
```

Vérifie que le flux ESP32 est lisible avant de lancer la reconnaissance.

## Structure

```
doorbell-ai/
├── doorbell.py        # script principal
├── test_stream.py     # test du flux vidéo seul
├── known_faces/       # photos de référence (gitignorées)
└── .gitignore
```

## Paramètres

Dans `doorbell.py` :

| Variable | Défaut | Description |
|---|---|---|
| `ESP32_URL` | `http://192.168.1.45:81/stream` | URL du stream MJPEG |
| `KNOWN_FACES_DIR` | `known_faces` | Dossier des photos de référence |
| `TOLERANCE` | `0.5` | Seuil de correspondance (0.4 = strict, 0.6 = permissif) |

Le script réduit chaque frame à 25 % avant la détection pour améliorer les performances, puis remet à l'échelle pour l'affichage.

## Pistes d'évolution

- [ ] Déclenchement sur appui sonnette plutôt que stream continu
- [ ] Publication du résultat via MQTT vers Home Assistant
- [ ] Sauvegarde des snapshots d'inconnus
- [ ] Service systemd pour tourner en arrière-plan sur RPi

## License

MIT