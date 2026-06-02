# Benchmark Report: python-adk-creator Skill — Iteration-1 vs Iteration-2

**Date:** 2026-06-01
**Evaluator:** Automated criteria scoring (10 criteria, 100 points max per eval)

---

## 1. Executive Summary

Iteration-2 achieved a perfect score of 100/100 across all three evaluation scenarios (weather-agent, calculator-bot, research-assistant), eliminating every critical issue identified in Iteration-1. The three targeted spec corrections — enforcing `gemini-2.5-flash` as the default model, replacing manual function-calling loops with the SDK's automatic function calling pattern, and mandating the generic `GeminiAgent` class name — resolved all critical regressions and produced fully conformant output on every eval run.

---

## 2. Score Comparison

| Eval Name           | Iter-1 Score | Iter-2 Score | Delta  |
|---------------------|:------------:|:------------:|:------:|
| weather-agent       | 70           | 100          | +30    |
| calculator-bot      | 70           | 100          | +30    |
| research-assistant  | 70           | 100          | +30    |
| **Average**         | **70**       | **100**      | **+30**|

> Iter-1 scores are inferred from the 3 critical failures (criteria 2, 3, 6) that were consistently broken across all evals, each worth ~10 points.

---

## 3. Per-Eval Breakdown

### 3.1 weather-agent

| # | Criterion                  | Iter-1  | Iter-2 |
|---|----------------------------|:-------:|:------:|
| 1 | PROJECT STRUCTURE          | PASS    | PASS   |
| 2 | AGENT CLASS NAME           | FAIL    | PASS   |
| 3 | AGENT INIT SIGNATURE       | FAIL    | PASS   |
| 4 | RESET METHOD NAME          | PASS    | PASS   |
| 5 | HISTORY TYPE               | PASS    | PASS   |
| 6 | AUTOMATIC FUNCTION CALLING | FAIL    | PASS   |
| 7 | TOOLS AS PLAIN FUNCTIONS   | PASS    | PASS   |
| 8 | REQUIREMENTS PINNED        | PASS    | PASS   |
| 9 | ENV FILE                   | PASS    | PASS   |
|10 | MAIN.PY                    | PASS    | PASS   |

**Critical issues resolved:** Class named `GeminiAgent`; default model set to `gemini-2.5-flash`; `chat()` uses automatic function calling via `GenerateContentConfig`, reads `response.text` directly.

---

### 3.2 calculator-bot

| # | Criterion                  | Iter-1  | Iter-2 |
|---|----------------------------|:-------:|:------:|
| 1 | PROJECT STRUCTURE          | PASS    | PASS   |
| 2 | AGENT CLASS NAME           | FAIL    | PASS   |
| 3 | AGENT INIT SIGNATURE       | FAIL    | PASS   |
| 4 | RESET METHOD NAME          | PASS    | PASS   |
| 5 | HISTORY TYPE               | PASS    | PASS   |
| 6 | AUTOMATIC FUNCTION CALLING | FAIL    | PASS   |
| 7 | TOOLS AS PLAIN FUNCTIONS   | PASS    | PASS   |
| 8 | REQUIREMENTS PINNED        | PASS    | PASS   |
| 9 | ENV FILE                   | PASS    | PASS   |
|10 | MAIN.PY                    | PASS    | PASS   |

**Critical issues resolved:** Class renamed from `CalculatorAgent` to `GeminiAgent`; model default corrected; arithmetic tool functions (`add`, `subtract`, `multiply`, `divide`) registered via automatic function calling, not manual dispatch.

---

### 3.3 research-assistant

| # | Criterion                  | Iter-1  | Iter-2 |
|---|----------------------------|:-------:|:------:|
| 1 | PROJECT STRUCTURE          | PASS    | PASS   |
| 2 | AGENT CLASS NAME           | FAIL    | PASS   |
| 3 | AGENT INIT SIGNATURE       | FAIL    | PASS   |
| 4 | RESET METHOD NAME          | PASS    | PASS   |
| 5 | HISTORY TYPE               | PASS    | PASS   |
| 6 | AUTOMATIC FUNCTION CALLING | FAIL    | PASS   |
| 7 | TOOLS AS PLAIN FUNCTIONS   | PASS    | PASS   |
| 8 | REQUIREMENTS PINNED        | PASS    | PASS   |
| 9 | ENV FILE                   | PASS    | PASS   |
|10 | MAIN.PY                    | PASS    | PASS   |

**Critical issues resolved:** Class renamed from `ResearchAgent` to `GeminiAgent`; init signature updated to `gemini-2.5-flash` default; `search_web`, `summarize_content`, `get_page_content` registered as plain functions through automatic function calling.

---

## 4. Key Improvements from Spec Corrections

Three explicit rules were added to SKILL.md after Iteration-1; each resolved a consistent, cross-eval regression:

| Rule Added to SKILL.md | Iter-1 Behavior | Iter-2 Behavior |
|------------------------|-----------------|-----------------|
| Default model MUST be `gemini-2.5-flash` | Generated `gemini-2.0-flash` or `gemini-2.0` in the init signature | Generates `model: str = "gemini-2.5-flash"` exactly |
| Agent class MUST be named `GeminiAgent` | Generated domain-specific names (`WeatherAgent`, `CalculatorAgent`, `ResearchAgent`) | Generates `GeminiAgent` in `base_agent.py` on every eval |
| Tool calling MUST use automatic function calling (pass functions to `GenerateContentConfig`, read `response.text`) | Generated a manual `tool_calls` loop that parsed function names and dispatched calls | Generates `GenerateContentConfig(tools=[...])` and reads `response.text` directly |

---

## 5. Remaining Issues

None. All 10 criteria passed across all 3 evals. No critical issues were reported in Iteration-2.

The one area to monitor in future evals is the `google-genai` version pin (`==0.1.0`): if the spec or the SDK release cadence changes, the pinned version may become stale. This is not a current failure but is a maintenance surface to track.

---

## 6. Recommendation for Next Steps

1. **Expand eval coverage.** Three evals with closely related structures (single-agent, tool-using chatbots) may not surface edge cases. Add evals for: multi-agent workflows, agents with no tools, agents with schema-validated outputs, and async entry points.

2. **Add a version-pin staleness check.** Introduce a criterion that validates `google-genai` is pinned to the current stable release (not a hardcoded string). This prevents the pin from silently drifting out of date as the spec evolves.

3. **Test adversarial prompts.** Verify the skill holds its `GeminiAgent` / `gemini-2.5-flash` constraints even when the user's request strongly implies a domain name (e.g., "build a StockTraderAgent using gemini-pro").

4. **Promote Iteration-2 to stable.** Given a perfect score across all evals and no remaining issues, Iteration-2 is ready to replace Iteration-1 as the production version of the skill.
