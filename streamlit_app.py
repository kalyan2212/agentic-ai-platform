import streamlit as st
import pandas as pd
import plotly.express as px
from src.Customer import Customer
from src.IntegrationChannel import IntegrationChannel
from src.ChannelType import ChannelType
from src.MigrationOrchestrator import MigrationOrchestrator
from src.RiskAssessor import RiskAssessor
from src.SimulationEngine import SimulationEngine

# Initialize session state
if 'customers' not in st.session_state:
    st.session_state.customers = []
if 'migration_plans' not in st.session_state:
    st.session_state.migration_plans = []
if 'orchestrator' not in st.session_state:
    st.session_state.orchestrator = MigrationOrchestrator()

# Sidebar navigation
st.sidebar.title('Navigation')
page = st.sidebar.radio('Select a page:', ['Dashboard', 'Customer Management', 'Risk Assessment', 'Migration Planning', 'Migration Execution'])

# Dashboard page
if page == 'Dashboard':
    st.title('Dashboard')
    # Metrics
    total_customers = len(st.session_state.customers)
    total_migration_plans = len(st.session_state.migration_plans)
    completed_migrations = sum(1 for plan in st.session_state.migration_plans if plan['status'] == 'Completed')
    in_progress_migrations = sum(1 for plan in st.session_state.migration_plans if plan['status'] == 'In Progress')
    success_rate = (completed_migrations / total_migration_plans * 100) if total_migration_plans > 0 else 0
    st.metric('Total Customers', total_customers)
    st.metric('Total Migration Plans', total_migration_plans)
    st.metric('Completed Migrations', completed_migrations)
    st.metric('In-Progress Migrations', in_progress_migrations)
    st.metric('Success Rate', f'{success_rate:.2f}%')
    
    # Migration status distribution
    migration_status = pd.DataFrame({'Status': ['Completed', 'In Progress', 'Failed'], 'Count': [completed_migrations, in_progress_migrations, total_migration_plans - completed_migrations - in_progress_migrations]})
    fig = px.bar(migration_status, x='Status', y='Count', title='Migration Status Distribution')
    st.plotly_chart(fig)

# Customer Management page
elif page == 'Customer Management':
    st.title('Customer Management')
    with st.form(key='customer_form'):
        customer_id = st.text_input('Customer ID')
        name = st.text_input('Name')
        industry = st.text_input('Industry')
        business_criticality = st.selectbox('Business Criticality', ['High', 'Medium', 'Low'])
        compliance_requirements = st.text_input('Compliance Requirements')
        integration_channels = []
        if st.button('Add Integration Channel'):
            channel_id = st.text_input('Channel ID')
            channel_type = st.selectbox('Channel Type', [ChannelType.TYPE1, ChannelType.TYPE2])
            channel_name = st.text_input('Channel Name')
            config = st.text_area('Config')
            legacy_endpoint = st.text_input('Legacy Endpoint')
            target_endpoint = st.text_input('Target Endpoint')
            transaction_volume = st.number_input('Transaction Volume', min_value=0)
            integration_channels.append({'channel_id': channel_id, 'channel_type': channel_type, 'name': channel_name, 'config': config, 'legacy_endpoint': legacy_endpoint, 'target_endpoint': target_endpoint, 'transaction_volume': transaction_volume})
        if st.form_submit_button('Create Customer'):
            new_customer = Customer(customer_id, name, industry, business_criticality, compliance_requirements, integration_channels)
            st.session_state.customers.append(new_customer)
            st.success('Customer created successfully!')
    # Display customers
    if st.session_state.customers:
        st.subheader('Existing Customers')
        for cust in st.session_state.customers:
            expander = st.expander(cust.name)
            with expander:
                st.write(cust)

# Risk Assessment page
elif page == 'Risk Assessment':
    st.title('Risk Assessment')
    customer_options = [cust.name for cust in st.session_state.customers]
    selected_customer = st.selectbox('Select a customer:', customer_options)
    if st.button('Assess Risk'):
        risk_score = RiskAssessor.assess(selected_customer)
        st.success(f'Risk Score for {selected_customer}: {risk_score}')
        # Display risk details

# Migration Planning page
elif page == 'Migration Planning':
    st.title('Migration Planning')
    customer_options = [cust.name for cust in st.session_state.customers]
    selected_customer = st.selectbox('Select a customer:', customer_options)
    migration_strategy = st.selectbox('Choose Migration Strategy:', ['Phased', 'Big Bang', 'Parallel'])
    if st.button('Create Migration Plan'):
        migration_plan = st.create_migration_plan(selected_customer, migration_strategy)
        st.session_state.migration_plans.append(migration_plan)
        st.success('Migration Plan created successfully!')
        # Display migration plan details

# Migration Execution page
elif page == 'Migration Execution':
    st.title('Migration Execution')
    migration_plan_options = [plan['name'] for plan in st.session_state.migration_plans]
    selected_plan = st.selectbox('Select a Migration Plan:', migration_plan_options)
    if st.button('Run Simulation'):
        results = SimulationEngine.run_simulation(selected_plan)
        st.write(results)
    if st.button('Execute Migration'):
        execution_status = st.execute_migration(selected_plan)
        st.success(f'Execution Status: {execution_status}')