import torch
import torchaudio as ta
from chatterbox.tts import ChatterboxTTS

device = "mps" if torch.backends.mps.is_available() else "cpu"
model = ChatterboxTTS.from_pretrained(device=device)

text = "The rain had eased by the time we reached Galway, and the hills had gone soft and grey."

wav = model.generate(
    text,
    audio_prompt_path="ref.wav",   # remove this line to use the default voice
    exaggeration=0.35,             # lower = calmer, flatter delivery
    cfg_weight=0.4,                # lower = slower pacing
)
ta.save("out.wav", wav, model.sr)
print("Saved out.wav")
