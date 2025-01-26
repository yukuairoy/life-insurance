import streamlit as st
import numpy as np
import pandas as pd
import numpy_financial as nf
import altair as alt


def main():
    st.title("Permanent Life Insurance Rate of Return Calculator")

    st.subheader("Premium Payments")
    premium_start_age, premium_end_age = st.slider(
        "Age Range for Paying Premium (inclusive)",
        min_value=15,
        max_value=75,
        value=(30, 50),
    )
    annual_premium = st.slider(
        "Annual Premium Amount", min_value=0, max_value=120_000, value=5000, step=1000
    )

    st.subheader("Withdrawals")
    withdrawal_start_age, withdrawal_end_age = st.slider(
        "Age Range for Withdrawals (inclusive)",
        min_value=20,
        max_value=120,
        value=(60, 90),
    )
    annual_withdrawal = st.slider(
        "Annual Withdrawal Amount",
        min_value=0,
        max_value=300000,
        value=30000,
        step=1000,
    )

    st.subheader("Death Benefit")
    death_age = st.slider("Age at Death", min_value=20, max_value=120, value=86)
    net_death_benefit = st.number_input(
        "Net Death Benefit",
        min_value=1000,
        max_value=4_000_000,
        value=1_000_000,
        step=1000,
    )

    if st.button("Calculate IRR"):
        # Force the chart to start at the first premium age
        start_age = premium_start_age
        scenario_end_age = max(death_age, premium_end_age, withdrawal_end_age)

        ages = range(start_age, scenario_end_age + 1)
        net_flows = np.zeros(len(ages), dtype=float)

        # Premium outflows (negative)
        for age in range(premium_start_age, min(premium_end_age, death_age) + 1):
            net_flows[age - start_age] -= annual_premium

        # Withdrawal inflows (positive)
        for age in range(withdrawal_start_age, min(withdrawal_end_age, death_age) + 1):
            # Make sure we're within the plotting range
            if age >= start_age:
                net_flows[age - start_age] += annual_withdrawal

        # Death benefit
        if death_age >= start_age:
            net_flows[death_age - start_age] += net_death_benefit

        # Compute IRR
        irr = nf.irr(net_flows)

        st.write("### Results")
        if irr is not None and not np.isnan(irr):
            st.write(f"**Estimated IRR**: {irr * 100:,.2f}%")
        else:
            st.write("Could not compute IRR with the given inputs.")

        # Prepare DataFrame for plotting
        df = pd.DataFrame({"Age": ages, "Net Flow": net_flows})

        # Bar chart on a linear scale
        chart = (
            alt.Chart(df)
            .mark_bar()
            .encode(
                x=alt.X("Age:O", title="Age"),
                y=alt.Y("Net Flow:Q", title="Net Cash Flow"),
                color=alt.condition(
                    alt.datum["Net Flow"] >= 0,
                    alt.value("steelblue"),  # color for >= 0
                    alt.value("red"),  # color for < 0
                ),
                tooltip=["Age", "Net Flow"],
            )
            .properties(width=700, height=400, title="Yearly Net Cash Flow")
            .interactive()
        )

        st.altair_chart(chart, use_container_width=True)


if __name__ == "__main__":
    main()
