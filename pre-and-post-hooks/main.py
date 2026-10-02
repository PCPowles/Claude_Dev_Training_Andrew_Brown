"""Demo: PreToolUse and PostToolUse hooks with the Claude Agent SDK.

Setup:
    pip install claude-agent-sdk
    # Requires the Claude Code CLI available on PATH (the SDK shells out to it).

Run:
    python main.py
"""

import asyncio

from claude_agent_sdk import ClaudeAgentOptions, HookMatcher, query


async def pre_tool_use_hook(input_data, tool_use_id, context):
    tool = input_data["tool_name"]
    print(f"[PRE]  {tool} id={tool_use_id}")
    print(f"       input={input_data['tool_input']}")
    return {}


async def post_tool_use_hook(input_data, tool_use_id, context):
    tool = input_data["tool_name"]
    print(f"[POST] {tool} id={tool_use_id}")
    print(f"       response={input_data['tool_response']}")
    return {}


async def block_dangerous_bash(input_data, tool_use_id, context):
    cmd = input_data["tool_input"].get("command", "")
    if "rm -rf" in cmd:
        print(f"[BLOCK] refusing dangerous command: {cmd!r}")
        return {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "deny",
                "permissionDecisionReason": "rm -rf is blocked by policy",
            }
        }
    return {}


async def main():
    options = ClaudeAgentOptions(
        allowed_tools=["Bash", "Write", "Read"],
        hooks={
            "PreToolUse": [
                HookMatcher(matcher=None, hooks=[pre_tool_use_hook]),
                HookMatcher(matcher="Bash", hooks=[block_dangerous_bash]),
            ],
            "PostToolUse": [
                HookMatcher(matcher=None, hooks=[post_tool_use_hook]),
            ],
        },
    )

    prompt = "Run `echo hello from hooks` with Bash, then tell me what you saw."

    async for message in query(prompt=prompt, options=options):
        print(message)


if __name__ == "__main__":
    asyncio.run(main())