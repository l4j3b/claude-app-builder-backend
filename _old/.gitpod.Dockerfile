FROM gitpod/workspace-full:latest

# Install pnpm
RUN npm install -g pnpm

# Install Python dependencies
RUN pip3 install --user pipenv

# Install Claude CLI globally
RUN npm install -g @anthropic-ai/claude-code

# Optionally verify it's installed
RUN claude --help || true

WORKDIR /workspace