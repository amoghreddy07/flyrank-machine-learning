# The Prompt Ladder

## Baseline Prompt (Weak)

> Help me complete my machine learning assignment.

**Representative AI Response:**
```
Sure! To complete a machine learning assignment, you'll generally need to:
1. Understand the problem
2. Collect and clean your data
3. Choose a model
4. Train and evaluate it
5. Write up your results
Let me know more about your specific assignment and I can help further.
```

---

## Version 1

**Layer Added:** Clear Goal

**Improved Prompt:**
> Help me frame a machine learning problem for prioritizing which webpages on a website need a content refresh, using a starter dataset provided by my internship.

**Representative Output:**
```
To frame this as an ML problem, start by deciding whether it's a
classification task (needs refresh / doesn't) or a ranking task
(order pages by refresh priority). Since you likely want a
prioritized list rather than a yes/no label, ranking may fit
better. You'll also need a target variable, a defined unit of
analysis (e.g., one row per page), and an evaluation metric
suited to ranking rather than plain accuracy.
```

- **What changed in the prompt:** Added a specific goal — content refresh prioritization — instead of a vague "help me."
- **What improved in the output:** The response stopped being a generic ML checklist and started reasoning about the actual problem type (ranking vs. classification), which is directly useful.
- **What still failed:** It didn't know who the output was for, so it stayed fairly textbook and didn't commit to a clean structure or metric choice.
- **What I would try next:** Tell it who this is for, so the depth and tone match a real internship deliverable instead of a general explanation.

---

## Version 2

**Layer Added:** Audience

**Improved Prompt:**
> Help me frame a machine learning problem for prioritizing which webpages on a website need a content refresh, using a starter dataset provided by my internship. I'm a machine learning intern writing this for a mentor review, not a beginner tutorial.

**Representative Output:**
```
Since this will be mentor-reviewed, frame it precisely: treat this
as a ranking problem, not classification, because the real goal is
ordering pages by priority. Define one row = one webpage. Pick a
target/proxy since you likely don't have labeled "needs refresh"
data. For evaluation, prioritize getting the top-ranked pages right
rather than overall accuracy — Precision@K is a reasonable fit.
```

- **What changed in the prompt:** Specified the audience — a mentor reviewing intern work — instead of leaving it audience-less.
- **What improved in the output:** The response got noticeably more precise and professional, and it started naming concrete things (Precision@K, target/proxy) instead of describing concepts abstractly.
- **What still failed:** It still didn't know what data I actually had access to, so the suggestions were reasonable but generic — it couldn't tailor anything to my starter dataset.
- **What I would try next:** Add context about the actual dataset and internship setup so the suggestions map to my real assignment instead of a hypothetical one.

---

## Version 3

**Layer Added:** Context

**Improved Prompt:**
> Help me frame a machine learning problem for prioritizing which webpages on a website need a content refresh, using a starter dataset provided by my internship. I'm a machine learning intern writing this for a mentor review. Context: this is part of the FlyRank Machine Learning internship, Week 2, working from a provided starter dataset with page-level SEO and performance columns.

**Representative Output:**
```
Given the FlyRank internship context, frame this as a ranking
problem: one row = one webpage. Use a target/proxy since explicit
refresh labels likely aren't provided. Evaluate with a
ranking-appropriate metric such as Precision@K. Document why ML is
preferable to fixed rules (e.g., static rules ignore traffic and
ranking trends). This aligns well with a typical Week 2 ML framing
deliverable.
```

- **What changed in the prompt:** Added internship name, week number, and a general description of the dataset's contents.
- **What improved in the output:** Barely anything — the response covered almost the same ground as Version 2, just with "FlyRank" and "Week 2" sprinkled in.
- **What still failed:** The extra context was mostly decorative. The AI didn't actually use it to change its reasoning or suggest anything dataset-specific, because I still hadn't told it what the columns or evaluation constraints actually were. This was the layer that honestly didn't help much — it made the prompt longer without making the output meaningfully better.
- **What I would try next:** Instead of vague context, specify the exact output structure I need, so the response stops repeating the same explanation and starts producing something usable.

