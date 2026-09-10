#!/usr/bin/env bash
# Copy every skill into a destination directory, refusing to overwrite what is already there.
#
# WHY THIS EXISTS. The README used to put a bare `cp -R skills/* "$DEST/"` on its first
# screen while teaching an existence check further down the same page. Two of these skill
# names are ordinary enough that a researcher may already have their own -- and unlike a
# plugin install, which namespaces every skill under the plugin, copying a directory has no
# namespace at all. The bare copy silently replaced the user's own SKILL.md and left their
# other files behind, producing a half-merged skill that looks installed and is not.
#
#   bash scripts/install_skills.sh "$HOME/.agents/skills"     # Codex, Antigravity CLI
#   bash scripts/install_skills.sh "$HOME/.claude/skills"     # Claude Code, without the plugin
#   bash scripts/install_skills.sh "$DEST" --force            # deliberately replace
set -eu

DEST="${1:-}"
FORCE="${2:-}"
if [ -z "$DEST" ]; then
  echo "usage: bash scripts/install_skills.sh <destination-directory> [--force]" >&2
  exit 2
fi

HERE="$(cd "$(dirname "$0")/.." && pwd)"
if [ ! -d "$HERE/skills" ]; then
  echo "no skills/ directory beside this script; run it from inside the repository" >&2
  exit 2
fi

mkdir -p "$DEST"
installed=0
skipped=0

for source in "$HERE"/skills/*/; do
  name="$(basename "$source")"
  target="$DEST/$name"
  if { [ -e "$target" ] || [ -L "$target" ]; } && [ "$FORCE" != "--force" ]; then
    echo "SKIP  $name  (already at $target; pass --force to replace, or move yours aside first)"
    skipped=$((skipped + 1))
    continue
  fi
  # Replace rather than merge. Copying over an existing directory leaves the previous
  # version's extra files in place, which is how a half-merged skill happens.
  if [ -e "$target" ] || [ -L "$target" ]; then
    rm -r -- "$target"
  fi
  cp -R "$source" "$target"
  installed=$((installed + 1))
done

echo "installed=$installed skipped=$skipped dest=$DEST"
if [ "$skipped" -gt 0 ]; then
  echo "Nothing of yours was overwritten. Re-run with --force once you have compared them."
fi
