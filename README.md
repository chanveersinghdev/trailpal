# 🌿 TrailPal Punjab

Offline "what's that?" for the outdoors. Point your camera at a plant, bird or insect,
get the name plus a fun fact from a **local open-weight model**. No internet, no cloud,
no photos leave your device. A daily quest (find 3 things) gets you outside.

## Run it
```bash
# 1. install Ollama: https://ollama.com
ollama pull gemma3:4b          # one-time download (~3.3 GB); works offline after
pip install -r requirements.txt
streamlit run app.py
```
Open on your phone via the "Network URL" Streamlit prints (same Wi-Fi/hotspot),
or just run it on a laptop and carry it on a walk.

## Open-source pieces
- **Gemma 3** (open-weight vision model) via **Ollama** (local inference)
- **Streamlit** UI, **Pillow**, local JSON species list (`data/species.json`)
- Swap the model by changing `MODEL` in `app.py` (e.g. `qwen2.5vl:3b`).

## Add your own species
Edit `data/species.json`, no retraining needed.
