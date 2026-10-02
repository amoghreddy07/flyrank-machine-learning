#!/usr/bin/env python
"""FlyRank ML Capstone — canonical reproducible pipeline (LANE 2: Refresh /
Content Opportunity Scoring).

What this script does (genuinely, end to end):
  1. Loads the 30,000-row anonymized modeling sample.
  2. Builds the documented 9-feature modeling frame (same as work/notebooks/
     w05_model.ipynb, w06_validation_audit.ipynb, w07_action_playbook.ipynb).
  3. Defines the label ``is_declining = (trend_direction == "down")``.
  4. Rebuilds the frozen hard-coded baseline (stale x visible x striking).
  5. Evaluates baseline vs Logistic Regression vs Random Forest on the SAME
     grouped-by-client holdout (GroupShuffleSplit by ``client_id``).
  6. Re-runs the age-ordered / time-aware validation proxy (ordered by
     ``content_age_days`` — NOT a strict calendar split; the sample has no
     calendar-date field).
  7. Generates the ranked editorial action queue with the w07 playbook logic.
  8. Writes regenerable artifacts to work/outputs/ (gitignored by design).
  9. Verifies every calculated metric against the independently recorded
     reference values (tolerance-checked, never forced).

Nothing here is hard-coded: every reported metric is calculated below.
Reference values are used ONLY as verification checks.

Run from the repository root (or anywhere — paths resolve from this file):
    python work/scripts/build_capstone.py
"""

from __future__ import annotations

import json
import os
import sys

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import GroupShuffleSplit
from sklearn.preprocessing import StandardScaler

# --------------------------------------------------------------------------
# Paths (resolve from this file so the script runs from any working dir)
# --------------------------------------------------------------------------
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
RAW_CSV = os.path.join(REPO_ROOT, "data", "raw", "content_refresh_anonymized.csv")
OUT_DIR = os.path.join(REPO_ROOT, "work", "outputs")
QUEUE_CSV = os.path.join(OUT_DIR, "content_action_queue.csv")
BASELINE_CSV = os.path.join(OUT_DIR, "baseline_action_score.csv")
METRICS_JSON = os.path.join(OUT_DIR, "capstone_metrics.json")

# --------------------------------------------------------------------------
# Fixed methodology (mirrors w05/w06/w07 — do not "tune to match")
# --------------------------------------------------------------------------
RANDOM_STATE = 42
TEST_SIZE = 0.2

FEATURES = [
    "days_since_last_update",
    "log_impressions_90d",
    "log_clicks_90d",
    "avg_position",
    "has_position_data",
    "ctr",
    "word_count",
    "has_word_count",
    "content_age_days",
]
TARGET = "is_declining"

# Columns that must NEVER appear in the feature matrix.
EXCLUDED_LEAKAGE_COLS = ["client_id", "content_id", "trend_direction", "trend_pct"]

# Reference values recorded independently in the lane notebooks (w05/w06).
# Verification ONLY — the pipeline calculates everything from scratch.
REFERENCE = {
    "grouped": {
        "baseline_p50": 0.400,
        "baseline_auc": 0.506,
        "rf_p50": 0.560,
        "rf_auc": 0.600,
        "lr_p50": 0.820,
        "lr_auc": 0.636,
        "test_base_rate": 0.511,
    },
    "age_ordered": {"lr_p50": 0.880, "lr_auc": 0.678},
}
TOL_P50 = 1e-9  # Precision@50 moves in 1/50 steps; any drift is a real change.
TOL_AUC = 0.01  # Small allowance for cross-version floating-point drift.
TOL_RATE = 0.001


def precision_at_k(scores, labels, k):
    """Of the top-K scored items, what fraction has label == 1?"""
    order = np.argsort(-np.asarray(scores))
    return float(np.asarray(labels)[order[:k]].mean())


def prepare_features(data):
    """Same feature engineering as w05/w06/w07 (missingness flags + logs)."""
    d = data.copy()
    d["has_word_count"] = d["word_count"].notna().astype(int)
    d["word_count"] = d["word_count"].fillna(0)
    # avg_position == 0 means "no data" (see docs/data-dictionary.md).
    d["has_position_data"] = (d["avg_position"] > 0).astype(int)
    d["log_impressions_90d"] = np.log1p(d["impressions_90d"])
    d["log_clicks_90d"] = np.log1p(d["clicks_90d"])
    return d


def build_baseline_score(d):
    """Frozen w04 rule: stale x visible x striking-distance x impressions."""
    is_stale = (d["days_since_last_update"] >= 91).astype(int)
    is_visible = (d["impressions_90d"] >= 100).astype(int)
    is_striking = ((d["avg_position"] >= 4) & (d["avg_position"] <= 20)).astype(int)
    return is_stale * is_visible * is_striking * d["impressions_90d"]


