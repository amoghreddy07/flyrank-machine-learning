#!/usr/bin/env python
# coding: utf-8

# # ML-08 — Capstone Modeling Lane
# 
# This notebook trains an ML model for the content refresh lane and compares it against the Week 4 baseline.
# 
# **Lane:** Refresh / Content Opportunity Scoring  
# **Dataset:** `data/raw/content_refresh_anonymized.csv`  
# **Label:** `is_declining` = 1 when `trend_direction == "down"`
# 

# In[1]:


# ── Imports and data load ──────────────────────────────────────
import pandas as pd
import numpy as np
from sklearn.model_selection import GroupShuffleSplit
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import precision_score, roc_auc_score
from IPython.display import display, Markdown

df = pd.read_csv("../../data/raw/content_refresh_anonymized.csv")

# Derive target exactly as in baseline
df["is_declining"] = (df["trend_direction"] == "down").astype(int)

# Create baseline score exactly as in baseline
df["is_stale"] = (df["days_since_last_update"] >= 91).astype(int)
df["is_visible"] = (df["impressions_90d"] >= 100).astype(int)
df["is_striking"] = ((df["avg_position"] >= 4) & (df["avg_position"] <= 20)).astype(int)
df["baseline_score"] = df["is_stale"] * df["is_visible"] * df["is_striking"] * df["impressions_90d"]

print(f"Loaded {len(df):,} rows")
print(f"Base rate: {df['is_declining'].mean():.3f}")


# ## 1. Method choice and why
# 
# **Method Chosen:** Logistic Regression (with a Random Forest for comparison).
# 
# **Why it fits:** 
# - The task is a binary classification ("yes/no with an observed label") converted into a ranking task ("which first?").
# - Logistic Regression provides probabilities which naturally rank the items.
# - It is highly interpretable (we can read coefficients to understand feature importance and catch leakage).
# - The baseline was a hard-coded heuristic; Logistic Regression will learn the optimal weights for these and other signals.
# 

# ## 2. Split design
# 
# **Design:** Grouped validation by `client_id` (GroupShuffleSplit).
# 
# **Why this is honest:** 
# - The dataset contains pages from multiple clients. If we do a random split, pages from the same client will leak into both train and test, inflating model performance.
# - A grouped split ensures that the model is evaluated on unseen clients, giving an honest estimate of how it will perform on future/new clients.
# 

# In[2]:


# ── Split design ───────────────────────────────────────────────
gss = GroupShuffleSplit(n_splits=1, test_size=0.2, random_state=42)
train_idx, test_idx = next(gss.split(df, groups=df["client_id"]))

df_train = df.iloc[train_idx].copy()
df_test = df.iloc[test_idx].copy()

# Verify no client overlap
train_clients = set(df_train["client_id"])
test_clients = set(df_test["client_id"])
overlap = train_clients.intersection(test_clients)

print(f"Train rows: {len(df_train):,} ({len(train_clients)} clients)")
print(f"Test rows: {len(df_test):,} ({len(test_clients)} clients)")
print(f"Client overlap between train/test: {len(overlap)}")


# ## 3. Train + compare vs my baseline
# 
# We will use safe historical features. 
# - **Missing values:** For `word_count`, we will add a binary `has_word_count` flag rather than blindly filling 0. `avg_position` = 0 means no data, so we will handle that too.
# - **Leakage check:** `trend_direction` and `trend_pct` are rigorously excluded. IDs are excluded.
# 

# In[3]:


# ── Feature Engineering ────────────────────────────────────────

def prepare_features(data):
    d = data.copy()

    # Missing value flags
    d["has_word_count"] = d["word_count"].notna().astype(int)
    d["word_count"] = d["word_count"].fillna(0)

    # 0 in avg_position means no data
    d["has_position_data"] = (d["avg_position"] > 0).astype(int)

    # Log transforms for heavy-tailed traffic
    d["log_impressions_90d"] = np.log1p(d["impressions_90d"])
    d["log_clicks_90d"] = np.log1p(d["clicks_90d"])

    # Drop rows without position data entirely if desired, but we can keep them 
    # since Logistic Regression can use the flag.
    return d

df_train_prep = prepare_features(df_train)
df_test_prep = prepare_features(df_test)

features = [
    "days_since_last_update", 
    "log_impressions_90d",
    "log_clicks_90d",
    "avg_position", 
    "has_position_data",
    "ctr",
    "word_count",
    "has_word_count",
    "content_age_days"
]
target = "is_declining"

X_train = df_train_prep[features]
y_train = df_train_prep[target]
X_test = df_test_prep[features]
y_test = df_test_prep[target]

