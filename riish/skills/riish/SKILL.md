---
name: riish
description: Set up and run a free, local text-to-speech voice on a Mac that approximates a warm, calm, low Irish male narrator (like the ElevenLabs "Cillian" voice), using Chatterbox (Resemble AI, MIT licence) with voice cloning from a consented reference clip. Use this skill whenever the user asks for local, free or offline TTS, an Irish or warm male narrator voice, a Cillian-like voice, Chatterbox setup, or voice cloning on a Mac, even if they do not name Chatterbox.
---

# riish: a local Irish-narrator voice on a Mac

This skill walks the user through installing Chatterbox on macOS and generating calm narration in a cloned voice. Everything runs on their Mac, for free, after a one-time download.

## How to guide the user

- The user pastes commands into Terminal one at a time, and has previously pasted two commands onto one line by mistake. Give one command per fenced bash block, and say "paste this, press Return, wait for it to finish" when it helps.
- Go one step at a time. After each step, ask what Terminal printed before moving on, so an error is caught where it happens rather than three steps later.
- Skip any step whose check already passes (for example, Homebrew is already installed).
- Keep the consent rule in step 5 firm. Cloning a voice without permission harms a real person, and the ElevenLabs terms forbid using their output as a reference.

## 1. Install Homebrew

First check whether Homebrew is already there:

```bash
brew --version
```

If that prints a version, skip to step 2. Otherwise install it:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

At the end the installer prints "Next steps" with two lines (an `echo ... >> ~/.zprofile` line and an `eval ...` line). Tell the user to copy and run each of those two lines separately, then quit and reopen Terminal.

If `brew` is still not found after reopening Terminal, run this fallback:

```bash
eval "$(/opt/homebrew/bin/brew shellenv)"
```

## 2. Install Python 3.11 and ffmpeg

```bash
brew install python@3.11
```

```bash
brew install ffmpeg
```

Verify Python:

```bash
python3.11 --version
```

It should print `Python 3.11.x`.

## 3. Create a project folder and virtual environment

```bash
mkdir -p ~/tts && cd ~/tts
```

```bash
python3.11 -m venv cb
```

```bash
source cb/bin/activate
```

The prompt now starts with `(cb)`, which means the environment is active. Tell the user that every new Terminal window needs this before running anything here:

```bash
cd ~/tts && source cb/bin/activate
```

## 4. Install Chatterbox

```bash
pip install --upgrade pip
```

```bash
pip install chatterbox-tts
```

This takes several minutes because it downloads PyTorch. Warn the user so they do not think it has hung.

## 5. Get a reference clip

Chatterbox clones the voice in a short reference recording. The clip decides the accent, depth and warmth of the result, so it matters more than any setting.

**Hard rule:** never use the ElevenLabs Cillian sample, or any ElevenLabs output, as a reference. Their terms forbid it, and their library voices belong to real actors. If the user asks to do this, decline and offer the options below.

### Option A: record a consenting speaker (best)

1. Find an Irish speaker who agrees to have their voice cloned for this use.
2. Open QuickTime Player, then choose File > New Audio Recording.
3. Record 10 to 20 seconds of them reading calm narration (slow, relaxed, low in their range, in a quiet room), then save it.
4. Convert it to the format Chatterbox expects (run this from `~/tts`):

```bash
ffmpeg -i ~/Desktop/Untitled.m4a -ac 1 -ar 24000 ref.wav
```

Tell the user to replace `~/Desktop/Untitled.m4a` with the real path of their file. Dragging the file from Finder into Terminal pastes its path. If ffmpeg says "No such file or directory", the path is wrong.

### Option B: the VCTK corpus

The VCTK corpus is free under CC BY 4.0 (credit is required if the output is shared): https://datashare.ed.ac.uk/handle/10283/3443

Irish male speakers in it:

- p245 (Dublin)
- p298 (Tipperary)
- p364 (Donegal)

They are aged 19 to 25, so they sound lighter than a deep, mature narrator. Pick one clip of 10 to 20 seconds and convert it with the same ffmpeg command, using that file's path.

### Option C: no clip yet

To test the install before a clip is ready, remove the `audio_prompt_path` line from `speak.py` in step 6. Chatterbox then uses its default voice.

## 6. Generate speech

Copy the bundled script `scripts/speak.py` (in this skill's folder) to `~/tts/speak.py`. If the skill is installed at `~/.claude/skills/riish`, the user can run:

```bash
cp ~/.claude/skills/riish/scripts/speak.py ~/tts/speak.py
```

If the skill lives elsewhere (for example, installed as a plugin), use that path, or write the file for the user with the script's exact contents.

With `(cb)` showing and inside `~/tts`, run:

```bash
python speak.py
```

The first run downloads about 1 to 2 GB of model weights, so it is slow. Later runs are much faster. Then play the result:

```bash
open out.wav
```

To narrate their own text, change the `text = "..."` line in `speak.py`.

## 7. Tuning

Both settings are in the `model.generate(...)` call in `speak.py`:

- `exaggeration` (try 0.3 to 0.7): lower is calmer and flatter, higher is more expressive. For a calm narrator, stay near 0.3 to 0.4.
- `cfg_weight`: lower gives slower, more relaxed pacing.

Change one value at a time and listen, because each affects the other.

For long text, split it into chunks under about 300 characters (at sentence ends), generate each chunk, and join the audio with `torch.cat` on the last dimension before saving. Long single inputs tend to drift or rush. If the user wants this, write a small loop into `speak.py` for them.

## 8. Troubleshooting

- `python3.11: command not found`: Homebrew is not on the PATH. Run the fallback `eval "$(/opt/homebrew/bin/brew shellenv)"` from step 1, then try again.
- `pip: command not found` (or packages "missing" that were installed): the virtual environment is not active. Run `cd ~/tts && source cb/bin/activate` and check for `(cb)`.
- An error mentioning MPS: Apple GPU support failed for this operation. In `speak.py`, change the device line to `device = "cpu"`. It is slower but reliable.
- Two commands pasted onto one line (for example, `brew install python@3.11brew install ffmpeg`): run each command separately, one per line.

## 9. Alternatives

Mention these only if Chatterbox does not suit the user.

- **Qwen3-TTS VoiceDesign** (Apache 2.0): describes a voice from a text prompt instead of cloning a clip. Its docs assume an NVIDIA GPU, and whether it can produce a convincing Irish accent is unverified.
- **Kokoro-82M** (Apache 2.0): small and runs on CPU, but has no cloning, and its only British male voices are `bm_george` and `bm_fable`. No Irish voice.
- **Piper, en_GB vctk model**: includes the VCTK Irish speakers listed above. Fast and light, but more robotic.

Do not recommend F5-TTS, XTTS v2, Fish Audio or Voxtral for this: their licences are non-commercial, or the project is dead.

## 10. Caveat about "Cillian"

ElevenLabs' own pages do not confirm that the Cillian voice is Irish-accented. Third-party listings describe it as "deep, warm and calm". Treat "like Cillian" as a target tone (deep, warm, calm) and let the user's consented reference clip supply the Irish accent.