---

## Version 4

**Layer Added:** Output Format

**Improved Prompt:**
> Help me frame a machine learning problem for prioritizing which webpages on a website need a content refresh, using a starter dataset provided by my internship. I'm a machine learning intern writing this for a mentor review. Context: this is part of the FlyRank Machine Learning internship, Week 2, working from a provided starter dataset with page-level SEO and performance columns. Format the answer as a Markdown list with these exact headers: ML Task, Target/Proxy, Unit of Analysis, Evaluation Metric, Why ML Fits.

**Representative Output:**
```
- **ML Task:** Ranking — order pages by refresh priority.
- **Target/Proxy:** A proxy signal indicating declining performance.
- **Unit of Analysis:** One row per webpage.
- **Evaluation Metric:** Precision@K, focused on top-ranked pages.
- **Why ML Fits:** Adapts to changing signals, unlike static rules.
```

- **What changed in the prompt:** Specified the exact Markdown structure and headers I wanted back.
- **What improved in the output:** Huge difference — the response became directly copy-paste usable and matched the structure my actual assignment needed, instead of paragraph explanations I'd have to reformat myself.
- **What still failed:** The content itself was still fairly generic under each header — no clear standard for what makes the target/proxy or metric choice good versus just plausible.
- **What I would try next:** Add explicit quality criteria so the response has to justify each choice instead of just stating it.

---

## Version 5

**Layer Added:** Quality Criteria

**Improved Prompt:**
> Help me frame a machine learning problem for prioritizing which webpages on a website need a content refresh, using a starter dataset provided by my internship. I'm a machine learning intern writing this for a mentor review. Context: this is part of the FlyRank Machine Learning internship, Week 2, working from a provided starter dataset with page-level SEO and performance columns. Format the answer as a Markdown list with these exact headers: ML Task, Target/Proxy, Unit of Analysis, Evaluation Metric, Why ML Fits. For each item, briefly justify why it's the right choice, not just what it is, and avoid suggesting any model training or invented results.

**Representative Output:**
```
- **ML Task:** Ranking — the goal is prioritized order, not a
  yes/no label, so ranking fits better than classification.
- **Target/Proxy:** Use a proxy for refresh need since explicit
  labels aren't available; justify the proxy's relevance.
- **Unit of Analysis:** One row per webpage, keeping the dataset
  interpretable and consistent with the framing task.
- **Evaluation Metric:** Precision@K, since getting the top
  priorities right matters more than overall accuracy.
- **Why ML Fits:** Learns from multiple signals and adapts, unlike
  fixed rules that don't adjust as performance changes.
```

- **What changed in the prompt:** Asked the AI to justify each choice and explicitly avoid inventing model training or results.
- **What improved in the output:** Each point now reads like reasoning instead of a definition — closer to what a mentor would actually want to see in a problem-framing writeup.
- **What still failed:** The justifications are still somewhat generic; they'd need real dataset column names and specifics to become truly review-ready.
- **What I would try next:** Feed in the actual starter dataset column names and constraints directly, rather than describing them abstractly, to get output tailored to the real data.

---

## Final Reusable Prompt

```
Help me frame a machine learning problem for [describe the business
problem in one sentence], using [describe the dataset briefly].

Please identify and justify each of the following:
- ML Task: what type of ML problem this is, and why
- Target/Proxy: what target or proxy variable to use, and why
- Unit of Analysis: what one row in the dataset represents
- Evaluation Metric: which metric fits this task, and why
- Why ML Is Appropriate: why ML is a better fit than fixed rules
  or manual review for this problem

Requirements:
- Do not suggest specific model training steps or invent results —
  this is a problem-framing exercise, not a modeling exercise.
- Keep the answer grounded only in the dataset and context provided.
- Output the answer in clean Markdown, using the exact headers
  above as a bulleted list.
```
