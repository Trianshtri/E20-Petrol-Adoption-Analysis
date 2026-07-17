"""
E20 Petrol Adoption — Python Analysis Layer
Covers: Data Cleaning -> EDA -> Statistical Hypothesis Testing -> Customer Segmentation
Stack: pandas, numpy, scipy, scikit-learn, matplotlib/seaborn
Input: consumer_survey_raw.csv (exported from SQL fact_survey_response JOIN dim_respondent)
"""

import pandas as pd
import numpy as np
from scipy import stats
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import matplotlib.pyplot as plt
import seaborn as sns

# ============================================================
# 1. DATA CLEANING
# ============================================================

def load_and_clean(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)

    # 1.1 Standardize column names
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]

    # 1.2 Drop exact duplicate submissions (device/timestamp based dedup done upstream;
    #     this is a content-based safety net)
    before = len(df)
    df = df.drop_duplicates(subset=[c for c in df.columns if c != "response_id"])
    print(f"Removed {before - len(df)} duplicate rows")

    # 1.3 Handle missing values
    likert_cols = ["understanding_score", "concern_engine_damage", "concern_mileage_loss",
                   "concern_warranty", "trust_govt", "trust_oem", "trust_dealer",
                   "trust_social_media", "nps_score"]
    for col in likert_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
            df[col] = df[col].fillna(df[col].median())

    # 1.4 Standardize categorical text (trim, title-case, fix known typos)
    cat_cols = df.select_dtypes(include="object").columns
    for col in cat_cols:
        df[col] = df[col].astype(str).str.strip()

    # 1.5 Validate ranges — flag out-of-range Likert responses (should be 1-5, or 0-10 for NPS)
    for col in [c for c in likert_cols if c != "nps_score"]:
        invalid = ~df[col].between(1, 5)
        if invalid.any():
            print(f"WARNING: {invalid.sum()} out-of-range values in {col} — clipped to [1,5]")
            df[col] = df[col].clip(1, 5)
    if "nps_score" in df.columns:
        df["nps_score"] = df["nps_score"].clip(0, 10)

    # 1.6 Convert boolean-like text fields to actual booleans
    bool_map = {"true": True, "false": False, "yes": True, "no": False,
               "1": True, "0": False}
    for col in ["aware_of_e20", "seen_signage", "attendant_explained",
               "knowingly_purchased_e20", "engine_issue_reported"]:
        if col in df.columns:
            df[col] = df[col].astype(str).str.lower().map(bool_map)

    # 1.7 Outlier check on numeric mileage-drop-derived fields (if % numeric captured)
    # (kept illustrative — actual mileage delta would come from odometer/fuel-log data)

    print(f"Final cleaned dataset: {len(df)} rows, {df.shape[1]} columns")
    return df


# ============================================================
# 2. EXPLORATORY DATA ANALYSIS (EDA)
# ============================================================

def run_eda(df: pd.DataFrame):
    print("\n--- Summary Statistics ---")
    print(df.describe(include="all").T)

    print("\n--- Awareness Rate by City Tier ---")
    print(df.groupby("city_tier")["aware_of_e20"].mean().round(3) * 100)

    print("\n--- Sentiment Distribution ---")
    print(df["overall_sentiment"].value_counts(normalize=True).round(3) * 100)

    # Visual 1: Awareness by city tier
    plt.figure(figsize=(7, 4))
    sns.barplot(data=df, x="city_tier", y="aware_of_e20", estimator=np.mean)
    plt.title("E20 Awareness Rate by City Tier")
    plt.ylabel("Awareness Rate")
    plt.tight_layout()
    plt.savefig("eda_awareness_by_citytier.png", dpi=150)
    plt.close()

    # Visual 2: Trust score comparison (grouped bar)
    trust_cols = ["trust_govt", "trust_oem", "trust_dealer", "trust_social_media"]
    trust_means = df[trust_cols].mean()
    plt.figure(figsize=(7, 4))
    trust_means.plot(kind="bar", color=["#1f77b4", "#2ca02c", "#ff7f0e", "#d62728"])
    plt.title("Average Trust Score by Information Source")
    plt.ylabel("Mean Trust (1-5)")
    plt.tight_layout()
    plt.savefig("eda_trust_by_source.png", dpi=150)
    plt.close()

    # Visual 3: Complaint rate by vehicle age band
    plt.figure(figsize=(7, 4))
    sns.barplot(data=df, x="vehicle_year_band", y="engine_issue_reported", estimator=np.mean)
    plt.title("Reported Engine Issue Rate by Vehicle Age Band")
    plt.tight_layout()
    plt.savefig("eda_complaints_by_vehicle_age.png", dpi=150)
    plt.close()


# ============================================================
# 3. STATISTICAL HYPOTHESIS TESTING
# ============================================================

