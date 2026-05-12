# Tableau Dashboard Creation Guide

This guide outlines the steps to build a professional Network Anomaly Detection dashboard based on your dataset.

## Phase 1: Data Preparation in Tableau

1.  **Load Data**: Open Tableau and connect to `Network_anomaly_data.csv`.
2.  **Create Row ID**: Since there is no timestamp, we need a proxy for time.
    *   Go to **Analysis** > **Create Calculated Field**.
    *   Name it `Record Sequence`.
    *   Formula: `INDEX()`
3.  **Group Attack Types**: The dataset has many specific attack names. Grouping them makes the dashboard more readable.
    *   Right-click the `attack` field > **Create** > **Group**.
    *   **DoS**: back, land, neptune, pod, smurf, teardrop.
    *   **Probe**: ipsweep, nmap, portsweep, satan.
    *   **R2L**: ftp_write, guess_passwd, imap, multihop, phf, spy, warezclient, warezmaster.
    *   **U2R**: buffer_overflow, loadmodule, perl, rootkit.
    *   **Normal**: normal.

---

## Phase 2: Building Visualizations (Worksheets)

### 1. KPI Scorecards (Top of Dashboard)
*   **Total Connections**: Drag `Number of Records` to Text.
*   **Total Anomalies**: Create a calculated field `Is Anomaly` (`IF [Grouped Attack] != 'normal' THEN 1 ELSE 0 END`). Drag to Text.
*   **Anomaly %**: Create `[Total Anomalies] / [Total Connections]`.

### 2. Traffic Volume Over Time (Line Chart)
*   **Columns**: `Record Sequence` (set to Continuous).
*   **Rows**: `Src_bytes` and `Dst_bytes` (use Dual Axis).
*   **Color**: Use different colors for Inbound and Outbound.
*   **Insight**: Look for spikes in traffic that correlate with attack flags.

### 3. Attack Type Breakdown (Tree Map or Pie Chart)
*   **Marks**: Drag `Grouped Attack` to Color and `Number of Records` to Size.
*   **Insight**: Quickly see which attack category is most prevalent.

### 4. Protocol & Service Risk (Heatmap)
*   **Columns**: `Protocol_type`.
*   **Rows**: `Service` (Filter for Top 15).
*   **Color**: `Total Anomalies`.
*   **Insight**: Identify which combinations (e.g., TCP + Private) are most frequently attacked.

### 5. Byte Transfer Analysis (Scatter Plot)
*   **Columns**: `Src_bytes`.
*   **Rows**: `Dst_bytes`.
*   **Detail**: `Record Sequence`.
*   **Color**: `Grouped Attack`.
*   **Scale**: Set both axes to **Logarithmic** (important due to extreme values).

---

## Phase 3: Dashboard Assembly

1.  **Layout**: Use a **Vertical Container**.
2.  **Header**: Add a Title "Network Security Monitoring Dashboard".
3.  **KPIs Row**: Place the three scorecard sheets side-by-side at the top.
4.  **Main View**: Place the "Traffic Volume Over Time" chart in the center.
5.  **Bottom Row**: Place the "Attack Breakdown" and "Service Risk Heatmap" side-by-side.
6.  **Interactivity**: 
    *   Go to **Dashboard** > **Actions** > **Add Action** > **Filter**.
    *   Set the "Attack Breakdown" chart as a source to filter the rest of the dashboard.

---

## Phase 4: Publishing

1.  Go to **Server** > **Tableau Public** > **Save to Tableau Public As...**.
2.  Copy the resulting URL and paste it into your **[`Submission_Links.md`](file:///C:/Users/sanke/Documents/Scaler/PortfolioProject01_AnomalyDetection/Submission_Links.md)** file.
