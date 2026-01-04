"""
Streamlit Dashboard for E-Commerce Customer Analytics
Interactive web application for exploring customer segmentation and predictions
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pickle
import os

# Page config
st.set_page_config(
    page_title="E-Commerce Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Load and preprocess the dataset"""
    if not os.path.exists('Online_Retail.xlsx'):
        st.error("Dataset not found! Please ensure Online_Retail.xlsx is in the project directory.")
        return None
    
    df = pd.read_excel('Online_Retail.xlsx')
    
    # Clean data
    df_clean = df.copy()
    df_clean = df_clean.dropna(subset=['CustomerID'])
    df_clean = df_clean[df_clean['Quantity'] > 0]
    df_clean = df_clean[df_clean['UnitPrice'] > 0]
    df_clean['TotalAmount'] = df_clean['Quantity'] * df_clean['UnitPrice']
    df_clean['InvoiceDate'] = pd.to_datetime(df_clean['InvoiceDate'])
    df_clean['Year'] = df_clean['InvoiceDate'].dt.year
    df_clean['Month'] = df_clean['InvoiceDate'].dt.month
    df_clean['Weekday'] = df_clean['InvoiceDate'].dt.day_name()
    df_clean['Hour'] = df_clean['InvoiceDate'].dt.hour
    
    return df_clean

@st.cache_data
def calculate_rfm(df_clean):
    """Calculate RFM metrics"""
    snapshot_date = df_clean['InvoiceDate'].max() + timedelta(days=1)
    
    rfm = df_clean.groupby('CustomerID').agg({
        'InvoiceDate': lambda x: (snapshot_date - x.max()).days,
        'InvoiceNo': 'nunique',
        'TotalAmount': 'sum'
    })
    rfm.columns = ['Recency', 'Frequency', 'Monetary']
    
    # Score
    rfm['R'] = pd.qcut(rfm['Recency'], 5, labels=[5, 4, 3, 2, 1], duplicates='drop')
    rfm['F'] = pd.qcut(rfm['Frequency'].rank(method='first'), 5, labels=[1, 2, 3, 4, 5], duplicates='drop')
    rfm['M'] = pd.qcut(rfm['Monetary'], 5, labels=[1, 2, 3, 4, 5], duplicates='drop')
    
    rfm['RFM_Score'] = rfm['R'].astype(int) + rfm['F'].astype(int) + rfm['M'].astype(int)
    
    def get_segment(score):
        if score >= 13:
            return 'Champions'
        elif score >= 11:
            return 'Loyal'
        elif score >= 9:
            return 'Potential Loyal'
        elif score >= 7:
            return 'New/Promising'
        elif score >= 5:
            return 'At Risk'
        else:
            return 'Lost'
    
    rfm['Segment'] = rfm['RFM_Score'].apply(get_segment)
    
    return rfm

