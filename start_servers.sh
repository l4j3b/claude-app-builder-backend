#!/bin/bash
# Start both Next.js and Claude Code servers

echo "Starting Claude Code Server on port 8000..."
cd code_api && python3 claude_server.py &
CLAUDE_PID=$!

echo "Starting Next.js development server on port 3000..."
cd app && npm run dev &
NEXTJS_PID=$!

echo "Both servers started!"
echo "Claude Code Server PID: $CLAUDE_PID"
echo "Next.js Server PID: $NEXTJS_PID"
echo ""
echo "URLs:"
echo "- Next.js: http://localhost:3000"
echo "- Claude Code API: http://localhost:8000"
echo "- Claude Code Health: http://localhost:8000/claude/health"
echo ""
echo "Press Ctrl+C to stop both servers"

# Wait for user interrupt
trap "kill $CLAUDE_PID $NEXTJS_PID; exit" INT
wait