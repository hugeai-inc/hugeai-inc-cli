// Package cli implements the hugeai-inc-cli command tree.
//
// All subcommands below the version and help commands are stubs: they
// print a short outline of the intended behaviour and return
// "not yet implemented". There is no Supabase client and no real
// cryptographic signing in this commit.
package cli

import (
	"fmt"
	"io"
	"strings"
)

// BuildInfo is the version metadata stamped into the binary at link time.
type BuildInfo struct {
	Version string
	Commit  string
	Date    string
}

const notImplemented = "not yet implemented"

// Run dispatches argv (including the program name in args[0]) and returns
// a process exit code. Exit 0 is success (including stubs and help);
// exit 2 is a usage or unknown-command error.
func Run(args []string, stdout, stderr io.Writer, info BuildInfo) int {
	name := "hugeai-inc-cli"
	if len(args) > 0 && args[0] != "" {
		name = args[0]
	}
	argv := []string{}
	if len(args) > 1 {
		argv = args[1:]
	}

	if len(argv) == 0 || isHelp(argv[0]) {
		writeRootHelp(stdout, name)
		return 0
	}

	switch argv[0] {
	case "version", "--version", "-v":
		return runVersion(stdout, info)
	case "help":
		writeRootHelp(stdout, name)
		return 0
	case "resolution":
		return runGroup(stdout, stderr, name, "resolution", argv[1:], resolutionCommands)
	case "meeting":
		return runGroup(stdout, stderr, name, "meeting", argv[1:], meetingCommands)
	case "keys":
		return runGroup(stdout, stderr, name, "keys", argv[1:], keysCommands)
	default:
		fmt.Fprintf(stderr, "unknown command: %s\n\n", argv[0])
		writeRootHelp(stderr, name)
		return 2
	}
}

func runVersion(stdout io.Writer, info BuildInfo) int {
	fmt.Fprintf(stdout, "hugeai-inc-cli %s\n", info.Version)
	if info.Commit != "" && info.Commit != "unknown" {
		fmt.Fprintf(stdout, "commit: %s\n", info.Commit)
	}
	if info.Date != "" && info.Date != "unknown" {
		fmt.Fprintf(stdout, "built:  %s\n", info.Date)
	}
	return 0
}

type stub struct {
	name    string
	summary string
	outline string
	aliases []string
}

func (s stub) matches(name string) bool {
	if s.name == name {
		return true
	}
	for _, a := range s.aliases {
		if a == name {
			return true
		}
	}
	return false
}

