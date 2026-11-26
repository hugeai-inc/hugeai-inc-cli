#!/usr/bin/env bash
# Sketch: publish .deb assets from a GitHub Release into the GitHub Pages
# apt repository. This is an outline, not a complete publisher — wire it
# to reprepro/aptly and uncomment the apt-pages job in
# .github/workflows/release.yml when the Pages site and signing key exist.
set -euo pipefail

echo "not yet implemented: packaging/apt/publish.sh" >&2
echo "See packaging/apt/README.md for the intended flow." >&2
exit 1
