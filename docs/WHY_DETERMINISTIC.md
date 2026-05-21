# Why Deterministic

Agent Readiness Scanner intentionally avoids LLM calls in the core readiness
scan.

The product is a preflight gate. Gates need to be repeatable.

---

## Repeatability

Same repo, same files, same result.

This matters because a readiness score should be stable enough for CI, release
checks, and team policy. LLM judgments can vary by prompt, model version,
temperature, context window, and provider behavior.

---

## Zero Token Cost

The scan costs nothing per run.

No API key. No token budget. No surprise usage bill. This makes it safe to run
locally, in CI, and across many repos.

---

## Offline Compatibility

The scanner reads the local filesystem only.

It works on private repos, air-gapped machines, local-agent workflows, and
developer laptops without internet access.

---

## CI Compatibility

CI gates need predictable output and exit codes.

`agent-scan . --fail-under 70` is useful because it does not depend on an
external model, network access, or third-party service availability.

---

## Trust Boundary

The scanner does not send repo content anywhere.

No LLM calls. No telemetry. No analytics. No background service. The trust model
is simple: local files in, local report out.

---

## Model Independence

Agent Readiness Scanner works before Claude, Cursor, Copilot, Codex, or local
agents touch the repo.

It is not tied to one model, one editor, one vendor, or one agent runtime.

---

## Faster Execution

Static checks are fast.

The scan should be quick enough to run before a coding session, inside CI, or as
part of a repo hygiene check without blocking the developer.

---

## Lower Attack Surface

No network calls means fewer ways to leak data, fail due to remote outages, or
introduce supply-chain/API risk.

The scanner should stay boring in the best possible way.

---

## Where LLMs Could Help Later

LLMs may be useful as optional layers:

- Optional report summarization
- Optional governance file drafting
- Optional red-cell review of readiness gaps

These must remain optional. LLMs must not be required for the core readiness
scan.

---

## Core Rule

LLMs can help explain or repair readiness gaps. They should not be necessary to
detect the first readiness signal.

