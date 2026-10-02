import os
from pathlib import Path
from anthropic import Anthropic

SESSION_ID = "sesn_01La9WpF87MdpJBMrhde5Ysz"  # paste your session ID here

client = Anthropic(
    default_headers={"anthropic-workspace-id": os.environ["ANTHROPIC_WORKSPACE_ID"]}
)

# Local folder to save the files into
out_dir = Path(__file__).parent / "outputs"
out_dir.mkdir(exist_ok=True)

# List the files the agent saved in this session
files = client.beta.files.list(
    scope_id=SESSION_ID,
    betas=["managed-agents-2026-04-01"],
)

for f in files.data:
    print(f"Downloading {f.filename} ...")
    content = client.beta.files.download(f.id)
    content.write_to_file(out_dir / f.filename)

print(f"Done. Files saved to {out_dir}")