def assign_action(row):
    """w07 playbook mapping: probability + visibility -> action + reason."""
    if row["decline_probability"] > 0.75 and row["impressions_90d"] > 1000:
        return (
            "High Priority Refresh",
            f"High decline risk ({row['decline_probability']:.1%}); "
            f"strong historical impressions ({row['impressions_90d']:.0f})",
        )
    if row["decline_probability"] > 0.75:
        return (
            "Standard Refresh Review",
            f"High decline risk ({row['decline_probability']:.1%}); lower volume",
        )
    if row["impressions_90d"] > 5000 and row["days_since_last_update"] > 180:
        return (
            "Preventative Update",
            f"Stale ({row['days_since_last_update']:.0f} days) but high traffic; "
            "refresh before decay",
        )
    return "Monitor", "Stable or low impact"


def check(name, calculated, expected, tol):
    ok = abs(calculated - expected) <= tol
    print(f"  [{'OK' if ok else 'MISMATCH'}] {name}: calculated={calculated:.3f} "
          f"reference={expected:.3f} (tol={tol})")
    return ok


def main():
    print("=" * 70)
    print("FlyRank Capstone — reproducible pipeline (30k anonymized sample)")
    print("=" * 70)

    # -- 1. Load -----------------------------------------------------------
    df = pd.read_csv(RAW_CSV)
    print(f"Loaded {len(df):,} rows x {df.shape[1]} columns from "
          "data/raw/content_refresh_anonymized.csv")

    # -- 2. Label ----------------------------------------------------------
    df[TARGET] = (df["trend_direction"] == "down").astype(int)
    print(f"Overall decline base rate: {df[TARGET].mean():.3f}")

    # -- 3. Features + leakage audit ---------------------------------------
    df_prep = prepare_features(df)
    for col in EXCLUDED_LEAKAGE_COLS:
        assert col not in FEATURES, f"LEAKAGE: {col} found in FEATURES!"
    overlap = set(EXCLUDED_LEAKAGE_COLS) & set(df_prep[FEATURES].columns)
    assert not overlap, f"LEAKAGE: excluded columns in matrix: {overlap}"
    print(f"Feature matrix: {len(FEATURES)} features; leakage audit passed "
          f"(excluded {EXCLUDED_LEAKAGE_COLS})")

    # -- 4. Baseline -------------------------------------------------------
    df_prep["baseline_score"] = build_baseline_score(df_prep)

    # -- 5-7. Grouped-by-client holdout, train, evaluate -------------------
    gss = GroupShuffleSplit(n_splits=1, test_size=TEST_SIZE,
                            random_state=RANDOM_STATE)
    train_idx, test_idx = next(gss.split(df_prep, groups=df_prep["client_id"]))
    df_train = df_prep.iloc[train_idx]
    df_test = df_prep.iloc[test_idx]
    assert not (set(df_train["client_id"]) & set(df_test["client_id"])), \
        "Client overlap between train and test!"
    X_train, y_train = df_train[FEATURES], df_train[TARGET]
    X_test, y_test = df_test[FEATURES], df_test[TARGET]
    print(f"Grouped split: train {len(df_train):,} rows "
          f"({df_train['client_id'].nunique()} clients) / test {len(df_test):,} "
          f"rows ({df_test['client_id'].nunique()} clients), overlap=0")

    scaler = StandardScaler()
    lr = LogisticRegression(random_state=RANDOM_STATE, max_iter=1000)
    lr.fit(scaler.fit_transform(X_train), y_train)
    lr_prob = lr.predict_proba(scaler.transform(X_test))[:, 1]

    rf = RandomForestClassifier(random_state=RANDOM_STATE, max_depth=6,
                                n_estimators=100)
    rf.fit(X_train, y_train)
    rf_prob = rf.predict_proba(X_test)[:, 1]

    base_score = df_test["baseline_score"].to_numpy()
    y_true = y_test.to_numpy()

    metrics = {
        "n_rows": int(len(df_prep)),
        "n_train": int(len(df_train)),
        "n_test": int(len(df_test)),
        "n_train_clients": int(df_train["client_id"].nunique()),
        "n_test_clients": int(df_test["client_id"].nunique()),
        "test_base_rate": float(y_true.mean()),
        "baseline_p50": precision_at_k(base_score, y_true, 50),
        "baseline_auc": float(roc_auc_score(y_true, base_score)),
        "lr_p50": precision_at_k(lr_prob, y_true, 50),
        "lr_auc": float(roc_auc_score(y_true, lr_prob)),
        "rf_p50": precision_at_k(rf_prob, y_true, 50),
        "rf_auc": float(roc_auc_score(y_true, rf_prob)),
    }

    # -- 8. Age-ordered / time-aware proxy ----------------------------------
    # No calendar-date field exists in the sample, so "time-aware" means
    # ordered by content_age_days (oldest first): train older 80%, test
    # newest 20%. This is a proxy, NOT a strict calendar split.
    df_time = df_prep.sort_values("content_age_days",
                                  ascending=False).reset_index(drop=True)
    cut = int(len(df_time) * 0.8)
    tr, te = df_time.iloc[:cut], df_time.iloc[cut:].copy()
    lr_t = LogisticRegression(random_state=RANDOM_STATE, max_iter=1000)
    sc_t = StandardScaler()
    lr_t.fit(sc_t.fit_transform(tr[FEATURES]), tr[TARGET])
    te_prob = lr_t.predict_proba(sc_t.transform(te[FEATURES]))[:, 1]
    metrics["age_lr_p50"] = precision_at_k(te_prob, te[TARGET].to_numpy(), 50)
    metrics["age_lr_auc"] = float(roc_auc_score(te[TARGET].to_numpy(), te_prob))
    print(f"Age-ordered proxy: train {len(tr):,} (older) / test {len(te):,} "
          "(newer) by content_age_days")

    # -- 9. Ranked action queue (w07 logic on the proxy-test frame) --------
    te["decline_probability"] = te_prob
    te[["recommended_action", "reason_code"]] = te.apply(
        assign_action, axis=1, result_type="expand")
    queue = te[te["recommended_action"] != "Monitor"].sort_values(
        "decline_probability", ascending=False).reset_index(drop=True)
    queue["rank"] = np.arange(1, len(queue) + 1)

    os.makedirs(OUT_DIR, exist_ok=True)
    queue[["rank", "decline_probability", "recommended_action",
           "reason_code"]].to_csv(QUEUE_CSV, index=False)

    # Baseline ranked list (w04 logic, full sample, baseline-score order).
    ranked = df_prep.sort_values("baseline_score",
                                 ascending=False).reset_index(drop=True)
    ranked["rank"] = np.arange(1, len(ranked) + 1)
    ranked[["rank", "baseline_score"]].to_csv(BASELINE_CSV, index=False)

    metrics["queue_rows"] = int(len(queue))
    with open(METRICS_JSON, "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)

    # -- Final report -------------------------------------------------------
    print("-" * 70)
    print(f"Dataset: {metrics['n_rows']:,} rows | "
          f"split {metrics['n_train']:,}/{metrics['n_test']:,} rows, "
          f"{metrics['n_train_clients']}/{metrics['n_test_clients']} clients")
    print(f"Test base rate: {metrics['test_base_rate']:.3f}")
    print(f"Baseline:            P@50={metrics['baseline_p50']:.3f} "
          f"ROC-AUC={metrics['baseline_auc']:.3f}")
    print(f"Logistic Regression: P@50={metrics['lr_p50']:.3f} "
          f"ROC-AUC={metrics['lr_auc']:.3f}")
    print(f"Random Forest:       P@50={metrics['rf_p50']:.3f} "
          f"ROC-AUC={metrics['rf_auc']:.3f}")
    print(f"Age-ordered proxy LR: P@50={metrics['age_lr_p50']:.3f} "
          f"ROC-AUC={metrics['age_lr_auc']:.3f}")
    print(f"Action queue: {metrics['queue_rows']:,} rows "
          f"({queue['recommended_action'].value_counts().to_dict()})")
    print(f"Outputs: {QUEUE_CSV}\n         {BASELINE_CSV}\n         {METRICS_JSON}")

    # -- Verification (reference checks only — never forced) ----------------
    print("-" * 70)
    print("Verification against independently recorded references:")
    ref = REFERENCE["grouped"]
    ok = True
    ok &= check("grouped baseline P@50", metrics["baseline_p50"],
                ref["baseline_p50"], TOL_P50)
    ok &= check("grouped baseline ROC-AUC", metrics["baseline_auc"],
                ref["baseline_auc"], TOL_AUC)
    ok &= check("grouped RF P@50", metrics["rf_p50"], ref["rf_p50"], TOL_P50)
    ok &= check("grouped RF ROC-AUC", metrics["rf_auc"], ref["rf_auc"], TOL_AUC)
    ok &= check("grouped LR P@50", metrics["lr_p50"], ref["lr_p50"], TOL_P50)
    ok &= check("grouped LR ROC-AUC", metrics["lr_auc"], ref["lr_auc"], TOL_AUC)
    ok &= check("grouped test base rate", metrics["test_base_rate"],
                ref["test_base_rate"], TOL_RATE)
    ok &= check("age-ordered LR P@50", metrics["age_lr_p50"],
                REFERENCE["age_ordered"]["lr_p50"], TOL_P50)
    ok &= check("age-ordered LR ROC-AUC", metrics["age_lr_auc"],
                REFERENCE["age_ordered"]["lr_auc"], TOL_AUC)

    print("-" * 70)
    print("Top-10 queue preview (public-safe: rank/score/action/reason only):")
    for _, r in queue.head(10).iterrows():
        print(f"  {int(r['rank']):>3} | {r['decline_probability']:.3f} | "
              f"{r['recommended_action']} | {r['reason_code']}")

    if not ok:
        print("VERIFICATION MISMATCH: one or more calculated metrics differ "
              "from the recorded references. Methodology was NOT altered to "
              "force a match — investigate before updating any claims.")
        return 1
    print("All verification checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
