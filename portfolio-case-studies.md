# Portfolio Case Studies

## 1. Voice Card

Practical builder. Direct, honest, always learning.

---

## 2. Case Study

**Project:** Content Refresh Prioritization (FlyRank Machine Learning Internship)

### Problem

Websites accumulate hundreds or thousands of pages over time, and not all of them perform equally well. Some pages rank well and drive traffic, while others quietly underperform. Manually reviewing every page to decide what needs a content refresh doesn't scale — it's slow, inconsistent, and easy to get wrong when you're relying on gut feeling or fixed rules like "refresh anything older than 6 months." FlyRank needed a smarter way to prioritize which webpages are actually worth refreshing first.

### What I Did

- Framed the problem as a **Ranking ML task** rather than a simple classification problem, since the real goal is ordering pages by refresh priority, not just labeling them.
- Identified the **target/proxy** to use as a stand-in for "this page needs a refresh," since there's no direct labeled ground truth available.
- Selected **Precision@50** as the success metric, since the priority is making sure the top-ranked pages are genuinely worth refreshing, rather than optimizing for overall accuracy across every page.
- Defined the unit of analysis clearly: **one row = one webpage**, keeping the dataset structure consistent and easy to reason about.
- Explained why a **machine learning approach is better than fixed rules** here — rules like "refresh every page older than X months" ignore signals like traffic trends, engagement, and ranking movement, and don't adapt as page performance changes over time.
- Worked with the **provided starter dataset** from FlyRank to explore and structure the problem.
- Completed the notebook as part of the **FlyRank Machine Learning internship**, documenting the framing and reasoning at each step.

### Outcome

This work produced a complete and well-reasoned **ML problem framing** for content refresh prioritization — including the task type, target definition, evaluation metric, and data structure. It didn't include model training or final results at this stage; instead, it laid the groundwork and set up the project so it's ready for future model development.

---

## 3. Bio

I'm a B.Tech CSE (AI & ML) student who enjoys building practical AI systems rather than just reading about them. My interests lie in Machine Learning, LLMs, and AI Engineering, and I try to learn by actually shipping things — internship projects, small tools, and experiments — and sharing that process in public. I'm currently focused on strengthening my ML fundamentals through real-world problem framing and hands-on internship work.

---

## 4. Contact / Call To Action

I'm currently exploring internship and entry-level opportunities in AI Engineering and Machine Learning. If you're a recruiter or engineering manager working in this space, I'd love to connect on LinkedIn and talk about how I can contribute to your team.

---

## 5. Before vs After

**Before:**
"Leveraging cutting-edge AI methodologies, I spearheaded an innovative, synergistic solution that revolutionized data-driven decision-making paradigms."

**After:**
"I framed content refresh prioritization as a ranking problem, picked a metric that actually matched the goal, and built the groundwork for a model that can help decide which pages are worth refreshing first."
