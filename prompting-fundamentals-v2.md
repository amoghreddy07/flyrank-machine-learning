# Prompting Fundamentals on Real Tasks v2

## Task

Frame a machine learning problem for prioritizing which webpages should receive a content refresh, using the FlyRank starter dataset. The goal is a clear problem framing — task type, target/proxy, unit of analysis, and evaluation metric — not a trained model.

---

## Version 0 — Naive Prompt

> Help me complete my ML assignment.

**Representative Output:**
```
Sure! Here's a general approach to any ML assignment:
1. Understand the problem statement
2. Explore and clean your dataset
3. Choose a suitable model
4. Train and evaluate it
5. Summarize your findings
Let me know your dataset and I can give more specific advice.
```

**Why this is weak:** The prompt gives no information about the actual task, dataset, or goal, so the response is a generic textbook checklist. It could apply to literally any ML assignment, which means it adds nothing I couldn't already find in a tutorial.

---

## Version 1 — Role Assignment

**Technique:** Role Assignment

**Prompt:**
> You are an experienced machine learning mentor reviewing an intern's problem framing. Help me frame a machine learning problem for prioritizing which webpages need a content refresh.

**Representative Output:**
```
As your mentor, the first thing I'd check is whether you've framed
this as a ranking or classification problem — that decision shapes
everything downstream. Since you want a prioritized list of pages,
ranking is likely the better fit. I'd also want to see your target
definition and unit of analysis clearly stated before touching
metrics or models.
```

**Note:** Assigning the mentor role shifted the tone from "generic tutorial" to "evaluative feedback." The output started asking the kind of clarifying questions a real reviewer would ask, instead of listing generic ML steps.

---

## Version 2 — Context & Motivation

**Technique:** Context and Motivation

**Prompt:**
> You are an experienced machine learning mentor reviewing an intern's problem framing. Help me frame a machine learning problem for prioritizing which webpages need a content refresh. Context: this is for a real internship task using a provided starter dataset of webpages with SEO and performance-related columns, and the goal is a clean problem framing, not a trained model.

**Representative Output:**
```
Given that this is a framing exercise and not a modeling task, focus
on: (1) task type — ranking, since priority order matters more than
a binary label, (2) a target/proxy since explicit "needs refresh"
labels probably don't exist, (3) unit of analysis — one row per
page, and (4) a metric suited to ranking rather than accuracy.
```

**Note:** Adding context about the dataset and the fact that this is a framing-only exercise stopped the model from drifting toward suggesting model training. The response became more scoped and stayed within the actual boundaries of the assignment.

---

## Version 3 — Few-shot Examples

**Technique:** Few-shot Examples

**Prompt:**
> You are an experienced machine learning mentor. Help me frame a machine learning problem for prioritizing which webpages need a content refresh, using a provided starter dataset. Here are two examples of good framing from other problems:
> Example 1 — Customer churn: Task = classification, Target = churned (yes/no), Unit = one customer, Metric = recall.
> Example 2 — Product recommendation: Task = ranking, Target = likelihood of purchase, Unit = one product per user, Metric = Precision@K.
> Now frame the content refresh problem the same way.

**Representative Output:**
```
Following the same pattern:
- Task = ranking (order pages by refresh priority)
- Target/Proxy = a proxy signal for declining page performance
- Unit = one row per webpage
- Metric = Precision@K, since top-ranked pages matter most
This mirrors the recommendation example more closely than churn,
since both are about prioritized ordering, not a single label.
```

**Note:** The few-shot examples gave the model a consistent format to follow and, more usefully, it explicitly reasoned about which example the new problem resembled. The output became more structured and self-justifying instead of just stating conclusions.

---

## Version 4 — Output Structure

**Technique:** Output Structure

**Prompt:**
> You are an experienced machine learning mentor. Help me frame a machine learning problem for prioritizing which webpages need a content refresh, using a provided starter dataset. Return the answer as a Markdown table with columns: Component, Choice, Reason.

**Representative Output:**
```
| Component | Choice | Reason |
|---|---|---|
| ML Task | Ranking | Priority order matters more than a label |
| Target/Proxy | Performance decline signal | No explicit refresh labels exist |
| Unit of Analysis | One row per webpage | Matches dataset granularity |
| Evaluation Metric | Precision@K | Top-ranked accuracy matters most |
```

**Note:** Specifying a table format made the output immediately usable in a report or notebook without reformatting. It also forced the model to be concise per row instead of writing paragraph explanations that repeat the same point.

---

## Version 5 — Step Decomposition

**Technique:** Step Decomposition

**Prompt:**
> You are an experienced machine learning mentor. Help me frame a machine learning problem for prioritizing which webpages need a content refresh, using a provided starter dataset. Work through it step by step: first decide the task type, then the target/proxy, then the unit of analysis, then the metric, then explain why ML fits better than fixed rules. Return the final answer as a Markdown table.

**Representative Output:**
```
Step 1 - Task type: Ranking, since the output is a priority order.
Step 2 - Target/proxy: a decline-in-performance signal, standing in
for "needs refresh."
Step 3 - Unit of analysis: one row per webpage.
Step 4 - Metric: Precision@K, focused on getting top priorities right.
Step 5 - Why ML fits: it adapts to multiple signals over time, unlike
a fixed rule like "refresh every 6 months."

| Component | Choice |
|---|---|
| ML Task | Ranking |
| Target/Proxy | Performance decline signal |
| Unit of Analysis | One webpage per row |
| Evaluation Metric | Precision@K |
| Why ML Fits | Adapts to signals; fixed rules don't |
```

**Note:** Breaking the reasoning into explicit steps before the table made the final answer noticeably more defensible — each row in the table now has visible reasoning behind it rather than appearing as an unexplained conclusion. This was the most mentor-review-ready version.

---

## Claude vs ChatGPT Comparison

| Category | Claude | ChatGPT |
|-----------|---------|----------|
| Tone | More like a mentor giving considered feedback — slower, more explanatory | More direct and to the point, less "reasoning out loud" |
| Accuracy | Correctly avoided suggesting model training when told this was a framing-only task | Occasionally drifted toward suggesting "you could also try a baseline model," even when told not to |
| Structure | Followed the requested table/step format consistently across versions | Followed the format too, but sometimes added an extra unrequested summary paragraph after the table |
| Strengths | Stronger at justifying *why* each choice was made, not just stating it | Faster, more concise answers when a quick structured answer was all that was needed |
| Weaknesses | Responses ran slightly longer than necessary for a simple table request | Sometimes generalized the problem (e.g., mentioning "SEO best practices" broadly) instead of staying tightly scoped to the framing task |

---

## Final Reusable Prompt Template

```
You are an experienced machine learning mentor. Help me frame a
machine learning problem for [describe the business problem in one
sentence], using [briefly describe the dataset].

Work through it step by step:
1. Identify the ML task (e.g., classification, ranking, regression)
   and explain why it fits.
2. Recommend a target or proxy variable, and explain the reasoning.
3. Define the unit of analysis (what one row represents).
4. Recommend an evaluation metric suited to this task, and explain why.
5. Explain why ML is a better fit than fixed rules or manual review.

Requirements:
- This is a problem-framing exercise only — do not suggest specific
  model training steps, invented metrics, or fabricated results.
- Base the answer only on the task and dataset described above.
- Return the final answer as a clean Markdown table with columns:
  Component, Choice, Reason.
```
