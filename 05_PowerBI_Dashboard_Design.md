# Power BI Dashboard Suite — Design Specification
## E20 Petrol Adoption Analytics

Data model: import `e20_survey_cleaned_segmented.csv` (from Python pipeline) + `dim_dealer` / `fact_dealer_survey` from SQL. Star schema: `dim_respondent` (1) → (many) `fact_survey_response`; `dim_dealer` (1) → (many) `fact_dealer_survey`.

---

## 1. KPI Framework

| KPI | Definition | Target |
|---|---|---|
| Awareness Rate | % respondents aware_of_e20 = TRUE | >85% |
| Understanding Index | Avg understanding_score (1-5) | >3.5 |
| Adoption Rate | % knowingly_purchased_e20 = TRUE | >70% |
| Trust Composite Score | Avg of trust_govt/oem/dealer (weighted) | >3.5 |
| Complaint Rate | % engine_issue_reported = TRUE | <10% |
| NPS (E20 confidence) | Standard NPS calc on nps_score | >0 (positive) |
| Undecided Middle Size | % segment = 'Undecided Middle' | Track for conversion |
| Dealer Training Coverage | % dealers received_omc_training = TRUE | 100% |

## 2. DAX Measures

```dax
Awareness Rate =
DIVIDE(
    CALCULATE(COUNTROWS(fact_survey_response), fact_survey_response[aware_of_e20] = TRUE),
    COUNTROWS(fact_survey_response)
)

Understanding Index = AVERAGE(fact_survey_response[understanding_score])

Adoption Rate =
DIVIDE(
    CALCULATE(COUNTROWS(fact_survey_response), fact_survey_response[knowingly_purchased_e20] = TRUE),
    COUNTROWS(fact_survey_response)
)

Trust Composite Score =
( AVERAGE(fact_survey_response[trust_govt])
+ AVERAGE(fact_survey_response[trust_oem]) * 1.2   -- OEM weighted higher per H6 finding
+ AVERAGE(fact_survey_response[trust_dealer]) ) / 3.2

Complaint Rate =
DIVIDE(
    CALCULATE(COUNTROWS(fact_survey_response), fact_survey_response[engine_issue_reported] = TRUE),
    COUNTROWS(fact_survey_response)
)

NPS Score =
VAR Promoters = CALCULATE(COUNTROWS(fact_survey_response), fact_survey_response[nps_score] >= 9)
VAR Detractors = CALCULATE(COUNTROWS(fact_survey_response), fact_survey_response[nps_score] <= 6)
VAR Total = COUNTROWS(fact_survey_response)
RETURN DIVIDE(Promoters - Detractors, Total) * 100

Undecided Middle % =
DIVIDE(
    CALCULATE(COUNTROWS(fact_survey_response), fact_survey_response[segment_label] = "Undecided Middle"),
    COUNTROWS(fact_survey_response)
)

MoM Awareness Change =
VAR CurrentM = [Awareness Rate]
VAR PriorM = CALCULATE([Awareness Rate], DATEADD(dim_date[Date], -1, MONTH))
RETURN CurrentM - PriorM

Complaint Rate by Vehicle Age Band =
CALCULATE([Complaint Rate], ALLEXCEPT(dim_respondent, dim_respondent[vehicle_year_band]))
```

## 3. Dashboard Layout — Executive Dashboard (Page 1)

**Purpose:** 10-second read for MoPNG/OMC leadership.

- **Top strip (KPI cards, 5 across):** Awareness Rate | Adoption Rate | Trust Composite | Complaint Rate | NPS
- **Left panel:** Donut chart — Sentiment Distribution (Very Positive → Very Negative)
- **Center:** Map visual — Adoption Rate by City (bubble size = sample count, color = adoption %)
- **Right panel:** Bar chart — Segment sizes (Confident Adopter / Undecided Middle / Skeptical Traditionalist / Uninformed Majority)
- **Bottom strip:** Trend line — Awareness & Adoption Rate over survey weeks (if longitudinal tracking enabled)
- **Slicers:** City Tier, Vehicle Type, Vehicle Age Band (top-right, persistent across pages)

## 4. Dashboard Layout — Operational / Diagnostic Dashboard (Page 2)

**Purpose:** For OMC operations & dealer network teams.

- Table: Dealer-level complaint volume vs. training coverage (conditional formatting: red if complaints high AND training = No)
- Bar chart: Top concern drivers (Engine Damage / Mileage Loss / Warranty) ranked by mean score
- Scatter plot: Trust in Dealer (x) vs. NPS Score (y), colored by attendant_explained (tests H4 visually)
- Chi-square/statistical annotations panel (text card summarizing H1, H2, H4, H6 results with p-values)

## 5. Dashboard Layout — Storytelling Dashboard (Page 3, for stakeholder narrative walkthrough)

**Purpose:** Guided narrative for a workshop/presentation setting — built with bookmarks and a "story" button sequence.

1. **Bookmark 1 — "The Awareness Illusion":** Highlight Awareness Rate (high) next to Understanding Index (low) — visual gap callout
2. **Bookmark 2 — "The Undecided Middle":** Segment donut zoomed into the 35-40% undecided slice with annotation
3. **Bookmark 3 — "Where Trust Breaks":** Trust Composite by source, OEM highlighted vs. Government/Dealer
4. **Bookmark 4 — "The Real Risk Segment":** Complaint rate by vehicle age band, pre-2018 fleet highlighted
5. **Bookmark 5 — "The Fix":** Recommendation cards mapped to KPI movement (R1→Trust, R4→Undecided Middle conversion)

Use **Power BI bookmarks + a button-based "Next" navigation** to walk an executive audience through the insight arc rather than a static grid.

## 6. Where Excel / SQL / Python / Power BI Are Used (Tooling Map)

| Stage | Tool | Why |
|---|---|---|
| Raw survey capture, quick pivot checks, field team tracker | **Excel** | Fast, distributable to non-technical field team; data validation dropdowns for enumerators |
| Structured storage, joins across consumer/dealer/interview data, repeatable aggregation queries | **SQL** | Single source of truth, enforces schema/referential integrity, scalable querying |
| Data cleaning at scale, statistical hypothesis testing, regression, clustering/segmentation | **Python** | Needed for stats (scipy), ML (scikit-learn) beyond what Excel/SQL can do cleanly |
| Executive & operational dashboards, self-serve slicing, stakeholder storytelling | **Power BI** | Visual, interactive, distributable to non-technical stakeholders, refreshable |

---
*Document 5 of 9.*
