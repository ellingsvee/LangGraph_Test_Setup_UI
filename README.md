## Installation
I use [uv](https://docs.astral.sh/uv/) to set up to python package
```bash
# Create viritual environment
uv venv
source .venv/bin/activate

# Install packages
uv sync
```
Then set up the UI by
```bash
cd src/ui
pnpm install
cd ../..
```
Launch the LangGraph CLI by
```bash
langgraph dev
```
and navigate to the [Agent Chat UI](https://agentchat.vercel.app/)!
