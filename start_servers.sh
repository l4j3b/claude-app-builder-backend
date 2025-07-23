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

cd /app/code_api && python3 server.py &
CLAUDE_PID=$!

cd /app/next_app && pnpm dev --port 3000 &
NEXTJS_PID=$!

trap "kill $CLAUDE_PID $NEXTJS_PID" INT
wait
