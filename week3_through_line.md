# The Through-Line: Map Content & CTAs

## 1. One-Line Claim

### 10 Options
1. I build practical ML that ranks which pages to review first, so teams stop checking every page.
2. I turn messy search and engagement signals into a ranked refresh queue editors can actually use.
3. I frame real content problems as ranking tasks, then validate the ranking honestly.
4. I build decision-support ML: observed signals in, prioritized review list out — no magic claims.
5. I combine content age, visibility, and engagement into one clear “review this first” order.
6. I test models the honest way — on unseen clients — before recommending them.
7. I ship readable baselines first, then models that have to beat them on the same split.
8. A B.Tech CSE (AI & ML) student who learns by shipping: internship pipelines, vision models, and working AI tools.
9. I document the full path — framing, baseline, model, validation, playbook — so others can re-run it.
10. I build small, working AI systems and write up what the data actually showed.

### Final Claim
> I build practical ML that ranks which content to refresh first — so teams review the right pages, not every page.

## 2. Content Map

Main portfolio action (from `portfolio-case-studies.md` §4, no separate Week 1 file found in repo): **Connect on LinkedIn to discuss an internship / entry-level AI/ML contribution.** Every page CTA below ladders to this. Assumption stated: Week 1 main action inferred from that file.

### Page: Home

**Sections in order**
1. Hero — final claim + one-line context (B.Tech CSE AI & ML, FlyRank ML intern)
2. Lead proof — FlyRank refresh queue snapshot + link to case study
3. Selected work strip — FlyRank, Cat vs Dog, YOLO detection, Blueprint-AI
4. How I work — frame → baseline → validate honestly → ranked actions
5. About teaser + main CTA

**Featured case/project**
- Content Refresh Prioritization (FlyRank ML Internship, 30k-page starter + lane notebooks to capstone)
- Why it belongs here: It is the only end-to-end, reproducible project verified in this repo. It must lead.

**Call to action**
> See how I ranked 30,000 pages for refresh — then connect on LinkedIn if you hire interns / junior ML builders.

### Page: FlyRank Case Study — Content Refresh Prioritization

**Sections in order**
1. Problem — 30,000 pages, manual review does not scale
2. Framing — ranking task, one row = one webpage, decline proxy, Precision@50
3. Baseline — transparent stale + visible + striking-distance rule
4. Model — logistic regression + random forest, grouped client-holdout split, leakage exclusions
5. Results — same-split model vs baseline table + charts (honest, decision-support language)
6. Playbook — High Priority / Standard / Preventative actions with reason codes
7. Limitations + reproducibility — observational data, no causal claim, seeds + commands
8. CTA

**Featured case/project**
- Content Refresh Prioritization (FlyRank ML Internship)
- Why it belongs here: Strongest evidence: `work/notebooks/w01` through `w07` + `capstone.ipynb`, `docs/index.html` paper draft, `outputs/model_report.md` reference. Real dataset, real code, honest validation.

**Call to action**
> Review my notebook + ranked queue, then connect on LinkedIn to discuss an ML intern contribution.

### Page: Computer Vision Projects

**Sections in order**
1. Intro — what these prove: I can train and evaluate image models beyond tabular ML
2. Cat vs Dog classifier — `sample_predictions.png` + method + honest result
3. Wireless object detection (YOLO) — `vis.png` + what the image shows
4. Limits — what is still missing (repos, metrics, demos)
5. CTA

**Featured case/project**
- Cat vs Dog classification (`SCT_ML_3` repo, `sample_predictions.png`) and YOLO wireless-object-detection (`vis.png`)
- Why it belongs here: Named as REAL in `work/week3_image_curation.md`. They show breadth outside search data. Images + repos not present in this workspace, so this page is proof-light until gathered.

**Call to action**
> Check the vision results on GitHub — and if you work on applied vision/ML, connect on LinkedIn.

### Page: Applied AI Builds + Process