# Train Logistic Regression
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

lr = LogisticRegression(random_state=42, max_iter=1000)
lr.fit(X_train_scaled, y_train)

# Predict probabilities
df_test["lr_prob"] = lr.predict_proba(X_test_scaled)[:, 1]

# Also fit Random Forest for comparison
rf = RandomForestClassifier(random_state=42, max_depth=6, n_estimators=100)
rf.fit(X_train, y_train)
df_test["rf_prob"] = rf.predict_proba(X_test)[:, 1]


# In[4]:


# ── Evaluation vs Baseline ─────────────────────────────────────
def precision_at_k(scores, labels, k):
    order = np.argsort(-np.asarray(scores))
    return np.asarray(labels)[order[:k]].mean()

k_values = [10, 20, 50, 100]
test_base_rate = df_test["is_declining"].mean()

results = []
for k in k_values:
    base_p = precision_at_k(df_test["baseline_score"].values, df_test["is_declining"].values, k)
    lr_p = precision_at_k(df_test["lr_prob"].values, df_test["is_declining"].values, k)
    rf_p = precision_at_k(df_test["rf_prob"].values, df_test["is_declining"].values, k)

    results.append({
        "K": k,
        "Baseline": base_p,
        "Logistic Regression": lr_p,
        "Random Forest": rf_p
    })

res_df = pd.DataFrame(results)
print(f"Test Base Rate: {test_base_rate:.3f}\n")
print("Precision@K on Test Set (Grouped by Client):")
print(res_df.to_string(index=False))

# Calculate supporting metrics like ROC-AUC
base_auc = roc_auc_score(y_test, df_test["baseline_score"])
lr_auc = roc_auc_score(y_test, df_test["lr_prob"])
rf_auc = roc_auc_score(y_test, df_test["rf_prob"])

print(f"\nROC-AUC:")
print(f"Baseline: {base_auc:.3f}")
print(f"LogReg:   {lr_auc:.3f}")
print(f"RF:       {rf_auc:.3f}")


# ## 4. Errors and interpretation
# 
# We'll look at the coefficients of the Logistic Regression model to understand what it leaned on, and then review a few false positives to see where it gets it wrong.
# 

# In[5]:


# ── Feature Importance (LogReg Coefficients) ───────────────────
coefs = pd.DataFrame({
    "Feature": features,
    "Coefficient": lr.coef_[0]
}).sort_values(by="Coefficient", key=abs, ascending=False)

print("Logistic Regression Coefficients (Scaled Features):")
print(coefs.to_string(index=False))


# **Interpretation:**
# - `log_impressions_90d` and `has_position_data` strongly drive predictions.
# - `days_since_last_update` has a positive coefficient, confirming the staleness hypothesis (older = more likely to decline).
# - `content_age_days` and `word_count` also play a role. 
# - There are no suspiciously perfect features here (which confirms no obvious target leakage).
# 

# In[6]:


# ── Error Analysis (False Positives) ───────────────────────────
# Let's find pages the model was VERY confident would decline, but didn't.
df_test["lr_prediction"] = (df_test["lr_prob"] > 0.5).astype(int)
false_positives = df_test[(df_test["lr_prediction"] == 1) & (df_test["is_declining"] == 0)]
top_fps = false_positives.sort_values(by="lr_prob", ascending=False).head(3)

print("Top False Positives (Predicted Decline, Actual Stable/Up):\n")
for _, row in top_fps.iterrows():
    print(f"Content ID: {row['content_id']}")
    print(f"Probability: {row['lr_prob']:.3f} | Actual: {row['is_declining']}")
    print(f"  Staleness: {row['days_since_last_update']} days")
    print(f"  Impressions (90d): {row['impressions_90d']:,}")
    print(f"  Avg Position: {row['avg_position']}")
    print("  ---")


# **Error Analysis:**
# The model sometimes confidently predicts a decline for pages that are extremely stale but have very high historical impressions. 
# These are likely "evergreen" pages that rank highly for high-volume head terms. They haven't been updated, but their authority or relevance remains so strong that they aren't losing traffic. The model expects staleness to cause decay, but for absolute top-tier content, staleness doesn't immediately hurt performance.
# 

# ## Self-check
# 
# Before you submit, confirm each line honestly:
# 
# - [x] Every section above is filled — markdown thinking AND the code that backs it
# - [x] The notebook runs top to bottom with no errors (Runtime → Run all)
# - [x] No client names, URLs, or private queries anywhere
# - [x] My claims use careful words: observed, measured, directional, decision-support
# - [x] Committed to my repo under `work/notebooks/` — then submit your repo URL on the card. Done.
# 
