"""Voice-clone narration with Chatterbox (Resemble AI, MIT), run locally. Called by render.py when --voice-ref is set;
it runs in its own venv because Chatterbox pins torch 2.6:

    uv venv --python 3.11 ~/venvs/chatterbox && uv pip install --python ~/venvs/chatterbox/bin/python chatterbox-tts
    ~/venvs/chatterbox/bin/python growth/video/clone_tts.py jobs.json

jobs.json: {"ref": "<reference clip>", "exaggeration": 0.5, "cfg": 0.5,
            "jobs": [{"text": "...", "out": "<path>.wav"}, ...]}
Chatterbox stamps every clip with Resemble's inaudible PerTh watermark (marks it as AI audio)."""
import json, os, re, sys, time

import torch, torchaudio as ta
from chatterbox.tts import ChatterboxTTS

MAX_CHARS = 280  # long inputs drift or get cut off; generate sentence groups and join them


def chunks(text):
    sents = re.split(r"(?<=[.!?])\s+", text.strip())
    out, cur = [], ""
    for s in sents:
        if cur and len(cur) + 1 + len(s) > MAX_CHARS:
            out.append(cur)
            cur = s
        else:
            cur = f"{cur} {s}".strip()
    if cur:
        out.append(cur)
    return out


def main(path):
    spec = json.load(open(path))
    # CPU, not the Mac GPU: on the M5 Pro the same 25 s clip took 59 s on CPU and 166 s on MPS (2026-11-06).
    device = os.environ.get("CLONE_DEVICE", "cpu")
    _load = torch.load
    torch.load = lambda *a, **k: _load(*a, **{**k, "map_location": torch.device(device)})  # weights were saved on CUDA
    t0 = time.time()
    model = ChatterboxTTS.from_pretrained(device=device)
    print(f"loaded on {device} in {time.time() - t0:.0f}s", flush=True)
    gap = torch.zeros(1, int(model.sr * 0.18))
    for job in spec["jobs"]:
        if os.path.exists(job["out"]):
            continue
        t1 = time.time()
        parts = []
        for c in chunks(job["text"]):
            wav = model.generate(c, audio_prompt_path=spec["ref"], exaggeration=spec.get("exaggeration", 0.5),
                                 cfg_weight=spec.get("cfg", 0.5))
            parts += [wav.cpu(), gap]
        audio = torch.cat(parts[:-1], dim=1)
        tmp = job["out"] + ".part.wav"
        ta.save(tmp, audio, model.sr)
        os.replace(tmp, job["out"])
        print(f"{os.path.basename(job['out'])}: {audio.shape[1] / model.sr:.1f}s audio in {time.time() - t1:.0f}s", flush=True)


if __name__ == "__main__":
    main(sys.argv[1])
