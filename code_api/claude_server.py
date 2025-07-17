#!/usr/bin/env python3
"""
Claude Code SDK Server
Exposes an endpoint for Claude to modify code in your Gitpod workspace
"""

import os
import asyncio
import json
from pathlib import Path
from typing import Any, List
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from claude_code_sdk import query, ClaudeCodeOptions

app = FastAPI(title="Claude Code Server", version="1.0.0")

# Enable CORS for Gitpod and local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Local Next.js dev server
        "https://*.gitpod.io",    # Gitpod workspace URLs
        "https://3000-*-*.gitpod.io",  # Gitpod Next.js port
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ClaudeRequest(BaseModel):
    prompt: str
    max_turns: int = 10
    system_prompt: str = "You are a helpful coding assistant. Follow the user's instructions carefully."

class ClaudeResponse(BaseModel):
    messages: List[Any]
    status: str

@app.post("/claude", response_model=ClaudeResponse)
async def claude_endpoint(request: ClaudeRequest):
    """
    Expose Claude Code SDK with proper permissions for code modification
    """
    try:
        # Get the workspace directory (Gitpod uses /workspace)
        project_path = Path("/workspace/claude-poc/src") if Path("/workspace/claude-poc/src").exists() else Path.cwd()

        print(f"Request received: {request.prompt}")
        print(f"Project path: {project_path}")

        # Configure Claude Code options
        options = ClaudeCodeOptions(
            max_turns=request.max_turns,
            system_prompt=request.system_prompt,
            cwd=project_path,
            allowed_tools=["Read", "Write", "Edit", "Bash", "Glob", "Grep", "LS"],
            permission_mode="acceptEdits",
            model="claude-3-5-sonnet-20241022"
        )

        messages = []

        # Query Claude with streaming response
        async for message in query(prompt=request.prompt, options=options):
            # Convert message to dict for JSON serialization
            message_dict = {
                "type": type(message).__name__,
                "content": str(message.content) if hasattr(message, 'content') else str(message),
                "subtype": getattr(message, 'subtype', None)
            }

            print(f"Message received: {message_dict}")
            messages.append(message_dict)

        return ClaudeResponse(messages=messages, status="success")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/claude/stream")
async def claude_stream(request: ClaudeRequest):
    """
    Streaming endpoint for Claude Code SDK responses
    """
    async def generate():
        try:
            # Get the workspace directory (Gitpod uses /workspace)
            project_path = Path("/workspace/claude-poc") if Path("/workspace/claude-poc").exists() else Path.cwd()

            print(f"Stream request received: {request.prompt}")
            print(f"Project path: {project_path}")

            # Configure Claude Code options
            options = ClaudeCodeOptions(
                max_turns=request.max_turns,
                system_prompt=request.system_prompt,
                cwd=project_path,
                allowed_tools=["Read", "Write", "Edit", "Bash", "Glob", "Grep", "LS"],
                permission_mode="acceptEdits",
                model="claude-3-5-sonnet-20241022"
            )

            # Stream each message as it arrives
            async for message in query(prompt=request.prompt, options=options):
                # Convert message to dict for JSON serialization
                message_dict = {
                    "type": type(message).__name__,
                    "content": str(message.content) if hasattr(message, 'content') else str(message),
                    "subtype": getattr(message, 'subtype', None)
                }

                print(f"Streaming message: {message_dict}")
                yield f"data: {json.dumps(message_dict)}\n\n"

        except Exception as e:
            error_dict = {"error": str(e)}
            yield f"data: {json.dumps(error_dict)}\n\n"

        # Signal end of stream
        yield "data: [DONE]\n\n"

    return StreamingResponse(generate(), media_type="text/plain")

@app.get("/claude/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "cwd": str(Path.cwd())}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)