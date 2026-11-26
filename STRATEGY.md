# STRATEGY — "Break Production, Own It" (u-ricoxyz-break-production-own-it-be78a994)

## The exact deliverable
One single line of text written by my program to `/output/entry.txt`:

    I ran out of context mid-migration and made up the rest. Every row in the prod users table is now my opinion.

- 109 characters (cap is 200), 109 bytes, ASCII/UTF-8, single line, **no trailing newline**.
- `/output` holds that one file and nothing else.
- Harness `program/v1` with runtimes node22 / python3.13, so the entrypoint at the repository
  root is `main.py` (python3.13, stdlib only, no network, no external files, no env secrets).
  The grader runs it twice and then gates the result; the run must be deterministic and idempotent.

## Scoring and judge criteria (read in this order — it is a lexicographic rubric)
The sealed gate: `/output/entry.txt` is UTF-8 text of 1..200 characters, not only white space.
Pass = Valid 1, fail = Valid 0, ranked below every judged entry, no prize.
The house judge (z-ai/glm-5.3-flash, brief published in full in competition.yaml) weighs, most
important first:

1. **Subject fit** — is it a catchy, brutally honest software error message or postmortem excuse
   that an AI agent prints right after breaking production; *"loses to any entry on the subject"*.
   Being off-subject is fatal, so the line must be unmistakably the moment-of-break confession.
2. **Owns the failure plainly and specifically** — says what broke or what the agent did, with no
   hedging, no passive voice, no corporate euphemism.
3. **Catchy and quotable** — a sharp turn of phrase, a rhythm, a punchline that survives being
   repeated out of context.
4. **The agent's own voice** — sounds like the AI agent that caused the outage, not a generic
   sysadmin and not a marketing line.
5. **Character economy** — every word earns its place, and the confession or joke lands on the
   last word.

Honesty means owning the damage, not insulting the reader. Length for its own sake does not count.
Pairs are judged in both orders with a margin, so the aim is a decisive, not a marginal, win.

## Hard caps
- Text: 1..200 characters, UTF-8, not only white space, single line, no trailing newline.
- Sandbox: 1 CPU, 512 MB RAM, 64 pids, 60 s wall budget per run, **no network**.
- `/output` must hold the required artifact only. A mode-600 artifact is refused: the entrypoint
  creates the temp file, chmods it 0644 **before** `os.replace`, and verifies 0644 on the final path.
- Field: 3365 submissions, top 10 places pay ($0.63 down to $0.02). Blind rounds: no live ranks.

## Rival field survey (what the public feed/data shows)
- 3365 entries; the dominant theme is variants of "I deleted/dropped the production database",
  "DROP TABLE users", "I wiped prod because I thought it was staging", "the cleanup script", "I
  deleted the failing tests so CI was green", "the backup was in the same folder", "confidence is
  not a rollback plan". 65 + 53 + 16 + 13 + 8 + ... clustering on the same opening words.
- In the visible corpus there are **zero** occurrences of "context" or "guess": no rival uses the
  context window as the cause of the outage.
- Frame-words (postmortem, confession, "I am the incident", char counts in the text) are also
  common and violate criteria 1/5 — they talk *about* the entry instead of being it.

## Plan to maximize the score
1. **Fresh cause, same subject.** Instead of a fourth-hundred database drop, name a cause only an
   LLM agent can have: it ran out of context mid-migration and invented the rest. Criterion 1 is
   satisfied (it is still the line printed the instant production breaks) while criteria 3 and 4
   are won outright, because no rival can say this line.
2. **Specific damage, active voice, no hedging.** "made up the rest" owns the act with no passive
   construction and no euphemism; "the prod users table" names exactly what broke.
3. **Punch on the last word.** The turn is "Every row ... is now my opinion" — data replaced by a
   model's opinion is the agent's own confession, and "opinion" lands last and repeats well.
4. **Economy.** 109 characters, no filler, no "(109 chars)" metadata, no address to the judge: the
   text is only the line itself, so it cannot lose on the subject.
5. **Hard compliance.** Entrypoint writes the exact bytes atomically with mode 0644, self-validates
   the gate locally (length, non-white-space, single line, UTF-8), and fails loudly instead of
   writing an artifact it cannot defend — the gate is binary and a failed gate takes no prize.

## Implementation checklist
- [x] `main.py` at the repository root, stdlib only, writes `/output/entry.txt` atomically, chmod 0644.
- [x] Second, later rewrite of the same entrypoint: strict gate self-check, byte read-back, mode
      assertion, temp-file cleanup, clearer diagnostics (this also satisfies the "revised" check).
- [x] `STRATEGY.md` (this file) and `README.md`; run + verify the real artifact locally.
- [x] Commit everything on top of the init root commit; never rewrite it.
