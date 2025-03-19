import streamlit as st


def streamlit_roi_ver_1():
    # ROI Calculator
    st.subheader("Calculate Your Potential ROI", divider=True)

    with st.container():
        calc_col1, calc_col2, calc_col3 = st.columns(3)

        with calc_col1:
            current_hours = st.slider(
                "Current hours spent on procurement per week", 1, 48, 20
            )

        with calc_col2:
            hourly_rate = st.slider(
                "Average hourly rate of procurement staff (AED)", 20, 100, 40
            )

        with calc_col3:
            ampa_reduction = st.slider(
                "Expected time reduction with AMPA (%)", 30, 90, 60
            )

        savings = current_hours * hourly_rate * (ampa_reduction / 100) * 52

        st.metric("Estimated Annual Savings", f"AED{savings:,.2f}")


def streamlit_roi():
    # ROI Calculator
    st.subheader("Calculate Your Potential ROI", divider=True)

    with st.form(key="roi_calculator"):
        # Employee details
        st.subheader("Employee Information")
        col1, col2 = st.columns(2)

        with col1:
            monthly_salary = st.number_input(
                "Monthly salary of procurement employee (AED)",
                min_value=3000,
                max_value=30000,
                value=10000,
                step=1000,
            )

        with col2:
            working_hours = st.number_input(
                "Working hours per month",
                min_value=120,
                max_value=240,
                value=176,  # Based on standard 22 working days at 8 hours
                step=8,
            )

        # Procurement workload
        st.subheader("Current Procurement Process")
        col3, col4 = st.columns(2)

        with col3:
            procurement_percentage = st.slider(
                "Percentage of time spent on procurement tasks",
                min_value=10,
                max_value=100,
                value=70,
                step=5,
            )

        with col4:
            num_procurements = st.number_input(
                "Average number of procurement cycles per month",
                min_value=1,
                max_value=100,
                value=15,
                step=1,
            )

        # Company digitization level
        st.subheader("Company Profile")
        company_profile = st.selectbox(
            "Select your company's current procurement digitization level",
            options=[
                "Paper-based process (70-80% time reduction with AMPA)",
                "Basic digital tools (50-60% time reduction with AMPA)",
                "Partial automation (30-40% time reduction with AMPA)",
                "Advanced systems (20-30% time reduction with AMPA)",
            ],
            index=1,
        )

        # Map selection to time reduction percentage
        time_reduction_map = {
            "Paper-based process (70-80% time reduction with AMPA)": 75,
            "Basic digital tools (50-60% time reduction with AMPA)": 55,
            "Partial automation (30-40% time reduction with AMPA)": 35,
            "Advanced systems (20-30% time reduction with AMPA)": 25,
        }

        time_reduction = time_reduction_map[company_profile]

        # Form submission button
        submitted = st.form_submit_button("Calculate ROI")

        if submitted:
            # Calculate hourly rate
            hourly_rate = monthly_salary / working_hours

            # Calculate hours spent on procurement
            procurement_hours = working_hours * (procurement_percentage / 100)

            # Calculate time saved
            hours_saved_monthly = procurement_hours * (time_reduction / 100)

            # Calculate monetary value of time saved
            monthly_savings = hours_saved_monthly * hourly_rate
            annual_savings = monthly_savings * 12

            # Calculate productivity increase
            additional_procurements = num_procurements * (time_reduction / 100)

            # Display results
            st.success("ROI Analysis Complete")

            col_savings, col_productivity = st.columns(2)

            with col_savings:
                st.metric("Annual Cost Savings", f"AED {annual_savings:,.2f}")
                st.text(f"Monthly savings: AED {monthly_savings:,.2f}")

            with col_productivity:
                st.metric(
                    "Additional Procurement Capacity",
                    f"{additional_procurements:.1f} cycles/month",
                )
                st.text(f"Hours saved per month: {hours_saved_monthly:.1f}")
                st.text(f"Hours saved annually: {hours_saved_monthly * 12:.1f}")

            # Calculation explanation in expander
            with st.expander("View Calculation Methodology"):
                st.subheader("How We Calculate Your ROI")

                st.subheader("Step 1: Calculate Hourly Rate", anchor=False)
                st.code(
                    f"Hourly Rate = Monthly Salary ÷ Working Hours = {monthly_salary} ÷ {working_hours} = AED {hourly_rate:.2f}"
                )

                st.subheader(
                    "Step 2: Calculate Time Spent on Procurement", anchor=False
                )
                st.code(
                    f"Procurement Hours = Working Hours × Procurement Percentage = {working_hours} × {procurement_percentage}% = {procurement_hours:.2f} hours"
                )

                st.subheader("Step 3: Calculate Time Saved with AMPA", anchor=False)
                st.code(
                    f"Hours Saved = Procurement Hours × Time Reduction = {procurement_hours:.2f} × {time_reduction}% = {hours_saved_monthly:.2f} hours per month"
                )

                st.subheader("Step 4: Calculate Financial Savings", anchor=False)
                st.code(
                    f"Monthly Savings = Hours Saved × Hourly Rate = {hours_saved_monthly:.2f} × {hourly_rate:.2f} = AED {monthly_savings:.2f}"
                )
                st.code(
                    f"Annual Savings = Monthly Savings × 12 = {monthly_savings:.2f} × 12 = AED {annual_savings:.2f}"
                )

                st.subheader("Step 5: Calculate Productivity Increase", anchor=False)
                st.code(
                    f"Additional Procurement Capacity = Current Cycles × Time Reduction = {num_procurements} × {time_reduction}% = {additional_procurements:.2f} additional cycles per month"
                )

                st.subheader("What This Means For Your Business:", anchor=False)
                st.text(
                    f"By implementing AMPA, your procurement employee can save {hours_saved_monthly:.1f} hours per month."
                )
                st.text(
                    f"This translates to AED {annual_savings:.2f} in annual cost savings and the capacity to"
                )
                st.text(
                    f"handle {additional_procurements:.1f} more procurement cycles per month with the same resources."
                )

                if time_reduction > 50:
                    st.text(
                        "💡 Insight: With over 50% time reduction, you may want to consider reallocating"
                    )
                    st.text(
                        "some of the saved time to strategic procurement initiatives or other value-adding activities."
                    )

            # ROI information
            st.info(
                "Note: For a complete ROI calculation including payback period, please contact our sales team for AMPA pricing information."
            )
