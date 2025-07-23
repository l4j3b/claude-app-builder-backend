FROM python:3.11-slim AS python-builder

WORKDIR /build

# Install Claude Python deps
COPY code_api/requirements.txt ./code_api/requirements.txt
RUN pip install --upgrade pip && \
    pip install --prefix=/python-packages -r code_api/requirements.txt

COPY code_api/ ./code_api/


FROM node:20-slim

COPY --from=python-builder /python-packages /usr/local
COPY --from=python-builder /build/code_api /app/code_api

WORKDIR /app

COPY next_app/ ./next_app
COPY start_servers.sh ./
COPY proxy_server.js ./

# Install Node tooling, Claude CLI, and reverse proxy dependencies
ENV CI=true
RUN npm install -g pnpm @anthropic-ai/claude-code && \
    npm install express http-proxy-middleware && \
    cd next_app && pnpm install

EXPOSE 3000

CMD ["node", "proxy_server.js"]