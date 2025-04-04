import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# --- DP Function for Workforce Allocation ---
def workforce_allocation(n, m, profit):
    dp = np.zeros((n + 1, m + 1), dtype=int)

    for i in range(1, n + 1):  # Iterate through projects
        for j in range(m + 1):  # Iterate through available workforce
            dp[i][j] = dp[i-1][j]  # Case: Exclude the project
            for k in range(j + 1):  # Allocate k workers
                dp[i][j] = max(dp[i][j], profit[i-1][k] + dp[i-1][j-k])

    return dp[n][m], dp

# --- Streamlit UI ---
st.title("📊 Project Scheduling & Workforce Allocation")
st.markdown("Optimize workforce allocation across multiple projects for maximum efficiency.")

# --- Input Section ---
st.sidebar.header("🔢 Input Parameters")
n = st.sidebar.number_input("Number of Projects", min_value=1, max_value=10, value=3, step=1)
m = st.sidebar.number_input("Total Available Workforce", min_value=1, max_value=20, value=5, step=1)

st.sidebar.subheader("📈 Profitability Table")
profit = []
for i in range(n):
    profit.append(
        list(map(int, st.sidebar.text_input(f"Profit for Project {i+1} (comma-separated)", 
                                            "0,3,5,8,9,10").split(",")))
    )

profit = np.array(profit)

# --- Compute DP Solution ---
if st.sidebar.button("🚀 Allocate Workforce"):
    max_profit, dp_table = workforce_allocation(n, m, profit)

    # --- Display Results ---
    st.subheader("📌 Optimized Workforce Allocation")
    st.write(f"**Maximum Profit Achievable:** ₹{max_profit}")

    # --- Display DP Table ---
    df = pd.DataFrame(dp_table, columns=[f"{i} Workers" for i in range(m+1)], index=[f"Project {i}" for i in range(n+1)])
    st.dataframe(df)

    # --- Bar Chart Visualization ---
    fig, ax = plt.subplots()
    ax.bar(range(n), dp_table[:, -1][1:], color="blue", alpha=0.7)
    ax.set_xlabel("Projects")
    ax.set_ylabel("Allocated Workforce Profit")
    ax.set_title("Workforce Allocation Profit Per Project")
    ax.set_xticks(range(n))
    ax.set_xticklabels([f"Project {i+1}" for i in range(n)])
    st.pyplot(fig)
