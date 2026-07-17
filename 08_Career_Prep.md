# Career Prep Kit
## Resume Bullets, Interview Questions, and STAR Answers for the E20 Project

---

## A. Resume Bullet Points (pick 3-5 based on role you're targeting)

**For Business Analyst / Consulting roles:**
- Led an end-to-end market research and business analytics engagement on India's E20 petrol transition, designing and executing a 450-respondent stratified survey and 30+ stakeholder interviews across 4 city tiers.
- Built a full analytics pipeline (Excel → SQL → Python → Power BI) to diagnose consumer trust and adoption drivers for a national policy rollout, translating findings into 7 prioritized, costed recommendations.
- Applied statistical hypothesis testing (chi-square, t-tests, logistic regression) in Python to validate 7 business hypotheses on consumer adoption behavior, identifying vehicle age and dealer communication quality as the strongest predictors of trust.
- Designed a K-Means customer segmentation model identifying 4 actionable personas, including a 37%-sized "Undecided Middle" segment representing the highest-ROI intervention target.
- Developed a 3-page Power BI dashboard suite (Executive, Operational, Storytelling) with 8+ custom DAX measures to track adoption KPIs in near real time for OMC and policymaker stakeholders.
- Conducted root cause analysis (Fishbone/5-Why) and SWOT/PESTLE/competitor benchmarking (Brazil ethanol, US E15) to reframe a perceived "fuel technology problem" as a communication-infrastructure problem, redirecting recommended investment toward dealer training and OEM co-messaging.
- Delivered a 13-slide executive presentation and full consulting deliverable pack to simulate a real OMC/MoPNG engagement, including cost-benefit analysis and a phased 12-month implementation roadmap.

**For Data Analyst roles (more technical framing):**
- Cleaned and engineered a 450-row survey dataset in Python (pandas), handling missing values, categorical standardization, and range validation before downstream analysis.
- Built and validated a logistic regression model to predict E20 adoption likelihood from trust, understanding, and concern features, plus a K-Means clustering model for customer segmentation.
- Designed a normalized SQL schema (star schema: dim_respondent, fact_survey_response, dim_dealer, fact_dealer_survey) with 8 analytical queries supporting BI dashboard consumption.

---

## B. Interview Questions You Should Expect (and be ready to defend)

1. **"Walk me through this project end to end."** → Use the STAR summary below; lead with the business problem, not the tools.
2. **"Why did you choose a stratified sample instead of simple random sampling?"** → Ensures representation across city tiers and vehicle age bands, which you hypothesized (and later confirmed) were the strongest segmentation variables — random sampling risked under-representing Tier-3/Rural respondents.
3. **"How did you validate your hypotheses statistically — walk me through one test."** → Pick H2 (chi-square, vehicle age vs. complaint rate) and explain the test, the p-value threshold, and what a significant result implies for the business.
4. **"Your sample is only 450 — how confident are you in the findings?"** → ±4.6% margin of error at 95% CI is disclosed as a limitation; this is a rapid diagnostic, not a national census, and you'd recommend a larger wave before nationwide investment decisions.
5. **"How did you decide on 4 customer segments and not 3 or 5?"** → In a real engagement, you'd run the elbow method / silhouette score to pick k; be honest that this project uses an illustrative k=4 chosen for business interpretability (4 clean, actionable personas) — a great chance to show self-awareness rather than overclaiming rigor.
6. **"What was the single most important insight, and why?"** → The Awareness-Understanding gap (Finding 1) — it reframes the whole intervention strategy from "more advertising" to "better point-of-sale explanation."
7. **"If a dealer or OEM stakeholder pushed back on your recommendation, how would you respond?"** → Show you can defend with data (e.g., dealer training cost R1 vs. benefit of reduced complaint-handling and warranty disputes) while remaining open to iterating based on their operational constraints.
8. **"What would you do differently with more time/budget?"** → Larger, nationally representative sample; longitudinal tracking instead of a single wave; actual odometer/fuel-log data instead of self-reported mileage perception (addresses H3 more rigorously).
9. **"How does this project show consulting skills, not just analytics skills?"** → Emphasize the frameworks (SWOT, PESTLE, root cause, cost-benefit, stakeholder mapping) and the fact that the deliverable is structured as a client engagement, not a dashboard exercise.
10. **"Why should we trust your cost-benefit numbers?"** → Be upfront: they're illustrative planning placeholders explicitly caveated as such — in a real engagement, they'd be built from actual OMC financials. This honesty is itself a strong interview signal.

---

## C. STAR Method Answers

### STAR 1: End-to-end project overview
**Situation:** India accelerated its E20 ethanol-blended petrol rollout to 2025, but adoption trust and understanding lagged the policy timeline, creating friction across OMCs, OEMs, dealers, and consumers.
**Task:** I set out to run this as a full consulting engagement — diagnose the root causes of adoption resistance and deliver a prioritized, data-backed roadmap, not just a survey summary.
**Action:** I designed a stratified 450-respondent survey plus 30+ stakeholder interviews, built a SQL data model, cleaned and analyzed the data in Python (hypothesis testing, logistic regression, K-Means segmentation), and built a 3-page Power BI dashboard suite. I applied SWOT, PESTLE, root cause, and competitor benchmarking frameworks to translate findings into 7 costed recommendations and a 12-month roadmap.
**Result:** The analysis reframed the core issue from a perceived "fuel technology problem" to a "communication infrastructure problem," redirecting recommended investment toward dealer training and OEM co-branded messaging — the kind of insight that changes where a real client would spend their budget.

### STAR 2: Handling a statistical/methodological challenge
**Situation:** Self-reported mileage-drop data is highly susceptible to perception bias — I couldn't just take survey answers at face value.
**Task:** I needed to distinguish genuine technical complaints from perception-driven ones without independent odometer data.
**Action:** I cross-tabulated perceived mileage drop against vehicle age band and used the resulting pattern (older vehicles disproportionately reporting issues) plus dealer/pump attendant interviews as a triangulation check, and explicitly flagged this as a modeled hypothesis (H3) requiring follow-up validation with real fuel-log data rather than presenting it as a confirmed fact.
**Result:** This produced a defensible, appropriately caveated insight — and demonstrated methodological honesty rather than overclaiming from self-report data alone, which is exactly the instinct a consulting reviewer is testing for.

### STAR 3: Turning data into a business recommendation
**Situation:** The segmentation analysis surfaced a large (37%) "Undecided Middle" segment sitting between committed adopters and hard resisters.
**Task:** Translate that statistical segment into something a marketing or policy team could act on.
**Action:** I profiled the segment's specific trust and concern scores, compared it against the other 3 personas, and built a targeted digital campaign recommendation (R4) explicitly sized and sequenced as the fastest-payback initiative in the cost-benefit analysis.
**Result:** This became the highest-priority "quick win" recommendation in the final roadmap and executive deck — showing the ability to move from a clustering output to a resourced, prioritized business action.

---
*Document 8 of 9.*