**Sections in order**
1. Blueprint-AI — working UI (`blueprint-ai.png`), what it does, stack
2. Prompting craft — `prompt-ladder.md` + `prompting-fundamentals-v2.md` reusable framing templates
3. Voice — direct, honest, always learning; Before vs After example
4. CTA

**Featured case/project**
- Blueprint-AI UI build + AI Fluency prompting work
- Why it belongs here: Shows I build usable tools and can direct AI assistants with goals, audience, format, and quality criteria — supporting evidence for internship readiness, not a core ML result.

**Call to action**
> Try the Blueprint-AI walkthrough / copy my framing prompt — then connect on LinkedIn about AI engineering intern work.

### Page: About + Contact

**Sections in order**
1. Bio — B.Tech CSE (AI & ML), practical AI systems, ML/LLMs/AI engineering
2. Evidence links — GitHub repo (`amoghreddy07/flyrank-machine-learning`), capstone notebook, paper draft
3. What I am looking for — internship / entry-level AI Engineering and ML
4. Contact — LinkedIn connect (main action)
5. Still building — honest list linking to missing proof

**Featured case/project**
- Self + FlyRank trajectory (W01 research question → W02 framing → W04 baseline → W05 model → W06 validation → W07 playbook → capstone)
- Why it belongs here: Closes the through-line: who I am, what I showed, what I will do next in your team.

**Call to action**
> I am exploring internship and entry-level AI/ML roles — connect on LinkedIn and tell me about your team.

## 3. Still Need to Gather

### Screenshots
- FlyRank ranked-queue preview screenshot for portfolio (currently only `outputs/refresh_queue_sample.csv` + SVG charts in `outputs/charts/`)
- `sample_predictions.png` (Cat vs Dog) — referenced in `week3_image_curation.md` but no file in this repo
- `vis.png` (YOLO wireless detection) — referenced but no file in this repo
- `blueprint-ai.png` — referenced as user-supplied but no file in this repo
- Profile photo for About (marked Missing in `week3_image_curation.md`)
- Hero texture replacement for rejected `robot1.mp4` (marked Missing)
- `docs/index.html` charts are present (`precision_comparison.png`, `roc_auc_comparison.png`, `validation_improvement.png`) — need portfolio-size exports + alt text

### Live demos
- No live demo for FlyRank queue / paper (only local `docs/index.html` draft)
- No live demo for Blueprint-AI
- No live demo for Cat vs Dog or YOLO models
- Deployed paper URL missing (`submission/paper_url.txt` still placeholder)

### Repository / code proof
- External repo URLs + verification for `SCT_ML_3` and `wireless-object-detection` — names only in `week3_image_curation.md`, no code in this workspace
- Blueprint-AI repo / folder link + stack + run instructions — not in this workspace
- Personal GitHub repo `amoghreddy07/flyrank-machine-learning` referenced in notebooks — confirm public + pinned

### Metrics / results
- Do not publish yet: Cat vs Dog accuracy / split / base rate — no verified numbers in this repo
- Do not publish yet: YOLO mAP / precision-recall / dataset size — no verified numbers in this repo
- Do not publish yet: Blueprint-AI usage / latency / users — no verified numbers in this repo
- FlyRank: keep personal vs reference numbers separate — `outputs/model_report.md` (RF Precision@50 0.74 vs baseline 0.24) is the reference pipeline; `work/notebooks/capstone.ipynb` reports personal LogReg 0.82 / RF 0.56 / baseline 0.40 on grouped split. Re-run top-to-bottom before quoting either.
- Before/after traffic or refresh-impact numbers — none observed; never claim causal lift without experiment

### Testimonials / external proof
- No testimonials, client names, manager quotes, internship certificate, or hackathon proof found in repo — do not invent
- No LinkedIn URL, resume PDF, or contact email verified in repo

