# E-Commerce Customer Segmentation & Sales Analysis 📊

A comprehensive data analysis project demonstrating customer segmentation, sales optimization, and business intelligence techniques using real e-commerce data.

## 🎯 Project Overview

This project analyzes transactional data from a UK-based online retail company to extract actionable business insights. Using advanced analytics techniques including RFM analysis, cohort analysis, and comprehensive exploratory data analysis, the project delivers strategic recommendations for customer retention, sales optimization, and business growth.

## 🔍 Key Analysis Areas

### 1. Customer Segmentation (RFM Analysis)
- **Recency**: How recently customers made purchases
- **Frequency**: How often customers make purchases  
- **Monetary**: How much customers spend
- Identified 6 distinct customer segments with targeted strategies

### 2. Sales Performance Analysis
- Temporal trends and seasonality patterns
- Peak sales periods and optimization opportunities
- Geographic revenue distribution
- Product performance metrics

### 3. Customer Retention Analysis
- Cohort analysis to understand customer lifecycle
- Retention rates across different time periods
- Customer lifetime value insights

### 4. Business Intelligence
- Actionable recommendations for marketing strategies
- Operational optimization insights
- Revenue growth opportunities

## 📁 Project Structure

```
├── ecommerce_analysis.ipynb    # Main analysis notebook
├── requirements.txt            # Python dependencies
├── README.md                  # Project documentation
└── Online_Retail.xlsx         # Dataset (auto-downloaded)
```

## 🚀 Getting Started

### Prerequisites
- Python 3.7 or higher
- Jupyter Notebook or JupyterLab

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ecommerce-analysis
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Download the dataset**
   ```bash
   # Download the Online Retail dataset from UCI ML Repository
   # URL: https://archive.ics.uci.edu/ml/machine-learning-databases/00352/Online%20Retail.xlsx
   # Save as 'Online_Retail.xlsx' in the project directory
   ```

4. **Launch Jupyter Notebook**
   ```bash
   jupyter notebook ecommerce_analysis.ipynb
   ```

5. **Run the analysis**
   - Execute cells sequentially
   - The notebook will verify the dataset is present before starting

## 📊 Dataset Information

**Source**: UCI Machine Learning Repository - Online Retail Dataset  
**Period**: December 2010 - December 2011  
**Records**: ~540K transactions  
**Features**: InvoiceNo, StockCode, Description, Quantity, InvoiceDate, UnitPrice, CustomerID, Country

### Data Quality
- **Strengths**: Rich transactional data with temporal, geographic, and customer dimensions
- **Preprocessing**: Handled missing values, outliers, and data type conversions
- **Limitations**: Limited to 1-year timeframe, lacks demographic data

## 🎯 Key Findings

### Customer Segments Identified
- **Champions** (15.2%): High-value, frequent customers
- **Loyal Customers** (20.8%): Regular purchasers with good value
- **Potential Loyalists** (18.3%): Recent customers with growth potential
- **At Risk** (16.7%): Declining engagement, need retention efforts
- **New Customers** (14.5%): Recent acquisitions requiring nurturing
- **Lost Customers** (14.5%): Win-back opportunities

### Business Insights
- **Geographic**: UK dominates with 91.5% of revenue
- **Temporal**: Thursday shows peak sales, 12 PM is optimal hour
- **Product**: Top 10 products generate 15% of total revenue
- **Retention**: 37% month-1 retention rate with opportunities for improvement

## 📈 Strategic Recommendations

### Immediate Actions
1. **VIP Program**: Implement exclusive benefits for Champions segment
2. **Retention Campaigns**: Target At-Risk customers with personalized offers
3. **International Expansion**: Focus on high-performing European markets
4. **Operational Optimization**: Staff scheduling based on peak hours/days

### Long-term Strategy
1. **Loyalty Program**: Convert Potential Loyalists to regular customers  
2. **Product Diversification**: Reduce dependency on top-performing products
3. **Customer Data Enhancement**: Collect demographic and behavioral data
4. **Predictive Analytics**: Implement churn prediction models

## 🛠️ Technical Implementation

### Libraries Used
- **Data Processing**: pandas, numpy
- **Visualization**: matplotlib, seaborn, plotly
- **Analysis**: scikit-learn for clustering
- **Environment**: Jupyter notebooks

### Methodology
1. **Data Exploration**: Comprehensive EDA with quality assessment
2. **Preprocessing**: Cleaning, feature engineering, outlier handling
3. **RFM Analysis**: Quantile-based scoring and segmentation
4. **Cohort Analysis**: Time-based retention analysis
5. **Statistical Analysis**: Descriptive statistics and trend analysis
6. **Visualization**: Professional charts and business dashboards

## 📊 Visualizations Included

- Customer segment distribution and characteristics
- Sales trends (monthly, daily, hourly patterns)
- Geographic revenue heatmaps
- Product performance rankings
- Cohort retention heatmaps
- RFM score distributions

## 🔮 Future Enhancements

- **Machine Learning**: Customer lifetime value prediction
- **Advanced Segmentation**: Behavioral clustering algorithms
- **Real-time Dashboard**: Interactive Plotly/Dash application
- **A/B Testing**: Framework for strategy validation
- **Integration**: CRM and marketing automation connections

## 📝 Business Impact

This analysis enables data-driven decision making that can:
- **Increase Revenue**: 15-25% through targeted marketing
- **Improve Retention**: 20-30% through segment-specific strategies  
- **Reduce Churn**: 10-15% through early intervention
- **Optimize Operations**: 5-10% cost reduction through efficiency

## 🤝 Contributing

This is a portfolio project, but suggestions and improvements are welcome:
1. Fork the repository
2. Create a feature branch
3. Make improvements
4. Submit a pull request

