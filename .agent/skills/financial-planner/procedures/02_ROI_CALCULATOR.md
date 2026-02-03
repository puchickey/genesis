# Procedure 02: ROI Calculator

**Objective:**
Validate a purchase decision by calculating its "Payback Period" based on the user's hourly value.

## 🧮 Logic Flow

### 1. Variables
*   **Price (P):** Cost of the item (e.g., 200,000 JPY for Washer).
*   **Time Saved (T):** Hours saved per month (e.g., 10 hours for hanging laundry).
*   **Hourly Rate (R):** User's estimated hourly value (Default: 3,000 JPY/hr).

### 2. Calculation
> `Payback Months = P / (T * R)`

### 3. Verdict
*   **If Payback < 12 months:** "Instant Buy. It pays for itself in a year."
*   **If Payback < 24 months:** "Recommended. Good investment."
*   **If Payback > 36 months:** "Luxury. Buy only if you really love it."

### 4. Output
Present the calculation result clearly.
*   "This drum washer costs 200k, but saves 15hrs/month. It effectively pays for itself in **4.4 months**. Buying it is cheaper than NOT buying it."