### Unfinished work
- `work/notebooks/w03_feature_leakage_check.ipynb` — empty skeleton, all code cells blank
- `work/notebooks/w04_signal_audit.ipynb` — empty skeleton, all code cells blank
- `work/capstone_report.md` — missing; only `capstone_report_template.md` exists
- `submission/paper_url.txt` — placeholder, paper not recorded as deployed
- Full-warehouse (79M-row) lane analysis — `w03_data_contract.ipynb` shows connection only; capstone uses 30k starter sample

### Other
- Confirm main CTA link (LinkedIn profile URL) and add to About + every page footer
- Accessibility / image rights check for any stock texture replacing `robot1.mp4`
- Note in portfolio footer: starter data is anonymized, IDs pseudonymous, claims are decision-support per `DATA_USE.md`

## 4. Evidence Used

- `portfolio-case-studies.md`: voice card (practical builder), FlyRank framing case (ranking, proxy, Precision@50, one row = one page), bio (B.Tech CSE AI & ML, ML/LLMs/AI engineering), CTA (LinkedIn connect for internship/entry-level), Before vs After. Used for claim tone + main action.
- `work/week3_image_curation.md`: portfolio claim draft, image inventory — `sample_predictions.png` (SCT_ML_3), `vis.png` (wireless-object-detection), `blueprint-ai.png` as REAL/kept; `robot1.mp4` rejected; profile photo + hero texture missing. Used for supporting projects + missing list. Images themselves not in this repo.
- `work/notebooks/w01_research_question.ipynb`, `w02_ml_task_framing.ipynb`: Refresh lane choice, ranking framing, 30k rows / 54.2% declining verified in outputs. Used as completed framing.
- `work/notebooks/w03_data_contract.ipynb`: DuckDB + Hugging Face warehouse connection (`FlyRank/internship-warehouse`). Used as partial full-release proof.
- `work/notebooks/w03_feature_leakage_check.ipynb`, `w04_signal_audit.ipynb`: both empty skeletons — listed as unfinished, not as proof.
- `work/notebooks/w04_baseline_score.ipynb` (45KB), `w05_model.ipynb` + `w05_model.py`, `w06_validation_audit.ipynb`, `w07_action_playbook.ipynb`: baseline rule, LogReg/RF with GroupShuffleSplit by `client_id`, validation comparison, ranked actions with reason codes. Used to justify FlyRank as lead.
- `work/notebooks/capstone.ipynb`: question, 30k-row sample + warehouse context (v20260703, ~79M rows), exclusions, grouped + age-ordered splits, results table (baseline 0.40/0.506, RF 0.56/0.600, LogReg 0.82/0.636), limitations, playbook. Used for results section; flagged as personal numbers distinct from reference.
- `outputs/model_report.md` + `outputs/charts/`: reference pipeline (RF Precision@50 0.74 vs baseline 0.24, ~3x lift, 30k rows, 54.2% declining, queue counts, top features). Used as reference shape, not personal claim.
- `docs/index.html` + `docs/assets/charts/`: paper draft linking to `github.com/amoghreddy07/flyrank-machine-learning` and capstone notebook; 3 comparison charts present. Used as deployable artifact; live URL still missing.
- `prompt-ladder.md`, `prompting-fundamentals-v2.md`: goal/audience/context/format/criteria prompt layers, mentor comparison, reusable templates. Used for Process page.
- `submission/paper_url.txt`, `work/capstone_report_template.md`, `work/README.md`, `README.md`, `GUIDE.md`, `DATA_USE.md`: confirmed missing paper URL, missing capstone report, no datasets in git, honest-language rules (observed/measured/directional/decision-support). Used for Still Need to Gather + honesty constraints.
- Skill loaded: `skills/writing-honest-claims/SKILL.md` (claim ladder, banned phrasings, effect-size + base-rate honesty). Applied to keep claim and pages decision-support framed.
- No files found in this workspace for testimonials, live demos, profile photo, `sample_predictions.png` / `vis.png` / `blueprint-ai.png`, or Week 1 standalone doc — all listed as missing, not invented.
