FROM python:3.11-slim

WORKDIR /app

COPY next_app/ ./next_app
COPY code_api/ ./code_api
COPY start_servers.sh ./
COPY proxy_server.js ./

# Set CI environment for faster npm installs
ENV CI=true

# Install Node.js 20 and system dependencies
RUN apt-get update && apt-get install -y curl && \
    curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y nodejs

# Install Python dependencies for Claude API
RUN pip install --no-cache-dir -r code_api/requirements.txt

# Install Node.js global tools
RUN npm install -g pnpm @anthropic-ai/claude-code

# Install proxy server dependencies
RUN npm install express http-proxy-middleware

# Install Next.js app dependencies
RUN cd next_app && pnpm install

EXPOSE 3000

CMD ["bash", "start_servers.sh"]