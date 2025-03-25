set windows-shell := ['pwsh.exe', '-MTA', '-NoLogo', '-NoProfile', '-Command']

default: run

run:
  uv run --env-file .env -m src

test:
  uv run --env-file .env pytest
