"""TrailPal Punjab - offline 'what's that?' for the outdoors.
Runs fully local: Ollama (open-weight vision model) + Streamlit + JSON.
"""
import json, io, difflib
from datetime import date
from pathlib import Path

import streamlit as st
import ollama
from PIL import Image

MODEL = "gemma3:4b"          # swap for qwen2.5vl:3b, llava, etc.
QUEST_GOAL = 3
BASE = Path(__file__).parent
SPECIES = json.loads((BASE / "data" / "species.json").read_text(encoding="utf-8"))
LOG = BASE / "sightings.json"

PROMPT = """You are a careful naturalist in Punjab, India.
Identify the main plant, bird or insect in this photo.
Reply ONLY with JSON: {"name": "common name", "type": "bird|plant|insect|other",
"confidence": "low|medium|high", "fact": "one short fun fact"}.
If you are unsure, say confidence low. Do not invent."""

SOUND_PROMPT = """You are a birding guide in Punjab, India. The user describes a bird sound:
"{desc}"
Suggest the 3 most likely common Punjab birds. Reply ONLY with JSON:
{{"guesses": [{{"name": "...", "why": "short reason"}}]}}"""


def load_log():
    if LOG.exists():
        return json.loads(LOG.read_text(encoding="utf-8"))
    return []


def save_log(entries):
    LOG.write_text(json.dumps(entries, indent=2), encoding="utf-8")


def ask(messages):
    r = ollama.chat(model=MODEL, messages=messages, format="json")
    return json.loads(r["message"]["content"])


def local_match(name):
    names = [s["name"] for s in SPECIES]
    hit = difflib.get_close_matches(name.title(), names, n=1, cutoff=0.6)
    if not hit:
        low = name.lower()
        hit = [n for n in names if n.lower() in low or low in n.lower()][:1]
    return next((s for s in SPECIES if s["name"] == hit[0]), None) if hit else None


st.set_page_config(page_title="TrailPal Punjab", page_icon="🌿", layout="centered",
                   initial_sidebar_state="collapsed")
st.markdown(f"<style>{(BASE / 'static' / 'glass.css').read_text(encoding='utf-8')}</style>",
            unsafe_allow_html=True)
st.title("🌿 TrailPal Punjab")
st.caption("Offline nature ID. Snap it, learn it, put the phone away.")

log = load_log()
today = date.today().isoformat()
today_n = sum(1 for e in log if e["date"] == today)

st.progress(min(today_n / QUEST_GOAL, 1.0), text=f"Daily quest: {today_n}/{QUEST_GOAL} finds")
if today_n >= QUEST_GOAL:
    st.success("Quest done! Close this tab and keep walking. 🚶")

tab1, tab2, tab3 = st.tabs(["📷 Identify", "🎧 What's that sound?", "📒 My finds"])

with tab1:
    pic = st.camera_input("Take a photo") or st.file_uploader("...or upload one", type=["jpg", "jpeg", "png"])
    if pic and st.button("What is this?", type="primary"):
        img = Image.open(pic).convert("RGB")
        img.thumbnail((768, 768))            # smaller = faster on laptops
        buf = io.BytesIO(); img.save(buf, "JPEG")
        with st.spinner("Thinking locally..."):
            try:
                res = ask([{"role": "user", "content": PROMPT, "images": [buf.getvalue()]}])
            except Exception as e:
                st.error(f"Is Ollama running and `{MODEL}` pulled? ({e})"); st.stop()
        name = res.get("name", "Unknown")
        match = local_match(name)
        st.subheader(name)
        st.write(f"**Type:** {res.get('type','?')}  |  **Confidence:** {res.get('confidence','?')}")
        st.info(match["fact"] if match else res.get("fact", ""))
        if match:
            st.caption("✅ Matched in the local Punjab species list")
        log.append({"date": today, "name": name, "type": res.get("type", "other")})
        save_log(log)

with tab2:
    desc = st.text_input("Describe the sound (e.g. 'loud rising ku-oo ku-oo from a mango tree')")
    if desc and st.button("Guess the bird"):
        with st.spinner("Listening in my head..."):
            try:
                res = ask([{"role": "user", "content": SOUND_PROMPT.format(desc=desc)}])
                for g in res.get("guesses", []):
                    st.write(f"**{g.get('name')}**: {g.get('why')}")
            except Exception as e:
                st.error(str(e))

with tab3:
    if not log:
        st.write("Nothing yet. Go find something! 🌱")
    for e in reversed(log[-30:]):
        st.write(f"{e['date']}  ·  {e['name']}  ({e['type']})")
    st.metric("Total finds", len(log))
