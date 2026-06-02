#!/usr/bin/env bash
set -euo pipefail

# Usage: GITHUB_TOKEN=... ./scripts/create_and_push_repo.sh [repo-name]
# Defaults to repo-name "skill-adk" if not provided.

TOKEN=${GITHUB_TOKEN:-}
if [ -z "$TOKEN" ]; then
  echo "Error: set GITHUB_TOKEN environment variable with a Personal Access Token (repo scope)"
  exit 1
fi

REPO=${1:-skill-adk}

# get authenticated user login
LOGIN=$(curl -s -H "Authorization: token $TOKEN" https://api.github.com/user | python3 -c "import sys,json; print(json.load(sys.stdin).get('login',''))")
if [ -z "$LOGIN" ]; then
  echo "Error: could not determine GitHub login. Check your token." >&2
  curl -s -H "Authorization: token $TOKEN" https://api.github.com/user
  exit 1
fi

echo "Authenticated as: $LOGIN"

# Create repository
resp=$(curl -s -o /dev/stderr -w "%{http_code}" -H "Authorization: token $TOKEN" \
  -d "{\"name\": \"$REPO\", \"private\": false}" \
  https://api.github.com/user/repos) || true

# If curl wrote HTTP code to stdout we still continue. Check repo existence by attempting to form remote URL.
REMOTE_URL="https://github.com/$LOGIN/$REPO.git"

echo "Setting remote to $REMOTE_URL"

# Configure git remote and push
cd "$(git rev-parse --show-toplevel)" || cd .

# Remove existing origin if present
if git remote get-url origin >/dev/null 2>&1; then
  git remote remove origin
fi

git remote add origin "$REMOTE_URL"

echo "Pushing branch 'main' to origin..."

git push -u origin main

echo "Done. Repository: https://github.com/$LOGIN/$REPO"
