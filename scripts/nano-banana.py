#!/usr/bin/env python3
"""
nano-banana.py — tiny helper for generating images via Gemini 2.5 Flash Image.

Pulls API key from the `llm` CLI keystore (installed by simonw/llm).
Writes PNGs to docs/brand/samples/ai/ alongside a source_prompt.txt sibling.

Usage:
  python scripts/nano-banana.py <slug> "<prompt>"
  python scripts/nano-banana.py hero-texture "rough black and white ..."
"""
import base64
import json
import pathlib
import subprocess
import sys
import urllib.request

MODEL = "gemini-2.5-flash-image"   # aka "nano banana". gemini-3.1-flash-image-preview also available for the next generation
OUT_DIR = pathlib.Path(__file__).parent.parent / "docs" / "brand" / "samples" / "ai"


def get_key() -> str:
    r = subprocess.run(["llm", "keys", "get", "gemini"], capture_output=True, text=True, check=True)
    return r.stdout.strip()


def generate(prompt: str, slug: str) -> pathlib.Path:
    key = get_key()
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={key}"
    body = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"responseModalities": ["IMAGE"]},
    }
    req = urllib.request.Request(
        url,
        data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=90) as resp:
        result = json.load(resp)

    parts = result["candidates"][0]["content"]["parts"]
    img_part = next((p for p in parts if "inlineData" in p or "inline_data" in p), None)
    if img_part is None:
        raise RuntimeError(f"no image in response: {json.dumps(result)[:500]}")
    data = img_part.get("inlineData") or img_part.get("inline_data")
    png_bytes = base64.b64decode(data["data"])

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    img_path = OUT_DIR / f"{slug}.png"
    prompt_path = OUT_DIR / f"{slug}.prompt.txt"
    img_path.write_bytes(png_bytes)
    prompt_path.write_text(prompt + "\n")
    return img_path


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit("usage: nano-banana.py <slug> \"<prompt>\"")
    slug, prompt = sys.argv[1], sys.argv[2]
    out = generate(prompt, slug)
    print(f"✓ {out}")
