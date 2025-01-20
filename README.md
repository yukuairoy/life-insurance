# Permanent Life Insurance IRR Calculator

A Streamlit app to calculate the internal rate of return (IRR) for a permanent life insurance policy. Users select:

- **Premium-Paying Ages** (inclusive range)
- **Annual Premium**
- **Withdrawal Ages** (inclusive range)
- **Annual Withdrawal**
- **Hypothetical Death Age**
- **Net Death Benefit**

The app computes:

- **Yearly Net Cash Flows** (negative for premiums, positive for withdrawals, plus a final death benefit).
- **IRR** using `numpy_financial.irr`.
- **Bar Chart** visualization showing each year’s net flow.

Install dependencies:

```bash
pip install streamlit numpy-financial altair
```