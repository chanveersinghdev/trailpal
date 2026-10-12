---
title: TrailPal Punjab - an offline nature ID that gets you off the screen
published: false
tags: devchallenge, hf26challenge
---

*This is a submission for the [Hacktoberfest Open-Source AI Challenge Week 1: Touch Grass](https://dev.to/challenges/hacktoberfest-week1-2026-10-05)*

## What I Built
TrailPal Punjab is an offline "what's that?" app for walks. Snap a plant, bird or insect and a local open-weight model names it and gives a fun fact, checked against a local list of Punjab species. A daily quest ("find 3 things") nudges you to go outside, and once it's done the app tells you to put the phone away. The screen is the shortest part of the experience. Built for hikers, kids, students and anyone curious about the trees and birds around them.

## Demo
<!-- add video or screenshots here -->

## Code
{% embed https://github.com/Chanveersingh/trailpal %}
<!-- replace with your real repo link -->

## How I Built It
- **Gemma 3 (4B)**, an open-weight vision model, run locally with **Ollama**
- **Streamlit** for a simple camera-friendly UI
- A local `species.json` of Punjab plants and birds to ground answers and reduce hallucinations
- JSON-mode prompts so the model returns name, type, confidence and a fact
- Sound tab: describe a bird call in words and the model suggests likely birds

## Why Does Open Innovation Matter?
- **Works with no signal.** Trails don't have bars. After a one-time model download it runs fully offline.
- **Privacy.** Photos never leave the device.
- **Free.** No API key, no per-call cost, which matters for students.
- **Swappable and tunable.** Change one line to try another model, or add local species to the JSON. A closed API can't be tuned to Punjab's trees and birds.

## How It Went Outside
<!-- 2-3 lines: where you tested it, what it got right/wrong. Bonus points! -->

## Prize Categories
<!-- list any that apply, or delete this section -->
