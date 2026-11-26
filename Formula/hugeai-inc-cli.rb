# Homebrew formula scaffold for hugeai-inc-cli.
# Prebuilt binaries; not built from source once a tagged release exists.
#
#   brew tap hugeai-inc/tap
#   brew install hugeai-inc-cli
#
# The tap repository is hugeai-inc/homebrew-tap (Homebrew's "hugeai-inc/tap").
# Archives are published on hugeai-inc/hugeai-inc-cli GitHub Releases.
# GoReleaser (brews: in .goreleaser.yaml) updates the copy of this formula
# in the tap on each tagged release, filling in url and sha256 per platform.
class HugeaiIncCli < Formula
  desc "CLI for Huge AI Inc board resolutions, meetings, and director identity keys"
  homepage "https://github.com/hugeai-inc/hugeai-inc-cli"
  version "0.0.0"
  license "MIT"

  # Until the first tagged release, install from the main branch:
  #
  #   brew install --HEAD hugeai-inc/tap/hugeai-inc-cli
  #
  # After v0.1.0 (and later) GoReleaser replaces the `head` block below
  # with on_macos / on_linux url and sha256 entries pointing at:
  #   https://github.com/hugeai-inc/hugeai-inc-cli/releases/download/vVERSION/hugeai-inc-cli_VERSION_OS_ARCH.tar.gz
  head "https://github.com/hugeai-inc/hugeai-inc-cli.git", branch: "main"

  depends_on "go" => :build if build.head?

  def install
    if build.head?
      ldflags = %W[
        -s -w
        -X main.version=HEAD
        -X main.commit=#{Utils.git_head}
      ]
      system "go", "build", *std_go_args(ldflags: ldflags), "./cmd/hugeai-inc-cli"
    else
      bin.install "hugeai-inc-cli"
    end
  end

  test do
    assert_match "hugeai-inc-cli", shell_output("#{bin}/hugeai-inc-cli version")
  end
end
