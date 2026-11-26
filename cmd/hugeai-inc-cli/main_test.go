package main

import (
	"bytes"
	"strings"
	"testing"

	"github.com/hugeai-inc/hugeai-inc-cli/internal/cli"
)

func testInfo() cli.BuildInfo {
	return cli.BuildInfo{Version: "0.0.0-test", Commit: "deadbeef", Date: "2026-11-25"}
}

func TestVersion(t *testing.T) {
	var stdout, stderr bytes.Buffer
	code := cli.Run([]string{"hugeai-inc-cli", "version"}, &stdout, &stderr, testInfo())
	if code != 0 {
		t.Fatalf("version exit = %d, want 0; stderr=%s", code, stderr.String())
	}
	out := stdout.String()
	if !strings.Contains(out, "hugeai-inc-cli 0.0.0-test") {
		t.Fatalf("version output missing version string:\n%s", out)
	}
	if !strings.Contains(out, "deadbeef") {
		t.Fatalf("version output missing commit:\n%s", out)
	}
}

func TestHelpListsCommands(t *testing.T) {
	var stdout, stderr bytes.Buffer
	code := cli.Run([]string{"hugeai-inc-cli", "--help"}, &stdout, &stderr, testInfo())
	if code != 0 {
		t.Fatalf("help exit = %d, want 0", code)
	}
	out := stdout.String()
	for _, want := range []string{
		"resolution draft",
		"resolution revise",
		"resolution sign",
		"resolution tally",
		"resolution list",
		"resolution verify",
		"meeting",
		"keys",
		"version",
	} {
		if !strings.Contains(out, want) {
			t.Errorf("help missing %q\n%s", want, out)
		}
	}
}

func TestUnknownCommand(t *testing.T) {
	var stdout, stderr bytes.Buffer
	code := cli.Run([]string{"hugeai-inc-cli", "nope"}, &stdout, &stderr, testInfo())
	if code != 2 {
		t.Fatalf("unknown command exit = %d, want 2", code)
	}
	if !strings.Contains(stderr.String(), "unknown command") {
		t.Fatalf("expected unknown command error, got %q", stderr.String())
	}
}

func TestStubsNotYetImplemented(t *testing.T) {
	commands := [][]string{
		{"resolution", "draft"},
		{"resolution", "revise"},
		{"resolution", "sign"},
		{"resolution", "tally"},
		{"resolution", "list"},
		{"resolution", "verify"},
		{"meeting", "create"},
		{"meeting", "list"},
		{"meeting", "minutes"},
		{"keys", "init"},
		{"keys", "register"},
		{"keys", "rotate"},
		{"keys", "revoke"},
		{"keys", "list"},
		{"keys", "status"},
	}
	for _, cmd := range commands {
		t.Run(strings.Join(cmd, " "), func(t *testing.T) {
			var stdout, stderr bytes.Buffer
			args := append([]string{"hugeai-inc-cli"}, cmd...)
			code := cli.Run(args, &stdout, &stderr, testInfo())
			if code != 0 {
				t.Fatalf("exit = %d, want 0; stderr=%s", code, stderr.String())
			}
			if !strings.Contains(stdout.String(), "not yet implemented") {
				t.Fatalf("expected stub message, got:\n%s", stdout.String())
			}
		})
	}
}
