#!/usr/bin/bash

tmux kill-session
cd /home/mlh-portfolio/
git fetch && git reset origin/main --hard
source venv/bin/activate
pip install -r requirements.txt
tmux new-session -d "flask run --host=0.0.0.0"