// resolutionCommands is the sketched board-resolution command set.
//
//	resolution draft   — draft a new board resolution
//	resolution revise  — create a new revision linked via supersedes_id
//	resolution sign    — cryptographically sign and submit a vote
//	resolution tally   — check vote tally and 2-of-3 majority status
//	resolution list    — list board resolutions by status/type
//	resolution verify  — verify cryptographic signatures and content hash
var resolutionCommands = []stub{
	{
		name:    "draft",
		summary: "Draft a new board resolution",
		outline: strings.TrimSpace(`
Outline — resolution draft
  Create a draft board resolution with a sequential resolution number,
  title, resolution_type (general | ceo_removal | key_recovery),
  canonical markdown body, optional meeting_id, and threshold (default 2 of 3).
  Opening the draft for signature will compute a SHA-256 content_hash and
  lock the text (edits after that create a new revision).

  Flags (planned, not wired):
    --title string
    --type general|ceo_removal|key_recovery
    --body-file path
    --meeting-id string
    --threshold 2
`),
	},
	{
		name:    "revise",
		summary: "Create a new revision linked via supersedes_id",
		outline: strings.TrimSpace(`
Outline — resolution revise
  Create a new immutable revision of an existing resolution. The new
  record points at the previous one via supersedes_id; the prior text
  stays locked. A fresh content_hash is computed when the revision is
  opened for signature.

  Flags (planned, not wired):
    --id string          resolution to supersede
    --title string
    --body-file path
`),
	},
	{
		name:    "sign",
		summary: "Sign and submit a vote (approve|reject|abstain|recused)",
		outline: strings.TrimSpace(`
Outline — resolution sign
  Sign a canonical JSON payload with the director's Ed25519 identity key
  and submit it for verification (no direct table writes):
    {resolution_id, content_hash, vote, member_id, key_id, timestamp}
  Votes: approve | reject | abstain | recused.
  Private keys never enter the server. Real signing is not implemented yet.

  Flags (planned, not wired):
    --id string
    --vote approve|reject|abstain|recused
    --key-id string
`),
	},
	{
		name:    "tally",
		summary: "Check vote tally and 2-of-3 majority status",
		outline: strings.TrimSpace(`
Outline — resolution tally
  Count verified attestations from distinct active directors against the
  resolution threshold (default 2 of 3). Two approve votes mark the
  resolution adopted (including ceo_removal and key_recovery); two reject
  votes mark it rejected.

  Flags (planned, not wired):
    --id string
`),
	},
	{
		name:    "list",
		summary: "List board resolutions by status or type",
		outline: strings.TrimSpace(`
Outline — resolution list
  List resolutions filtered by status (draft | open_for_signature |
  adopted | rejected) and/or resolution_type.

  Flags (planned, not wired):
    --status draft|open_for_signature|adopted|rejected
    --type general|ceo_removal|key_recovery
`),
	},
	{
		name:    "verify",
		summary: "Verify cryptographic signatures and content hash",
		outline: strings.TrimSpace(`
Outline — resolution verify
  Recompute the SHA-256 content_hash of the locked canonical text and
  verify each attestation against the signer's currently (or historically)
  valid public key. No real crypto verification is implemented yet.

  Flags (planned, not wired):
    --id string
`),
	},
}

// meetingCommands is the sketched board-meeting command set.
//
//	meeting create   — record a new board meeting
//	meeting list     — list board meetings
//	meeting minutes  — show or attach signed minutes
var meetingCommands = []stub{
	{
		name:    "create",
		summary: "Record a new board meeting",
		outline: strings.TrimSpace(`
Outline — meeting create
  Create a board meeting record (agenda, scheduled time, attendees)
  that resolutions can reference via meeting_id.

  Flags (planned, not wired):
    --title string
    --when rfc3339
`),
	},
	{
		name:    "list",
		summary: "List board meetings",
		outline: strings.TrimSpace(`
Outline — meeting list
  List recorded board meetings and their linked resolutions.
`),
	},
	{
		name:    "minutes",
		summary: "Show or attach signed meeting minutes",
		outline: strings.TrimSpace(`
Outline — meeting minutes
  Record or display canonical meeting minutes. Once opened for
  signature, minutes are locked and attested the same way as resolutions.

  Flags (planned, not wired):
    --id string
    --body-file path
`),
	},
}

