# Claude POC

This repo is a simple POC for using Claude CLI in Gitpod.

## How to use

1. Click "Open in Gitpod"
2. Wait for workspace to start.
3. Terminal runs `npm install && npm run dev` automatically.
4. Live preview opens on port 5173.
5. In terminal, run:

   ```bash
   claude -p "update the app title to say hello world" --dangerously-skip-permissions
   ```

6. See `src/App.js` update live.
7. Hot reload updates preview.

[![Open in Gitpod](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io/#https://github.com/l4j3b/claude-poc)

## Requirements

- Add your `ANTHROPIC_API_KEY` as a Gitpod Environment Variable.
