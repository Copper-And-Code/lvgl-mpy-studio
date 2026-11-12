#!/usr/bin/env bash
set -euo pipefail

ROOT=$(git rev-parse --show-toplevel)
cd "$ROOT"

if [[ ! -f build/site/index.html || ! -f build/site/.nojekyll ]]; then
    echo "Build the site first with .venv/bin/python tools/build_site.py" >&2
    exit 1
fi

TEMP=$(mktemp -d)
trap 'rm -rf "$TEMP"' EXIT
mkdir "$TEMP/tree"
cp -a build/site/. "$TEMP/tree/"
export GIT_INDEX_FILE="$TEMP/index"
export GIT_WORK_TREE="$TEMP/tree"

if git show-ref --verify --quiet refs/heads/gh-pages; then
    git read-tree gh-pages
else
    git read-tree --empty
fi
git add --all -- .
TREE=$(git write-tree)
PARENTS=()
if git show-ref --verify --quiet refs/heads/gh-pages; then
    PARENTS=(-p gh-pages)
fi
COMMIT=$(git commit-tree "$TREE" "${PARENTS[@]}" -m "Publish the project site" -m "Co-Authored-By: Claude <noreply@anthropic.com>")
git update-ref refs/heads/gh-pages "$COMMIT"

printf 'Prepared local gh-pages commit %s\n' "$COMMIT"
printf 'Nothing was pushed. After explicit owner approval, run:\n'
printf '  git push origin gh-pages:gh-pages\n'
