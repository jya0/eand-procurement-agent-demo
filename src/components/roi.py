import streamlit as st


def streamlit_roi_ver1():
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


def streamlit_roi_ver2():
    # ROI Calculator
    st.subheader("Calculate Your Potential ROI", divider=True)

    with st.form(key="roi_calculator_ver_2"):
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


def streamlit_roi_ver3():
    # ROI Calculator
    st.subheader("Calculate Your Potential ROI", divider=True)

    with st.form(key="roi_calculator_ver3"):
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

        # Supplier search time
        st.text("Time spent on supplier search and qualification:")
        col3, col4 = st.columns(2)

        with col3:
            search_hours = st.number_input(
                "Hours spent searching for suppliers per procurement",
                min_value=1,
                max_value=40,
                value=8,
                step=1,
            )

        with col4:
            num_procurements = st.number_input(
                "Number of new procurements per month",
                min_value=1,
                max_value=50,
                value=5,
                step=1,
            )

        # Communication time
        st.text("Time spent on supplier communication:")
        col5, col6 = st.columns(2)

        with col5:
            email_hours = st.number_input(
                "Hours spent on email communication per supplier",
                min_value=0.5,
                max_value=20.0,
                value=4.0,
                step=0.5,
            )

        with col6:
            suppliers_per_procurement = st.number_input(
                "Average suppliers contacted per procurement",
                min_value=1,
                max_value=20,
                value=3,
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

        # Different reduction rates for different activities
        search_reduction = time_reduction_map[company_profile]
        communication_reduction = (
            time_reduction_map[company_profile] * 0.9
        )  # Communication might be slightly less improved

        # Form submission button
        submitted = st.form_submit_button("Calculate ROI")

        if submitted:
            # Calculate hourly rate
            hourly_rate = monthly_salary / working_hours

            # Calculate total time spent on procurement activities
            total_search_time = search_hours * num_procurements
            total_communication_time = (
                email_hours * suppliers_per_procurement * num_procurements
            )
            total_procurement_time = total_search_time + total_communication_time

            # Calculate time saved
            search_time_saved = total_search_time * (search_reduction / 100)
            communication_time_saved = total_communication_time * (
                communication_reduction / 100
            )
            total_time_saved = search_time_saved + communication_time_saved

            # Calculate monetary value of time saved
            monthly_savings = total_time_saved * hourly_rate
            annual_savings = monthly_savings * 12

            # Calculate productivity increase
            time_efficiency_ratio = (
                total_time_saved / total_procurement_time
                if total_procurement_time > 0
                else 0
            )
            additional_capacity = num_procurements * time_efficiency_ratio

            # Display results
            st.success("ROI Analysis Complete")

            col_savings, col_productivity = st.columns(2)

            with col_savings:
                st.metric("Annual Cost Savings", f"AED {annual_savings:,.2f}")
                st.text(f"Monthly savings: AED {monthly_savings:,.2f}")

            with col_productivity:
                st.metric("Time Saved", f"{total_time_saved:.1f} hours/month")
                st.text(
                    f"Additional capacity: {additional_capacity:.1f} more procurements/month"
                )

            # Calculation explanation in expander
            with st.expander("View Calculation Methodology"):
                st.subheader("How We Calculate Your ROI")

                st.subheader("Step 1: Calculate Hourly Rate", anchor=False)
                st.code(
                    f"Hourly Rate = Monthly Salary ÷ Working Hours = {monthly_salary} ÷ {working_hours} = AED {hourly_rate:.2f}"
                )

                st.subheader("Step 2: Calculate Current Time Investment", anchor=False)
                st.code(
                    f"Search Time = Hours per Search × Procurements = {search_hours} × {num_procurements} = {total_search_time} hours/month"
                )
                st.code(
                    f"Communication Time = Hours per Supplier × Suppliers × Procurements = {email_hours} × {suppliers_per_procurement} × {num_procurements} = {total_communication_time} hours/month"
                )
                st.code(
                    f"Total Procurement Time = {total_search_time} + {total_communication_time} = {total_procurement_time} hours/month"
                )

                st.subheader("Step 3: Calculate Time Saved with AMPA", anchor=False)
                st.code(
                    f"Search Time Saved = {total_search_time} × {search_reduction}% = {search_time_saved:.2f} hours/month"
                )
                st.code(
                    f"Communication Time Saved = {total_communication_time} × {communication_reduction:.1f}% = {communication_time_saved:.2f} hours/month"
                )
                st.code(
                    f"Total Time Saved = {search_time_saved:.2f} + {communication_time_saved:.2f} = {total_time_saved:.2f} hours/month"
                )

                st.subheader("Step 4: Calculate Financial Savings", anchor=False)
                st.code(
                    f"Monthly Savings = Total Time Saved × Hourly Rate = {total_time_saved:.2f} × {hourly_rate:.2f} = AED {monthly_savings:.2f}"
                )
                st.code(
                    f"Annual Savings = Monthly Savings × 12 = {monthly_savings:.2f} × 12 = AED {annual_savings:.2f}"
                )

                st.subheader("Step 5: Calculate Productivity Increase", anchor=False)
                st.code(
                    f"Time Efficiency Ratio = Total Time Saved ÷ Total Procurement Time = {total_time_saved:.2f} ÷ {total_procurement_time} = {time_efficiency_ratio:.2f}"
                )
                st.code(
                    f"Additional Capacity = Current Procurements × Efficiency Ratio = {num_procurements} × {time_efficiency_ratio:.2f} = {additional_capacity:.2f} additional procurements per month"
                )

                st.subheader("What This Means For Your Business:", anchor=False)
                st.text(
                    f"By implementing AMPA, your procurement employee can save {total_time_saved:.1f} hours per month."
                )
                st.text(
                    f"This translates to AED {annual_savings:.2f} in annual cost savings and the capacity to"
                )
                st.text(
                    f"handle approximately {additional_capacity:.1f} more procurement cycles per month with the same resources."
                )

                if search_reduction > 50:
                    st.text(
                        "💡 Insight: With significant time reduction in supplier search, your employee will have"
                    )
                    st.text(
                        "more time to focus on strategic supplier relationships and negotiation."
                    )

            # ROI information
            st.info(
                "Note: For a complete ROI calculation including payback period, please contact our sales team for AMPA pricing information."
            )
