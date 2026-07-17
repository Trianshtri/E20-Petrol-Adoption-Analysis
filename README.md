# Market Research & Business Analytics for E20 Petrol Adoption in India

A full-cycle business consulting engagement (simulated) diagnosing consumer trust and adoption barriers around India's E20 (20% ethanol-blended petrol) rollout, and delivering a prioritized, data-backed roadmap — executed the way a consulting analytics team (e.g., ZS, Deloitte, EY, Accenture, Bain CN) would run it: primary research → SQL data model → Python statistical analysis → Power BI dashboards → executive recommendations.

## Why this project

India moved its ethanol-blending target from 2030 to 2025. Adoption at the pump has outpaced public understanding and trust. This project asks: **why**, and **what should OMCs, OEMs, and policymakers do about it** — backed by primary research, not assumption.

## Repository Structure

```
├── 01_Business_Strategy_Document.md   # Problem statement, objectives, scope, stakeholders,
│                                       # hypotheses, SWOT, PESTLE, competitor & root cause
│                                       # analysis, insights, recommendations, roadmap, risks
├── 02_Research_Instruments.md         # 48-question consumer survey + 3 interview guides
│                                       # (consumer, dealer, petrol pump attendant)
├── 03_database_design.sql             # Star-schema SQL design, seed data, 8 analytical queries
├── 04_python_analysis.py              # Data cleaning, EDA, hypothesis testing (chi-sq, t-test),
│                                       # logistic regression, K-Means segmentation
├── 05_PowerBI_Dashboard_Design.md     # KPI framework, DAX measures, 3-page dashboard layout
├── 06_Excel_Data_Structure.xlsx       # Data dictionary, sample raw data, field tracker, live KPI sheet
├── 07_Executive_Presentation.pptx     # 13-slide C-suite / client-ready deck
├── 08_Career_Prep.md                  # Resume bullets, interview Q&A, STAR answers
└── README.md
```

## Methodology at a glance

| Stage | Tool | Output |
|---|---|---|
| Field data capture | Excel | Structured raw survey + field tracker |
| Data modeling & storage | SQL (star schema) | `dim_respondent`, `fact_survey_response`, `dim_dealer`, `fact_dealer_survey` |
| Cleaning, stats, ML | Python (pandas, scipy, scikit-learn) | Hypothesis test results, adoption-driver model, 4-persona segmentation |
| Visualization & storytelling | Power BI | Executive, Operational, and Storytelling dashboards |

**Sample:** 450 stratified consumer survey responses (city tier × vehicle type × vehicle age) + 30+ semi-structured interviews (consumers, dealers, pump attendants). ±4.6% margin of error at 95% CI — explicitly scoped as a rapid diagnostic, not a national census.

## Key Findings (illustrative — see Document 1 for full detail)

1. **The Awareness Illusion:** ~82% awareness vs. ~34% correct understanding of E20 — a communication-depth problem, not a reach problem.
2. **Trust hierarchy:** OEM messaging is trusted more than government or dealer messaging — implying OEM co-branded communication should lead future campaigns.
3. **The Undecided Middle:** A ~37% segment is neither adopter nor resister — the single highest-ROI target for intervention.
4. **Vehicle age is the strongest predictor** of complaint/resistance — stronger than income or city tier.

## Hypotheses tested

7 hypotheses (H1–H7) covering awareness-by-geography, complaint-by-vehicle-age, perception-vs-reality on mileage, dealer-explanation effects on trust, price sensitivity, source trust ranking, and segment sizing — see `01_Business_Strategy_Document.md` §6 and `04_python_analysis.py` for test implementation.

## Limitations (stated up front, as a real engagement would)

- Sample is a rapid diagnostic (n=450), not a nationally representative census.
- Mileage-impact data is self-reported perception, not independently measured odometer/fuel-log data (flagged explicitly as H3, requiring follow-up validation).
- Cost-benefit figures are illustrative planning placeholders pending real OMC financial data.

## How to reproduce

1. Load `03_database_design.sql` into PostgreSQL/MySQL and seed with your survey export.
2. Export the joined dataset to `consumer_survey_raw.csv`.
3. Run `04_python_analysis.py` to clean, test hypotheses, and segment respondents → outputs `e20_survey_cleaned_segmented.csv`.
4. Import that CSV into Power BI Desktop and build the model per `05_PowerBI_Dashboard_Design.md`.

## Author

Business Analyst / Consulting portfolio project — see `08_Career_Prep.md` for how this maps to resume bullets and interview talking points.
