# riish

A Claude Code skill that walks you through setting up a free, local text-to-speech narrator voice on a Mac (a warm, calm, low Irish male voice) with Chatterbox and a consented reference clip.

## Install locally

Copy the skill folder into your personal skills directory:

```bash
mkdir -p ~/.claude/skills && cp -r <path-to>/riish ~/.claude/skills/riish
```

Replace `<path-to>` with the folder that contains this `riish` directory (in this repo, `riish/skills`).

## Install via the plugin

This repo is a plugin marketplace, and the skill also ships as the `riish` plugin. In Claude Code:

```
/plugin marketplace add <path-to-this-repo-or-its-git-url>
/plugin install riish@knowledge-work-plugins
```

Then ask Claude something like "set up a free local Irish narrator voice on my Mac".
