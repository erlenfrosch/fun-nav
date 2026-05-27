#!/usr/bin/env bash
set -euo pipefail
cd /home/erlenfrosch/repos/fun-nav

echo "=== 1. main squashen zu einem sauberen Root-Commit ==="
git checkout main

TREE=$(git rev-parse HEAD^{tree})
MSG="chore: initialer Projekt-Setup

Projektgrundlage: CLAUDE.md, AGENTS.md, .mcp.json, .forgecrate.yaml,
.claude/ (hooks, settings, skills) und memory-bank/ Grundstruktur.

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>"

NEW_MAIN=$(git commit-tree "$TREE" -m "$MSG")
git reset --hard "$NEW_MAIN"
echo "Neuer main: $(git log --oneline)"

echo ""
echo "=== 2. docs/runden-modus-spec neu von main ableiten ==="
git branch -D docs/runden-modus-spec 2>/dev/null || true
git checkout -b docs/runden-modus-spec

# Spec und Scripts aus dem alten Feature-Branch holen
git checkout 8d9ba6c -- docs/ scripts/ 2>/dev/null || true

# pr-body.md (Hilfsdatei) nicht mit committen
rm -f scripts/pr-body.md

echo ""
echo "=== 3. Gestaged ==="
git status --short

echo ""
echo "=== 4. Spec-Commit erstellen ==="
git add docs/ scripts/
git commit -m "docs: Runden-Modus Design Spec und GitHub Backlog Scripts

- Design Spec in docs/superpowers/specs/ (Architektur, Tech-Stack,
  Rundrouten-Algorithmus, User Flow)
- Scripts zum Erstellen des GitHub Backlogs
- Issue-Body-Dateien fuer alle 15 GitHub Issues

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>"

echo ""
echo "=== 5. Ergebnis ==="
git log --oneline --graph --all
