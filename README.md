# Space-game-fucking-around
# Space-game-fucking-around


1. Create a New Branch

# Create and switch to a new branch from current main
git checkout -b new-branch-name

# Or create branch without switching immediately
git branch new-branch-name
git checkout new-branch-name

2. Create a Worktree (Isolated Working Directory)

# Add a new worktree linked to a branch
git worktree add ../path/to/worktree new-branch-name

# Example: create worktree for new feature in sibling directory
git worktree add ../space_game-feature feature/login-system

# List all worktrees
git worktree list

# Remove worktree when done (after committing or stashing changes)
git worktree remove ../path/to/worktree

git checkout main