def test_h1_awareness_by_city(df):
    """H1: Awareness differs significantly by city tier (Chi-square test of independence)."""
    table = pd.crosstab(df["city_tier"], df["aware_of_e20"])
    chi2, p, dof, expected = stats.chi2_contingency(table)
    print(f"H1 (Awareness x City Tier): chi2={chi2:.2f}, p={p:.4f} -> "
          f"{'SIGNIFICANT' if p < 0.05 else 'not significant'}")
    return chi2, p


def test_h2_complaints_by_vehicle_age(df):
    """H2: Complaint rate differs by vehicle age band (Chi-square)."""
    table = pd.crosstab(df["vehicle_year_band"], df["engine_issue_reported"])
    chi2, p, dof, expected = stats.chi2_contingency(table)
    print(f"H2 (Complaints x Vehicle Age): chi2={chi2:.2f}, p={p:.4f} -> "
          f"{'SIGNIFICANT' if p < 0.05 else 'not significant'}")
    return chi2, p


def test_h4_dealer_explanation_effect(df):
    """H4: Consumers who received a dealer explanation show higher trust (independent t-test)."""
    explained = df.loc[df["attendant_explained"] == True, "trust_dealer"]
    not_explained = df.loc[df["attendant_explained"] == False, "trust_dealer"]
    t_stat, p = stats.ttest_ind(explained, not_explained, equal_var=False, nan_policy="omit")
    print(f"H4 (Dealer Explanation -> Trust): t={t_stat:.2f}, p={p:.4f} -> "
          f"{'SIGNIFICANT' if p < 0.05 else 'not significant'}")
    return t_stat, p


def test_h6_trust_source_comparison(df):
    """H6: Trust in OEM > trust in Govt/Dealer (paired t-test)."""
    t_stat, p = stats.ttest_rel(df["trust_oem"], df["trust_govt"], nan_policy="omit")
    print(f"H6 (OEM vs Govt trust): t={t_stat:.2f}, p={p:.4f} -> "
          f"{'SIGNIFICANT' if p < 0.05 else 'not significant'}")
    return t_stat, p


def logistic_adoption_drivers(df):
    """Logistic regression: which factors predict knowingly_purchased_e20 (adoption)?"""
    features = ["understanding_score", "trust_oem", "trust_dealer", "trust_govt",
               "concern_engine_damage", "concern_mileage_loss"]
    model_df = df.dropna(subset=features + ["knowingly_purchased_e20"])
    X = model_df[features]
    y = model_df["knowingly_purchased_e20"].astype(int)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)
    scaler = StandardScaler()
    X_train_s = scaler.fit_transform(X_train)
    X_test_s = scaler.transform(X_test)

    clf = LogisticRegression(max_iter=1000)
    clf.fit(X_train_s, y_train)

    coef_table = pd.Series(clf.coef_[0], index=features).sort_values(key=abs, ascending=False)
    print("\n--- Logistic Regression: Adoption Drivers (standardized coefficients) ---")
    print(coef_table.round(3))
    print("\n--- Classification Report ---")
    print(classification_report(y_test, clf.predict(X_test_s)))
    return clf, coef_table


# ============================================================
# 4. CUSTOMER SEGMENTATION (K-Means)
# ============================================================

def segment_customers(df, n_clusters=4):
    """
    Segment consumers into personas using trust, concern, and understanding features.
    Expected personas (post-labeling):
      - Skeptical Traditionalist (low trust, high concern)
      - Eco-Pragmatist (high understanding, low concern)
      - Uninformed Majority (low understanding, moderate everything)
      - Confident Adopter (high trust, low concern, high understanding)
    """
    features = ["understanding_score", "trust_govt", "trust_oem", "trust_dealer",
               "concern_engine_damage", "concern_mileage_loss", "concern_warranty", "nps_score"]
    seg_df = df.dropna(subset=features).copy()

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(seg_df[features])

    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    seg_df["segment"] = kmeans.fit_predict(X_scaled)

    profile = seg_df.groupby("segment")[features].mean().round(2)
    profile["segment_size"] = seg_df["segment"].value_counts()
    profile["segment_pct"] = (profile["segment_size"] / len(seg_df) * 100).round(1)

    print("\n--- Segment Profiles ---")
    print(profile)

    return seg_df, profile


# ============================================================
# 5. MAIN PIPELINE
# ============================================================

if __name__ == "__main__":
    df = load_and_clean("consumer_survey_raw.csv")
    run_eda(df)

    print("\n=== HYPOTHESIS TESTING ===")
    test_h1_awareness_by_city(df)
    test_h2_complaints_by_vehicle_age(df)
    test_h4_dealer_explanation_effect(df)
    test_h6_trust_source_comparison(df)

    print("\n=== ADOPTION DRIVER MODEL ===")
    logistic_adoption_drivers(df)

    print("\n=== CUSTOMER SEGMENTATION ===")
    seg_df, profile = segment_customers(df)

    # Export cleaned + segmented data for Power BI
    seg_df.to_csv("e20_survey_cleaned_segmented.csv", index=False)
    print("\nExported: e20_survey_cleaned_segmented.csv (ready for Power BI import)")
