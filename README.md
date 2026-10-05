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

# Game Development To-Do List

1. **Add Sound**
   pathfinder do * Add sound effects for shooting, enemies, abilities, power-ups, damage, etc.
   pathfinder do * Add background music.

2. **Redesign HUD**
   pathfinder do * Improve the overall HUD layout and appearance.

1) **Wave System / Wave Base Logic**
   pathfinder do * Create the core wave system.
   pathfinder do * Add boss waves.
   pathfinder do * Create scaling difficulty as the player progresses.
   pathfinder do * Add wave completion and transition logic.

2) **Power-Up Selection Screen**
   pathfinder do * Create a screen that appears when the player earns a power-up/stats.
   pathfinder do * Give the player 3 choices.
   pathfinder do * Allow the player to select one upgrade.
   pathfinder do * Apply the selected upgrade to the player.
   pathfinder do * Resume gameplay after the selection.

3) **Power-Up / Ability HUD Slots**
   pathfinder do * Add power-up/ability slots above the HP bar.
   pathfinder do * Use **Q, E, and F** as the ability/power-up keys.
   pathfinder do * Display the currently equipped ability or power-up in each slot.
   pathfinder do * Show cooldowns or charges.
   pathfinder do * Make the slots update when the player changes abilities.

4) **Stats / Stat Selection System**
   pathfinder do * Create a player stats system.
   pathfinder do * Decide which stats can be upgraded.
   pathfinder do * Add stat changes to the power-up/selection screen.
   pathfinder do * Allow the player to choose which stat they want to improve.
   pathfinder do * Consider stats such as:
     * Health
     * Damage
     * Attack speed
     * Movement speed
     * Ability cooldown

5) **Enemies and Bosses**
kadian have fun 

