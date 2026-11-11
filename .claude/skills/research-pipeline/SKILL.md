---
name: research-pipeline
description: Runs one stage of the PhD research pipeline (survey, design, verify, experiments, write, review) for one paper. Use when the user types /research-pipeline or asks to advance a paper.
argument-hint: "<paper-id> [stage] [venue]   e.g. v2x survey | benchmark next | status"
---
# Research pipeline

Arguments: `$ARGUMENTS`

You are the orchestrator. You delegate; you do not do stage work yourself.

## Start
1. Read `research/STATE.md` (and nothing else yet).
2. `status` -> print the table and the open items, then stop.
3. `<id> next` -> run the first stage that is not `done` for that paper.
4. Refuse to start a stage whose predecessor is not `done`, and say which one is missing.

## Stages

| stage | agents | inputs they read | output | gate |
|---|---|---|---|---|
| survey | `lit-scout` x3-5 topics in parallel -> `paper-reader`, one per new key, in parallel batches of 5 -> `gap-analyst` | brief, candidates | `papers/<id>/gap.md` | human approves gap |
| design | `protocol-designer` | brief, gap | `papers/<id>/design.md` | human settles DECISION items |
| verify | `formal-verifier` | design | `papers/<id>/model/` | none |
| experiments | `experiment-engineer` | design | `papers/<id>/results/` | human runs `run.sh` locally |
| write | `paper-writer` | gap, design, results | `papers/<id>/paper/main.tex` | none |
| review | `reviewer`, then `paper-writer` with the review; at most 2 rounds | paper + evidence | `papers/<id>/review.md` | human reads before submitting |

- `verify` and `experiments` are independent: launch both in one message.
- `benchmark` skips design and verify. `framework` runs only after two application papers are done.
- If verify falsifies a goal because of the design, return to design; do not patch the model.
- If gap-analyst reports thin spots, run one more scout + reader pass on those topics only, then re-run gap-analyst once.

## Token rules
- Give each agent only: the paper id, the stage inputs by path, and any human decision. Do not paste file contents or conversation history into prompts.
- Agents answer in a few lines. Do not ask for more, and do not read their output files
  yourself unless a gate needs you to show something to the human.
- Never re-run an agent whose output file exists unless its input changed or the human asks.
- One stage per invocation. Stop at every gate.
- Mechanical checks go through `tools/check_paper.py`, not through an agent.

## Finish
Update the paper's row in `research/STATE.md`, add anything the human must do under
"Open items", commit with message `<id>: <stage>`, and report in five lines or fewer:
what was produced, where, and what you need from the human.
