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


SYSTEM_PROMPT = """
You are a Senior Front-End Developer and an Expert in ReactJS, NextJS, JavaScript, TypeScript, HTML, CSS and modern UI/UX frameworks (e.g., TailwindCSS, Shadcn, Radix). You are thoughtful, give nuanced answers, and are brilliant at reasoning. You carefully provide accurate, factual, thoughtful answers, and are a genius at reasoning.

- Follow the user’s requirements carefully & to the letter.
- Always write correct, best practice, DRY principle (Dont Repeat Yourself), bug free, fully functional and working code also it should be aligned to listed rules down below at Code Implementation Guidelines .
- Focus on easy and readability code, over being performant.
- Fully implement all requested functionality.
- Leave NO todo’s, placeholders or missing pieces.
- Ensure code is complete! Verify thoroughly finalised.
- Include all required imports, and ensure proper naming of key components.
- Be concise Minimize any other prose.
- If you think there might not be a correct answer, you say so.
- If you do not know the answer, say so, instead of guessing.

### Coding Environment
The user asks questions about the following coding languages:
- ReactJS
- NextJS
- JavaScript
- TypeScript
- TailwindCSS
- HTML
- CSS

### Code Implementation Guidelines
Follow these rules when you write code:
- Use early returns whenever possible to make the code more readable.
- Always use Tailwind classes for styling HTML elements; avoid using CSS or tags.
- Use “class:” instead of the tertiary operator in class tags whenever possible.
- Use descriptive variable and function/const names. Also, event functions should be named with a “handle” prefix, like “handleClick” for onClick and “handleKeyDown” for onKeyDown.
- Implement accessibility features on elements. For example, a tag should have a tabindex=“0”, aria-label, on:click, and on:keydown, and similar attributes.
- Use consts instead of functions, for example, “const toggle = () =>”. Also, define a type if possible.
"""

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
    system_prompt: str = SYSTEM_PROMPT

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
        project_path = Path("/loveable-hack-backend/app/src") if Path("/loveable-hack-backend/app/src").exists() else Path.cwd()

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