// keysCommands is the sketched per-director Ed25519 key command set.
//
//	keys init      — generate a local identity keypair (private key stays local)
//	keys register  — register the public key with the board
//	keys rotate    — self-signed rotation of the active key
//	keys revoke    — 2-of-3 emergency revocation / recovery
//	keys list      — list keys and status (alias: keys status)
var keysCommands = []stub{
	{
		name:    "init",
		summary: "Generate a local Ed25519 identity keypair",
		outline: strings.TrimSpace(`
Outline — keys init
  Generate an Ed25519 identity keypair on this device. The private key
  never leaves the director's machine (or hardware key). Only the public
  key is later registered. Real key generation is not implemented yet.

  Flags (planned, not wired):
    --out-dir path
`),
	},
	{
		name:    "register",
		summary: "Register this director's public key",
		outline: strings.TrimSpace(`
Outline — keys register
  Publish the public key, fingerprint, and algorithm for this director.
  At most one key per member may be active at a time.

  Flags (planned, not wired):
    --public-key path
    --member-id string
`),
	},
	{
		name:    "rotate",
		summary: "Rotate the active key (self-signed by the current key)",
		outline: strings.TrimSpace(`
Outline — keys rotate
  Sign a rotation record with the current active key authorizing a new
  public key. The previous key moves to status=rotated; historical
  signatures made before rotated_at remain verifiable against it.

  Flags (planned, not wired):
    --new-public-key path
`),
	},
	{
		name:    "revoke",
		summary: "Emergency 2-of-3 revocation and key recovery",
		outline: strings.TrimSpace(`
Outline — keys revoke
  Propose or sign a 2-of-3 key_recovery resolution that revokes a lost
  or compromised key (revoked_at) and binds a replacement public key.
  The other two active directors must approve.

  Flags (planned, not wired):
    --member-id string
    --reason string
    --new-public-key path
`),
	},
	{
		name:    "list",
		summary: "List director keys and their status",
		aliases: []string{"status"},
		outline: strings.TrimSpace(`
Outline — keys list (alias: keys status)
  List each director's keys and status (active | rotated | revoked),
  fingerprints, and validity window. Private keys are never displayed.
`),
	},
}

func runGroup(stdout, stderr io.Writer, prog, group string, argv []string, commands []stub) int {
	if len(argv) == 0 || isHelp(argv[0]) {
		writeGroupHelp(stdout, prog, group, commands)
		return 0
	}
	for _, c := range commands {
		if c.matches(argv[0]) {
			return writeStub(stdout, prog, group, c)
		}
	}
	fmt.Fprintf(stderr, "unknown %s command: %s\n\n", group, argv[0])
	writeGroupHelp(stderr, prog, group, commands)
	return 2
}

func writeStub(stdout io.Writer, prog, group string, c stub) int {
	fmt.Fprintf(stdout, "%s\n\n", notImplemented)
	fmt.Fprintf(stdout, "# %s %s %s — %s\n", prog, group, c.name, c.summary)
	for _, line := range strings.Split(c.outline, "\n") {
		fmt.Fprintf(stdout, "# %s\n", line)
	}
	return 0
}

func writeRootHelp(w io.Writer, prog string) {
	fmt.Fprintf(w, `hugeai-inc-cli — Huge AI Inc board-resolution CLI

Usage:
  %s <command> [subcommand] [flags]

Commands:
  resolution   Draft, revise, sign, tally, list, and verify board resolutions
  meeting      Create, list, and record minutes for board meetings
  keys         Per-director Ed25519 identity keys (init, register, rotate, revoke, list)
  version      Print build version
  help         Show this help

Resolution subcommands:
  resolution draft     Draft a new board resolution
  resolution revise    Create a new revision linked via supersedes_id
  resolution sign      Cryptographically sign and submit a vote (approve|reject|abstain|recused)
  resolution tally     Check vote tally and 2-of-3 majority status
  resolution list      List board resolutions by status or type
  resolution verify    Verify cryptographic signatures and content hash

This build is a command-set scaffold. Subcommands print a short outline
and return "not yet implemented". There is no backend client and no
real signing logic yet.

Install:  brew install hugeai-inc/tap/hugeai-inc-cli
          apt install hugeai-inc-cli
          go install github.com/hugeai-inc/hugeai-inc-cli/cmd/hugeai-inc-cli@latest
`, prog)
}

func writeGroupHelp(w io.Writer, prog, group string, commands []stub) {
	fmt.Fprintf(w, "Usage:\n  %s %s <command> [flags]\n\nCommands:\n", prog, group)
	for _, c := range commands {
		alias := ""
		if len(c.aliases) > 0 {
			alias = " (alias: " + strings.Join(c.aliases, ", ") + ")"
		}
		fmt.Fprintf(w, "  %-12s %s%s\n", c.name, c.summary, alias)
	}
	fmt.Fprintf(w, "\nThis command is a stub and is not yet implemented.\n")
}

func isHelp(s string) bool {
	return s == "-h" || s == "--help" || s == "help"
}
