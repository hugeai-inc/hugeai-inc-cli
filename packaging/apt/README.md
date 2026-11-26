# apt repository for hugeai-inc-cli

`.deb` packages for `linux/amd64` and `linux/arm64` are built by GoReleaser
(`nfpms:` in `.goreleaser.yaml`) and by `packaging/nfpm.yaml` on each tagged
release, and attached to the GitHub Release.

Until a GitHub Pages apt repository is published, install a downloaded
package directly:

```sh
# Replace VERSION and ARCH (amd64 or arm64).
curl -fsSLO "https://github.com/hugeai-inc/hugeai-inc-cli/releases/download/vVERSION/hugeai-inc-cli_VERSION_ARCH.deb"
sudo apt install ./hugeai-inc-cli_VERSION_ARCH.deb
```

## Planned GitHub Pages apt repo

Once a signing key and Pages site are provisioned (this is the hook the
release workflow refers to), the repository will be served from GitHub
Pages on this project, and users will be able to install with:

```sh
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://hugeai-inc.github.io/hugeai-inc-cli/apt/gpg.key \
  | sudo gpg --dearmor -o /etc/apt/keyrings/hugeai-inc.gpg
echo "deb [signed-by=/etc/apt/keyrings/hugeai-inc.gpg] https://hugeai-inc.github.io/hugeai-inc-cli/apt stable main" \
  | sudo tee /etc/apt/sources.list.d/hugeai-inc.list
sudo apt update
sudo apt install hugeai-inc-cli
```

A sketched publisher lives at `packaging/apt/publish.sh`. Uncomment the
`apt-pages` job in `.github/workflows/release.yml` and set the
`APT_PAGES_TOKEN` repository secret (a token that can push to the Pages
branch) when you are ready to turn this on. The job should:

1. Download the `.deb` assets from the GitHub Release just published.
2. Import them into a reprepro, aptly, or similar repo on the `gh-pages`
   branch (or a `apt` folder published as GitHub Pages).
3. Sign `InRelease` / `Release.gpg` with the apt signing key (stored as
   a repository secret, never committed).
4. Push the updated repo so `apt update` sees the new version.

Do not commit private signing keys or tokens to this repository.