def main():
    st.markdown('<h1 class="main-header">📊 E-Commerce Customer Analytics Dashboard</h1>', unsafe_allow_html=True)
    
    # Load data
    df_clean = load_data()
    if df_clean is None:
        return
    
    # Sidebar
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox("Choose a page", [
        "📈 Overview",
        "👥 Customer Segmentation",
        "📊 Sales Analysis",
        "🔄 Retention Analysis",
        "🤖 ML Predictions",
        "🌍 Geographic Insights"
    ])
    
    # Overview Page
    if page == "📈 Overview":
        st.header("Business Overview")
        
        col1, col2, col3, col4 = st.columns(4)
        
        total_rev = df_clean['TotalAmount'].sum()
        num_customers = df_clean['CustomerID'].nunique()
        num_orders = df_clean['InvoiceNo'].nunique()
        avg_order = total_rev / num_orders
        
        with col1:
            st.metric("Total Revenue", f"£{total_rev:,.0f}")
        with col2:
            st.metric("Total Customers", f"{num_customers:,}")
        with col3:
            st.metric("Total Orders", f"{num_orders:,}")
        with col4:
            st.metric("Avg Order Value", f"£{avg_order:.2f}")
        
        # Revenue trend
        st.subheader("Revenue Trend Over Time")
        monthly = df_clean.groupby(df_clean['InvoiceDate'].dt.to_period('M'))['TotalAmount'].sum()
        monthly_df = pd.DataFrame({
            'Month': monthly.index.astype(str),
            'Revenue': monthly.values
        })
        
        fig = px.line(monthly_df, x='Month', y='Revenue', 
                      title='Monthly Revenue Trend',
                      markers=True)
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
        
        # Top products
        st.subheader("Top 10 Products by Revenue")
        products = df_clean.groupby('Description')['TotalAmount'].sum().nlargest(10)
        fig = px.bar(x=products.values, y=products.index, 
                     orientation='h', title='Top Products')
        fig.update_layout(height=400, yaxis={'categoryorder': 'total ascending'})
        st.plotly_chart(fig, use_container_width=True)
    
    # Customer Segmentation
    elif page == "👥 Customer Segmentation":
        st.header("RFM Customer Segmentation")
        
        rfm = calculate_rfm(df_clean)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Segment Distribution")
            seg_counts = rfm['Segment'].value_counts()
            fig = px.pie(values=seg_counts.values, names=seg_counts.index,
                        title='Customer Segments')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("Revenue by Segment")
            seg_rev = rfm.groupby('Segment')['Monetary'].sum().sort_values()
            fig = px.bar(x=seg_rev.values, y=seg_rev.index,
                        orientation='h', title='Revenue Distribution')
            fig.update_layout(yaxis={'categoryorder': 'total ascending'})
            st.plotly_chart(fig, use_container_width=True)
        
        # Segment details
        st.subheader("Segment Details")
        seg_summary = rfm.groupby('Segment').agg({
            'Recency': 'mean',
            'Frequency': 'mean',
            'Monetary': ['mean', 'sum']
        }).round(2)
        seg_summary.columns = ['Avg_Recency', 'Avg_Frequency', 'Avg_Monetary', 'Total_Revenue']
        seg_summary['Count'] = rfm.groupby('Segment').size()
        seg_summary['Rev_Pct'] = (seg_summary['Total_Revenue'] / seg_summary['Total_Revenue'].sum() * 100).round(1)
        
        st.dataframe(seg_summary.sort_values('Count', ascending=False))
        
        # Customer lookup
        st.subheader("Customer Lookup")
        customer_id = st.selectbox("Select Customer ID", sorted(rfm.index))
        if customer_id:
            customer_data = rfm.loc[customer_id]
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Segment", customer_data['Segment'])
            with col2:
                st.metric("Recency", f"{customer_data['Recency']:.0f} days")
            with col3:
                st.metric("Frequency", f"{customer_data['Frequency']:.0f}")
            with col4:
                st.metric("Monetary", f"£{customer_data['Monetary']:,.2f}")
    
    # Sales Analysis
    elif page == "📊 Sales Analysis":
        st.header("Sales Performance Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Sales by Day of Week")
            weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            daily = df_clean.groupby('Weekday')['TotalAmount'].sum().reindex(weekday_order)
            fig = px.bar(x=daily.index, y=daily.values, title='Revenue by Day')
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("Sales by Hour")
            hourly = df_clean.groupby('Hour')['TotalAmount'].sum()
            fig = px.line(x=hourly.index, y=hourly.values, 
                         title='Revenue by Hour', markers=True)
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        # Country analysis
        st.subheader("Top Countries by Revenue")
        top_countries = df_clean.groupby('Country')['TotalAmount'].sum().nlargest(15)
        fig = px.bar(x=top_countries.values, y=top_countries.index,
                    orientation='h', title='Revenue by Country')
        fig.update_layout(height=500, yaxis={'categoryorder': 'total ascending'})
        st.plotly_chart(fig, use_container_width=True)
    
    # Retention Analysis
    elif page == "🔄 Retention Analysis":
        st.header("Cohort Retention Analysis")
        
        df_clean['OrderMonth'] = df_clean['InvoiceDate'].dt.to_period('M').astype(str)
        first_purchase = df_clean.groupby('CustomerID')['InvoiceDate'].min().dt.to_period('M').astype(str)
        df_clean['Cohort'] = df_clean['CustomerID'].map(first_purchase)
        
        cohort_data = df_clean.groupby(['Cohort', 'OrderMonth'])['CustomerID'].nunique().reset_index()
        cohort_sizes = df_clean.groupby('Cohort')['CustomerID'].nunique()
        
        cohort_data['Period'] = (pd.to_datetime(cohort_data['OrderMonth']) - 
                                pd.to_datetime(cohort_data['Cohort'])).dt.days // 30
        
        cohort_data = cohort_data.drop_duplicates(['Cohort', 'Period'])
        cohort_pivot = cohort_data.pivot(index='Cohort', columns='Period', values='CustomerID')
        
        for col in cohort_pivot.columns:
            cohort_pivot[col] = cohort_pivot[col] / cohort_sizes
        
        cohort_pivot = cohort_pivot.fillna(0)
        
        # Heatmap
        fig = px.imshow(cohort_pivot.values, 
                       labels=dict(x="Months Since First Purchase", y="Cohort", color="Retention Rate"),
                       x=[f"Month {i}" for i in cohort_pivot.columns],
                       y=cohort_pivot.index,
                       color_continuous_scale='YlOrRd',
                       aspect="auto")
        fig.update_layout(height=600, title="Customer Retention Heatmap")
        st.plotly_chart(fig, use_container_width=True)
        
        # Average retention
        avg_ret = cohort_pivot.mean()
        st.subheader("Average Retention Rates")
        ret_df = pd.DataFrame({
            'Month': [f"Month {i}" for i in avg_ret.index],
            'Retention Rate': avg_ret.values
        })
        fig = px.line(ret_df, x='Month', y='Retention Rate', 
                     title='Average Retention Over Time', markers=True)
        st.plotly_chart(fig, use_container_width=True)
    
    # ML Predictions
    elif page == "🤖 ML Predictions":
        st.header("Machine Learning Predictions")
        
        st.info("💡 This section uses trained ML models to predict customer churn and lifetime value")
        
        # Load models if they exist
        if (os.path.exists('models/churn_model.pkl') and 
            os.path.exists('models/clv_model.pkl') and
            os.path.exists('models/churn_scaler.pkl') and
            os.path.exists('models/clv_scaler.pkl')):
            with open('models/churn_model.pkl', 'rb') as f:
                churn_model = pickle.load(f)
            with open('models/clv_model.pkl', 'rb') as f:
                clv_model = pickle.load(f)
            with open('models/churn_scaler.pkl', 'rb') as f:
                churn_scaler = pickle.load(f)
            with open('models/clv_scaler.pkl', 'rb') as f:
                clv_scaler = pickle.load(f)
            
            rfm = calculate_rfm(df_clean)
            
            st.subheader("Predict Churn for Customer")
            customer_id = st.selectbox("Select Customer", sorted(rfm.index), key='churn_customer')
            
            if customer_id:
                customer_features = rfm.loc[customer_id][['Recency', 'Frequency', 'Monetary']].values.reshape(1, -1)
                
                # Scale features
                customer_features_churn = churn_scaler.transform(customer_features)
                customer_features_clv = clv_scaler.transform(customer_features)
                
                churn_prob = churn_model.predict_proba(customer_features_churn)[0][1]
                clv_pred = clv_model.predict(customer_features_clv)[0]
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Churn Probability", f"{churn_prob*100:.1f}%")
                    if churn_prob > 0.5:
                        st.warning("⚠️ High churn risk - recommend retention campaign")
                    else:
                        st.success("✅ Low churn risk")
                
                with col2:
                    st.metric("Predicted CLV", f"£{clv_pred:,.2f}")
                    actual_clv = rfm.loc[customer_id, 'Monetary']
                    st.caption(f"Actual CLV: £{actual_clv:,.2f}")
            
            # Batch prediction
            st.subheader("Segment-Level Predictions")
            if st.button("Generate Predictions for All Segments"):
                segment_predictions = []
                for segment in rfm['Segment'].unique():
                    seg_customers = rfm[rfm['Segment'] == segment]
                    features = seg_customers[['Recency', 'Frequency', 'Monetary']].values
                    
                    # Scale features
                    features_churn = churn_scaler.transform(features)
                    features_clv = clv_scaler.transform(features)
                    
                    churn_probs = churn_model.predict_proba(features_churn)[:, 1]
                    clv_preds = clv_model.predict(features_clv)
                    
                    segment_predictions.append({
                        'Segment': segment,
                        'Avg_Churn_Prob': churn_probs.mean(),
                        'High_Risk_Customers': (churn_probs > 0.5).sum(),
                        'Avg_Predicted_CLV': clv_preds.mean(),
                        'Total_Customers': len(seg_customers)
                    })
                
                pred_df = pd.DataFrame(segment_predictions)
                st.dataframe(pred_df)
                
                # Visualization
                fig = px.bar(pred_df, x='Segment', y='Avg_Churn_Prob',
                           title='Average Churn Probability by Segment')
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("⚠️ ML models not found. Please run the training script first.")
            st.code("python train_models.py")
    
    # Geographic Insights
    elif page == "🌍 Geographic Insights":
        st.header("Geographic Performance Analysis")
        
        geo = df_clean.groupby('Country').agg({
            'TotalAmount': 'sum',
            'CustomerID': 'nunique',
            'InvoiceNo': 'nunique'
        })
        geo.columns = ['Revenue', 'Customers', 'Orders']
        geo['Rev_per_Customer'] = geo['Revenue'] / geo['Customers']
        geo = geo.sort_values('Revenue', ascending=False)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Revenue by Country")
            top_geo = geo.head(15)
            fig = px.bar(x=top_geo['Revenue'], y=top_geo.index,
                        orientation='h', title='Top 15 Countries')
            fig.update_layout(yaxis={'categoryorder': 'total ascending'}, height=500)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("Revenue per Customer")
            fig = px.bar(x=top_geo['Rev_per_Customer'], y=top_geo.index,
                        orientation='h', title='Revenue per Customer')
            fig.update_layout(yaxis={'categoryorder': 'total ascending'}, height=500)
            st.plotly_chart(fig, use_container_width=True)
        
        # Map visualization
        st.subheader("Geographic Distribution")
        st.dataframe(geo.head(20))

if __name__ == "__main__":
    main()

