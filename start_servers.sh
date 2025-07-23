# # Start both Next.js and Claude Code servers

# echo "Starting Next.js development server on port 3000..."
# cd /app/next_app && pnpm dev --port 3000 &

# echo "Starting Claude Code Server on port 8000..."
# cd /app/code_api && python3 server.py &
# CLAUDE_PID=$!

# NEXTJS_PID=$!

# echo "Both servers started!"
# echo "Claude Code Server PID: $CLAUDE_PID"
# echo "Next.js Server PID: $NEXTJS_PID"
# echo ""
# echo "URLs:"
# echo "- Next.js: http://localhost:3000"
# echo "- Claude Code API: http://localhost:8000"
# echo "- Claude Code Health: http://localhost:8000/claude/health"
# echo ""
# echo "Press Ctrl+C to stop both servers"

# # Wait for user interrupt
# trap "kill $CLAUDE_PID $NEXTJS_PID; exit" INT
# wait

#!/bin/bash

echo "Starting Python API on port 8000..."
cd /app/code_api && python3 server.py &
CLAUDE_PID=$!

echo "Starting Next.js app on port 3001..."
cd /app/next_app && pnpm dev --port 3001 &
NEXTJS_PID=$!

echo "Waiting for services to start..."
sleep 5

echo "Checking if services are running..."
curl -f http://localhost:8000/code/health || echo "Python API not responding on port 8000"
curl -f http://localhost:3001 || echo "Next.js app not responding on port 3001"

echo "Starting proxy server on port 3000..."
node /app/proxy_server.js &
PROXY_PID=$!

trap "kill $CLAUDE_PID $NEXTJS_PID $PROXY_PID" INT
wait
