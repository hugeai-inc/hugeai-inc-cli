// Command hugeai-inc-cli is the Huge AI Inc board-resolution CLI.
//
// This first commit is a compilable stub only: command outlines and
// "not yet implemented" handlers, with no Supabase client and no
// real cryptographic signing logic yet.
package main

import (
	"os"

	"github.com/hugeai-inc/hugeai-inc-cli/internal/cli"
)

// Set at link time by GoReleaser and the CI cross-compile job:
//
//	-X main.version=...
//	-X main.commit=...
//	-X main.date=...
var (
	version = "0.0.0-dev"
	commit  = "unknown"
	date    = "unknown"
)

func main() {
	os.Exit(cli.Run(os.Args, os.Stdout, os.Stderr, cli.BuildInfo{
		Version: version,
		Commit:  commit,
		Date:    date,
	}))
}
