Script to create a GitHub repository for this project and push the local `main` branch.

Usage:

1. Export your Personal Access Token (PAT) with `repo` scope into `GITHUB_TOKEN`.

```bash
export GITHUB_TOKEN=your_token_here
./scripts/create_and_push_repo.sh [repo-name]
```

If `[repo-name]` is omitted it defaults to `skill-adk`. The script will:
- determine the authenticated GitHub username
- create the repository under that account
- add the `origin` remote pointing to the new repo
- push the local `main` branch

Security: Never paste tokens into chat. Keep `GITHUB_TOKEN` private and revoke it if compromised.