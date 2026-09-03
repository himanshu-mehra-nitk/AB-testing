import pandas as pd
import numpy as np
import seaborn as sns
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler
import xgboost as xgb
from datetime import timedelta
import matplotlib.pyplot as plt
from scipy import stats
from scipy.stats import shapiro, ttest_ind, mannwhitneyu, f_oneway, kruskal
from warnings import simplefilter
simplefilter("ignore")


def run_analysis(section: str, priceSegment: str):
    # array for returning the response in the frontend 
    recommendations = []

    print("Section:", section)
    print("Price Segment:", priceSegment)

    # Dynamic dataset selection - this will come from frontend
    if section == "laptops" and priceSegment == "60000-90000":
        selected_category = "laptops_60k-90k"
    elif section == "mobiles" and priceSegment == "20000-30000":
        selected_category = "mobiles_20k-30k"
    elif section == "mobiles" and priceSegment == "60000-70000":
        selected_category = "mobiles_60k-70k"
    elif section == "laptops" and priceSegment == "110000-130000":
        selected_category = "laptops_110k-130k"
    elif section == "headphones" and priceSegment == "2000-5000":
        selected_category = "headphones_2k-5k"
    

    # Load the dataset based on selected category
    dataset_filename = f"{selected_category}.csv"
    df = pd.read_csv(dataset_filename)

    print("Dataset Info:")
    print(f"The dataset has {df.shape[0]} rows and {df.shape[1]} columns.")
    print(f"Columns: {df.columns.tolist()}")
    print("\nFirst few rows:")
    print(df.head())

    print(f"\nCampaign distribution:")
    print(df['Campaign_Name'].value_counts())

    print(f"\nThere are {df.isna().sum().sum()} null values.")
    print(f"There are {df.duplicated().sum()} duplicate values.")

    # Data Cleaning
    print("\n=== DATA CLEANING ===")
    # Extract only date part (ignore time) and convert to datetime
    df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d')

    # Check data types and convert if necessary
    print("\nData types before conversion:")
    print(df.dtypes)

    # No conversion needed as the data appears to be already in correct format
    print("\nData types after verification:")
    print(df.dtypes)

    # Get all products
    products = df['Campaign_Name'].unique()
    print(f"\nAvailable products: {list(products)}")

    # Create separate groups for each product
    product_groups = {}
    for product in products:
        product_groups[product] = df[df['Campaign_Name'] == product].copy()

    # Print group sizes
    for product, group in product_groups.items():
        print(f"{product}: {group.shape[0]} rows")

    # Basic statistics
    print("\n=== BASIC STATISTICS ===")
    for product, group in product_groups.items():
        print(f"\n{product} Statistics:")
        print(group[['Spend', 'Impressions', 'Reach', 'Clicks', 'Searches', 'View_Content', 'Add_to_Cart', 'Purchase']].describe())

    # Calculate additional metrics for all products
    print("\n=== ADDITIONAL METRICS ANALYSIS ===")
    for product, group in product_groups.items():
        group['CTR'] = group['Clicks'] / group['Impressions']
        group['View_Content_Rate'] = group['View_Content'] / group['Clicks']
        group['Add_to_Cart_Rate'] = group['Add_to_Cart'] / group['View_Content']
        group['Purchase_Rate'] = group['Purchase'] / group['Add_to_Cart']
        group['Overall_Conversion_Rate'] = group['Purchase'] / group['Clicks']
        
        # Replace infinite values with NaN and then fill with 0
        product_groups[product] = group.replace([np.inf, -np.inf], np.nan).fillna(0)

    # EDA - Visualization for all products
    print("\n=== EXPLORATORY DATA ANALYSIS ===")

    # 1. Spend Analysis
    fig, (ax1, ax2) = plt.subplots(ncols=2, figsize=(15, 5))

    # Line plot for daily spend
    for product, group in product_groups.items():
        avg_spend = group['Spend'].mean()
        ax1 = sns.lineplot(data=group, x='Date', y='Spend', label=product, ax=ax1)
        ax1.axhline(y=avg_spend, ls='--', label=f'{product} avg')

    ax1.set_title('Daily Amount Spent by Product', size=15)
    ax1.legend(fontsize=8, loc='upper right')
    ax1.set_xticklabels(ax1.get_xticklabels(), size=7)

    # Bar plot for total spend
    total_spends = [group['Spend'].sum() for group in product_groups.values()]
    ax2 = sns.barplot(x=list(product_groups.keys()), y=total_spends)
    ax2.set_ylabel('Total Spend')
    ax2.set_title('Total Amount Spent by Product', size=15)
    plt.xticks(rotation=45)

    plt.tight_layout()
    plt.show()

    # 2. Purchase Analysis
    fig, (ax1, ax2) = plt.subplots(ncols=2, figsize=(15, 5))

    # Line plot for daily purchases
    for product, group in product_groups.items():
        avg_purchase = group['Purchase'].mean()
        ax1 = sns.lineplot(data=group, x='Date', y='Purchase', label=product, ax=ax1)
        ax1.axhline(y=avg_purchase, ls='--', label=f'{product} avg')

    ax1.set_title('Daily Purchases by Product', size=15)
    ax1.legend(fontsize=8, loc='upper right')
    ax1.set_xticklabels(ax1.get_xticklabels(), size=7)

    # Bar plot for total purchases
    total_purchases = [group['Purchase'].sum() for group in product_groups.values()]
    ax2 = sns.barplot(x=list(product_groups.keys()), y=total_purchases)
    ax2.set_ylabel('Total Purchases')
    ax2.set_title('Total Purchases by Product', size=15)
    plt.xticks(rotation=45)

    plt.tight_layout()
    plt.show()

    # Statistical Testing - Compare all products
    print("\n=== STATISTICAL TESTING ===")

    # Normality test for key metrics
    def check_normality_all_products(metric_name):
        print(f"\nNormality Tests for {metric_name}:")
        for product, group in product_groups.items():
            if metric_name in group.columns:
                stat, p_value = shapiro(group[metric_name])
                print(f"  {product}: Shapiro-Wilk p-value = {p_value:.4f}")

    # Check normality for key metrics
    for metric in ['Purchase', 'CTR', 'Overall_Conversion_Rate']:
        check_normality_all_products(metric)

    # Perform ANOVA or Kruskal-Wallis test for multiple group comparison
    def perform_multiple_comparison(metric_name):
        print(f"\n--- Multiple Comparison Test for {metric_name} ---")
        
        # Prepare data for testing
        data_groups = []
        for product, group in product_groups.items():
            if metric_name in group.columns:
                data_groups.append(group[metric_name])
        
        # Check if all groups are normally distributed
        all_normal = True
        for i, data in enumerate(data_groups):
            stat, p_value = shapiro(data)
            if p_value < 0.05:
                all_normal = False
                break
        
        if all_normal and len(data_groups) >= 2:
            # Use ANOVA for normally distributed data
            f_stat, p_value = f_oneway(*data_groups)
            test_type = "One-way ANOVA"
            print(f"Test used: {test_type}")
            print(f"F-statistic: {f_stat:.4f}")
            print(f"P-value: {p_value:.4f}")
        else:
            # Use Kruskal-Wallis test for non-normal data
            h_stat, p_value = kruskal(*data_groups)
            test_type = "Kruskal-Wallis test"
            print(f"Test used: {test_type}")
            print(f"H-statistic: {h_stat:.4f}")
            print(f"P-value: {p_value:.4f}")
        
        # Interpretation
        alpha = 0.05
        if p_value < alpha:
            print(f"Result: Statistically significant difference between products (p < {alpha})")
            print("Conclusion: At least one product performs differently")
            
            # Perform pairwise comparisons to find which products differ
            print("\nPairwise Comparisons (Mann-Whitney U tests):")
            product_names = list(product_groups.keys())
            for i in range(len(product_names)):
                for j in range(i+1, len(product_names)):
                    product_a = product_names[i]
                    product_b = product_names[j]
                    if metric_name in product_groups[product_a].columns and metric_name in product_groups[product_b].columns:
                        stat, p_val = mannwhitneyu(product_groups[product_a][metric_name], 
                                                product_groups[product_b][metric_name])
                        significance = "SIGNIFICANT" if p_val < alpha else "not significant"
                        print(f"  {product_a} vs {product_b}: p-value = {p_val:.4f} ({significance})")
        else:
            print(f"Result: No statistically significant difference between products (p ≥ {alpha})")
            print("Conclusion: All products perform similarly")

    # Perform multiple comparison tests for key metrics
    metrics_to_test = ['Purchase', 'CTR', 'Overall_Conversion_Rate', 'Add_to_Cart', 'View_Content']

    for metric in metrics_to_test:
        if all(metric in group.columns for group in product_groups.values()):
            perform_multiple_comparison(metric)

    # Business Metrics Analysis for all products
    print("\n=== BUSINESS METRICS COMPARISON ===")

    business_metrics = {}
    for product, group in product_groups.items():
        business_metrics[product] = {
            'Total_Spend': group['Spend'].sum(),
            'Total_Purchases': group['Purchase'].sum(),
            'Avg_Cost_per_Purchase': group['Spend'].sum() / group['Purchase'].sum() if group['Purchase'].sum() > 0 else 0,
            'Total_Impressions': group['Impressions'].sum(),
            'Total_Clicks': group['Clicks'].sum(),
            'CTR': group['CTR'].mean(),
            'Overall_Conversion_Rate': group['Overall_Conversion_Rate'].mean(),
            'ROI': (group['Purchase'].sum() * 100) / group['Spend'].sum() if group['Spend'].sum() > 0 else 0
        }

    business_df = pd.DataFrame(business_metrics).T
    print(business_df)

    # Ranking Analysis
    print("\n=== PRODUCT RANKING ===")

    # Calculate scores for each product (higher is better)
    def calculate_product_score(row):
        score = 0
        # Higher purchases are better
        score += 0.3 * (row['Total_Purchases'] / business_df['Total_Purchases'].max())
        # Lower cost per purchase is better (inverse)
        if row['Avg_Cost_per_Purchase'] > 0:
            score += 0.3 * (1 / (row['Avg_Cost_per_Purchase'] / business_df['Avg_Cost_per_Purchase'].min()))
        # Higher CTR is better
        score += 0.2 * (row['CTR'] / business_df['CTR'].max())
        # Higher conversion rate is better
        score += 0.2 * (row['Overall_Conversion_Rate'] / business_df['Overall_Conversion_Rate'].max())
        return score

    business_df['Score'] = business_df.apply(calculate_product_score, axis=1)
    business_df['Rank'] = business_df['Score'].rank(ascending=False)

    # Sort by rank
    business_df = business_df.sort_values('Rank')
    print("\nProduct Ranking (1 = Best):")
    print(business_df[['Score', 'Rank']])

    # Final Recommendation
    print("\n=== FINAL RECOMMENDATION ===")
    best_product = business_df.index[0]
    best_score = business_df.loc[best_product, 'Score']
    second_best = business_df.index[1]
    second_score = business_df.loc[second_best, 'Score']

    improvement = ((best_score - second_score) / second_score) * 100

    print(f"🎯 TOP PERFORMING PRODUCT: {best_product}")
    print(f"   Overall Score: {best_score:.4f}")
    print(f"   Improvement over {second_best}: {improvement:.2f}%")

    print(f"\n📊 PRODUCT RANKINGS:")
    for rank, (product, row) in enumerate(business_df.iterrows(), 1):
        print(f"   {rank}. {product} (Score: {row['Score']:.4f})")

    product_ranking = []

    for rank, (product, row) in enumerate(business_df.iterrows(), 1):
        product_ranking.append({
            "rank": rank,
            "product": product,
            "score": round(row["Score"], 4)
        })

    # Additional insights
    print("\n=== KEY INSIGHTS ===")
    print("1. Conversion Funnel Analysis:")
    for product, group in product_groups.items():
        print(f"   {product}:")
        print(f"     CTR: {group['CTR'].mean():.2%}")
        print(f"     View Content Rate: {group['View_Content_Rate'].mean():.2%}")
        print(f"     Add to Cart Rate: {group['Add_to_Cart_Rate'].mean():.2%}")
        print(f"     Purchase Rate: {group['Purchase_Rate'].mean():.2%}")

    # store the key insights in a variable to return later
    insights = []

    for product, group in product_groups.items():
        insights.append({
            "product": product,
            "CTR": round(group['CTR'].mean(), 4),
            "View_Content_Rate": round(group['View_Content_Rate'].mean(), 4),
            "Add_to_Cart_Rate": round(group['Add_to_Cart_Rate'].mean(), 4),
            "Purchase_Rate": round(group['Purchase_Rate'].mean(), 4)
        })

    print("\n2. ROI Analysis:")
    for product, metrics in business_metrics.items():
        print(f"   {product} ROI: {metrics['ROI']:.2f}%")
    
    # store the ROI in a variable to return later
    roi_results = []

    for product, metrics in business_metrics.items():
        roi_results.append({
            "product": product,
            "ROI": round(metrics["ROI"], 4)   # store number (not formatted string)
        })

    print("\n3. Cost Efficiency:")
    for product, metrics in business_metrics.items():
        print(f"   {product} Cost per Purchase: ${metrics['Avg_Cost_per_Purchase']:.2f}")
    
    cost_efficiency_results = []

    for product, metrics in business_metrics.items():
        cost_efficiency_results.append({
            "product": product,
            "cost_per_purchase": round(metrics["Avg_Cost_per_Purchase"], 2)
        })

    # Performance Matrix
    print("\n4. Performance Matrix:")
    performance_matrix = business_df[['Total_Purchases', 'CTR', 'Overall_Conversion_Rate', 'ROI']]
    performance_matrix = (performance_matrix - performance_matrix.min()) / (performance_matrix.max() - performance_matrix.min())
    print("   (Normalized scores: 0 = Worst, 1 = Best)")
    print(performance_matrix)

    # the ml part
    def proper_ml_predictions(df):
        print("=== PROPER ML PREDICTIONS: REVENUE & SPEND OPTIMIZATION ===")
        
        # Data Preparation
        df['Date'] = pd.to_datetime(df['Date'])
        df = df.sort_values(['Campaign_Name', 'Date'])
        
        # Basic Data Validation
        print(f"Dataset shape: {df.shape}")
        print(f"Date range: {df['Date'].min()} to {df['Date'].max()}")
        print(f"Campaigns: {df['Campaign_Name'].unique().tolist()}")
        
        # 1. DATA EXPLORATION AND CLEANING
        print("\n📊 DATA EXPLORATION AND CLEANING")
        print("=" * 50)
        
        def explore_and_clean_data(df):
            # Check for missing values
            print("Missing values:")
            print(df.isnull().sum())
            
            # Check data types
            print("\nData types:")
            print(df.dtypes)
            
            # Remove any infinite values
            numeric_cols = ['Spend', 'Impressions', 'Reach', 'Clicks', 'Searches', 
                        'View_Content', 'Add_to_Cart', 'Purchase']
            
            for col in numeric_cols:
                df[col] = pd.to_numeric(df[col], errors='coerce')
                df[col] = df[col].fillna(df[col].mean())
            
            # Calculate basic metrics
            df['CTR'] = df['Clicks'] / df['Impressions']
            df['Conversion_Rate'] = df['Purchase'] / df['Clicks']
            df['Cost_per_Purchase'] = df['Spend'] / df['Purchase']
            df['Revenue'] = df['Purchase'] * 100  # Assuming $100 per purchase
            df['ROI'] = (df['Revenue'] - df['Spend']) / df['Spend'] * 100
            
            # Handle outliers - cap at 99th percentile
            for col in numeric_cols + ['CTR', 'Conversion_Rate', 'ROI']:
                if col in df.columns:
                    upper_limit = df[col].quantile(0.99)
                    lower_limit = df[col].quantile(0.01)
                    df[col] = np.clip(df[col], lower_limit, upper_limit)
            
            return df
        
        df_clean = explore_and_clean_data(df)
        
        # 2. BASIC PERFORMANCE ANALYSIS (Only Daily Trends)
        #print("\n📈 BASIC PERFORMANCE ANALYSIS - DAILY TRENDS")
        #print("=" * 50)
        
        def plot_campaign_performance(df):
            # Aggregate campaign performance for calculations
            campaign_stats = df.groupby('Campaign_Name').agg({
                'Spend': 'sum',
                'Revenue': 'sum',
                'Purchase': 'sum',
                'Clicks': 'sum',
                'Impressions': 'sum',
                'ROI': 'mean'
            }).reset_index()
            
            campaign_stats['CTR'] = campaign_stats['Clicks'] / campaign_stats['Impressions']
            campaign_stats['Conversion_Rate'] = campaign_stats['Purchase'] / campaign_stats['Clicks']
            campaign_stats['Cost_per_Purchase'] = campaign_stats['Spend'] / campaign_stats['Purchase']
            
            # Create only the daily trends plot (removed first two graphs)
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))
            
            # Plot 1: CTR and Conversion Rates (previously plot 3)
            x = np.arange(len(campaign_stats))
            width = 0.35
            ax1.bar(x - width/2, campaign_stats['CTR'] * 100, width, label='CTR (%)', alpha=0.7)
            ax1.bar(x + width/2, campaign_stats['Conversion_Rate'] * 100, width, label='Conversion Rate (%)', alpha=0.7)
            ax1.set_xlabel('Campaign')
            ax1.set_ylabel('Rate (%)')
            ax1.set_title('CTR vs Conversion Rate')
            ax1.set_xticks(x)
            ax1.set_xticklabels([name.split()[0] for name in campaign_stats['Campaign_Name']], rotation=45)
            ax1.legend()
            ax1.grid(True, alpha=0.3, axis='y')
            
            # Plot 2: Daily Trends (previously plot 4)
            daily_data = df.groupby(['Date', 'Campaign_Name']).agg({'Revenue': 'sum', 'Spend': 'sum'}).reset_index()
            for campaign in df['Campaign_Name'].unique():
                campaign_data = daily_data[daily_data['Campaign_Name'] == campaign]
                ax2.plot(campaign_data['Date'], campaign_data['Revenue'], label=campaign, marker='o', markersize=3)
            
            ax2.set_xlabel('Date')
            ax2.set_ylabel('Daily Revenue ($)')
            ax2.set_title('Daily Revenue Trends by Campaign')
            ax2.legend()
            ax2.tick_params(axis='x', rotation=45)
            ax2.grid(True, alpha=0.3)
            
            plt.tight_layout()
            plt.show()
            
            return campaign_stats
        
    # campaign_stats = plot_campaign_performance(df_clean)
        
        # 3. OPTIMAL AD SPEND PREDICTION (Proper Training)
        print("\n🎯 OPTIMAL AD SPEND PREDICTION")
        print("=" * 50)
        
        def train_optimal_spend_model(df):
            results = {}
            
            fig, axes = plt.subplots(2, 2, figsize=(15, 10))
            axes = axes.ravel()
            
            for idx, campaign in enumerate(df['Campaign_Name'].unique()):
                campaign_data = df[df['Campaign_Name'] == campaign].copy()
                
                if len(campaign_data) < 10:
                    print(f"⚠️  Insufficient data for {campaign}: {len(campaign_data)} records")
                    continue
                
                # Create features based on logical relationships
                campaign_data = campaign_data.sort_values('Date')
                
                # Feature engineering
                features = [
                    'Impressions', 'Clicks', 'View_Content', 'Add_to_Cart',
                    'CTR', 'Conversion_Rate', 'Revenue'
                ]
                
                # Create lag features
                for lag in [1, 2, 3]:
                    campaign_data[f'Spend_lag_{lag}'] = campaign_data['Spend'].shift(lag)
                    campaign_data[f'Revenue_lag_{lag}'] = campaign_data['Revenue'].shift(lag)
                    features.extend([f'Spend_lag_{lag}', f'Revenue_lag_{lag}'])
                
                # Calculate ROI efficiency (target for optimization)
                campaign_data['ROI_efficiency'] = campaign_data['Revenue'] / campaign_data['Spend']
                
                # Remove rows with missing values from lag features
                campaign_data = campaign_data.dropna()
                
                if len(campaign_data) < 5:
                    continue
                
                # Prepare features and target
                X = campaign_data[features]
                y = campaign_data['Spend']  # We want to predict optimal spend
                
                # Split data chronologically
                split_idx = int(len(X) * 0.7)
                X_train, X_test = X.iloc[:split_idx], X.iloc[split_idx:]
                y_train, y_test = y.iloc[:split_idx], y.iloc[split_idx:]
                
                if len(X_train) == 0 or len(X_test) == 0:
                    continue
                
                # Scale features
                scaler = StandardScaler()
                X_train_scaled = scaler.fit_transform(X_train)
                X_test_scaled = scaler.transform(X_test)
                
                # Train Random Forest model
                model = RandomForestRegressor(
                    n_estimators=100,
                    max_depth=10,
                    random_state=42,
                    min_samples_split=5,
                    min_samples_leaf=2
                )
                
                model.fit(X_train_scaled, y_train)
                
                # Make predictions
                y_pred = model.predict(X_test_scaled)
                
                # Calculate metrics
                mae = mean_absolute_error(y_test, y_pred)
                rmse = np.sqrt(mean_squared_error(y_test, y_pred))
                r2 = r2_score(y_test, y_pred)
                
                # Calculate optimal spend range (based on high-ROI periods)
                high_roi_threshold = campaign_data['ROI_efficiency'].quantile(0.7)
                optimal_periods = campaign_data[campaign_data['ROI_efficiency'] >= high_roi_threshold]
                
                if len(optimal_periods) > 0:
                    optimal_spend = optimal_periods['Spend'].mean()
                    current_spend = campaign_data['Spend'].mean()
                    improvement_pct = ((optimal_spend - current_spend) / current_spend) * 100
                else:
                    optimal_spend = current_spend = campaign_data['Spend'].mean()
                    improvement_pct = 0
                
                results[campaign] = {
                    'model': model,
                    'current_avg_spend': current_spend,
                    'optimal_spend': optimal_spend,
                    'improvement_pct': improvement_pct,
                    'mae': mae,
                    'r2': r2,
                    'test_size': len(X_test)
                }
                
                # Plot actual vs predicted
                ax = axes[idx]
                ax.scatter(y_test, y_pred, alpha=0.6, s=50)
                ax.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
                ax.set_xlabel('Actual Spend ($)')
                ax.set_ylabel('Predicted Spend ($)')
                ax.set_title(f'{campaign}\nMAE: ${mae:.0f}, R²: {r2:.2f}')
                ax.grid(True, alpha=0.3)
            
            plt.tight_layout()
            plt.suptitle('SPEND PREDICTION: ACTUAL VS PREDICTED', fontsize=16, fontweight='bold', y=1.02)
            plt.show()
            
            return results
        
        spend_results = train_optimal_spend_model(df_clean)
        
        # 4. REVENUE FORECASTING (Proper Time Series)
        print("\n📈 REVENUE FORECASTING")
        print("=" * 50)
        
        def train_revenue_forecasting_model(df):
            results = {}
            
            fig, axes = plt.subplots(2, 2, figsize=(15, 10))
            axes = axes.ravel()
            
            for idx, campaign in enumerate(df['Campaign_Name'].unique()):
                campaign_data = df[df['Campaign_Name'] == campaign].copy().sort_values('Date')
                
                if len(campaign_data) < 15:  # Need sufficient history
                    print(f"⚠️  Insufficient history for {campaign}: {len(campaign_data)} records")
                    continue
                
                # Create time series features
                features = []
                
                # Lag features
                for lag in [1, 2, 3, 7]:
                    campaign_data[f'Revenue_lag_{lag}'] = campaign_data['Revenue'].shift(lag)
                    campaign_data[f'Spend_lag_{lag}'] = campaign_data['Spend'].shift(lag)
                    campaign_data[f'Clicks_lag_{lag}'] = campaign_data['Clicks'].shift(lag)
                    features.extend([f'Revenue_lag_{lag}', f'Spend_lag_{lag}', f'Clicks_lag_{lag}'])
                
                # Rolling statistics
                for window in [3, 7]:
                    campaign_data[f'Revenue_rollmean_{window}'] = campaign_data['Revenue'].rolling(window).mean()
                    campaign_data[f'Revenue_rollstd_{window}'] = campaign_data['Revenue'].rolling(window).std()
                    features.extend([f'Revenue_rollmean_{window}', f'Revenue_rollstd_{window}'])
                
                # Date features
                campaign_data['day_of_week'] = campaign_data['Date'].dt.dayofweek
                campaign_data['day_of_month'] = campaign_data['Date'].dt.day
                campaign_data['is_weekend'] = (campaign_data['Date'].dt.dayofweek >= 5).astype(int)
                features.extend(['day_of_week', 'day_of_month', 'is_weekend'])
                
                # Remove rows with NaN from lag features
                campaign_data = campaign_data.dropna()
                
                if len(campaign_data) < 10:
                    continue
                
                # Prepare data
                X = campaign_data[features]
                y = campaign_data['Revenue']
                
                # Time-based split (last 30% for testing)
                split_idx = int(len(X) * 0.7)
                X_train, X_test = X.iloc[:split_idx], X.iloc[split_idx:]
                y_train, y_test = y.iloc[:split_idx], y.iloc[split_idx:]
                dates_test = campaign_data['Date'].iloc[split_idx:]
                
                if len(X_train) == 0 or len(X_test) == 0:
                    continue
                
                # Scale features
                scaler = StandardScaler()
                X_train_scaled = scaler.fit_transform(X_train)
                X_test_scaled = scaler.transform(X_test)
                
                # Train XGBoost model
                model = xgb.XGBRegressor(
                    n_estimators=100,
                    learning_rate=0.1,
                    max_depth=6,
                    random_state=42,
                    subsample=0.8,
                    colsample_bytree=0.8
                )
                
                model.fit(X_train_scaled, y_train)
                
                # Make predictions
                y_pred = model.predict(X_test_scaled)
                
                # Calculate metrics
                mae = mean_absolute_error(y_test, y_pred)
                rmse = np.sqrt(mean_squared_error(y_test, y_pred))
                r2 = r2_score(y_test, y_pred)
                
                # Generate 7-day forecast
                last_data = campaign_data.iloc[-1][features].values.reshape(1, -1)
                last_data_scaled = scaler.transform(last_data)
                
                forecast = []
                for i in range(7):
                    pred = model.predict(last_data_scaled)[0]
                    forecast.append(pred)
                    # Update features for next prediction (simplified)
                    # In practice, you'd update all lag features properly
                
                results[campaign] = {
                    'model': model,
                    'historical_avg_revenue': campaign_data['Revenue'].mean(),
                    'forecast_avg_revenue': np.mean(forecast),
                    'forecast_values': forecast,
                    'mae': mae,
                    'r2': r2,
                    'test_size': len(X_test)
                }
                
                # Plot historical vs predicted
                ax = axes[idx]
                ax.plot(dates_test, y_test.values, 'b-', label='Actual Revenue', linewidth=2, alpha=0.8)
                ax.plot(dates_test, y_pred, 'r--', label='Predicted Revenue', linewidth=2, alpha=0.8)
                ax.set_xlabel('Date')
                ax.set_ylabel('Revenue ($)')
                ax.set_title(f'{campaign}\nMAE: ${mae:.0f}, R²: {r2:.2f}')
                ax.legend()
                ax.tick_params(axis='x', rotation=45)
                ax.grid(True, alpha=0.3)
            
            plt.tight_layout()
            plt.suptitle('REVENUE FORECASTING: ACTUAL VS PREDICTED', fontsize=16, fontweight='bold', y=1.02)
            plt.show()
            
            return results
        
        revenue_results = train_revenue_forecasting_model(df_clean)
        
        # 5. FINAL RECOMMENDATIONS AND SUMMARY
        print("\n🎯 FINAL RECOMMENDATIONS")
        print("=" * 50)
        
        def create_final_recommendations(spend_results, revenue_results):
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
            
            # Spend Optimization Recommendations
            campaigns = list(spend_results.keys())
            current_spends = [spend_results[camp]['current_avg_spend'] for camp in campaigns]
            optimal_spends = [spend_results[camp]['optimal_spend'] for camp in campaigns]
            improvements = [spend_results[camp]['improvement_pct'] for camp in campaigns]
            
            x = np.arange(len(campaigns))
            width = 0.35
            
            bars1 = ax1.bar(x - width/2, current_spends, width, label='Current Spend', 
                        color='lightcoral', alpha=0.8)
            bars2 = ax1.bar(x + width/2, optimal_spends, width, label='Recommended Spend', 
                        color='lightgreen', alpha=0.8)
            
            ax1.set_xlabel('Campaign')
            ax1.set_ylabel('Daily Spend ($)')
            ax1.set_title('OPTIMAL SPEND RECOMMENDATIONS', fontweight='bold')
            ax1.set_xticks(x)
            ax1.set_xticklabels([camp.split()[0] for camp in campaigns], rotation=45)
            ax1.legend()
            ax1.grid(True, alpha=0.3, axis='y')
            
            # Add improvement percentages
            for i, (curr, opt, imp) in enumerate(zip(current_spends, optimal_spends, improvements)):
                ax1.text(i, max(curr, opt) * 1.05, f'{imp:+.1f}%', 
                    ha='center', va='bottom', fontweight='bold', fontsize=10,
                    color='green' if imp > 0 else 'red')
            
            # Revenue Forecast Summary
            rev_campaigns = list(revenue_results.keys())
            historical_rev = [revenue_results[camp]['historical_avg_revenue'] for camp in rev_campaigns]
            forecast_rev = [revenue_results[camp]['forecast_avg_revenue'] for camp in rev_campaigns]
            growth_rates = [((forecast_rev[i] - historical_rev[i]) / historical_rev[i] * 100) 
                        for i in range(len(rev_campaigns))]
            
            x_rev = np.arange(len(rev_campaigns))
            
            bars3 = ax2.bar(x_rev - width/2, historical_rev, width, label='Historical Avg', 
                        color='lightblue', alpha=0.8)
            bars4 = ax2.bar(x_rev + width/2, forecast_rev, width, label='7-Day Forecast', 
                        color='lightgreen', alpha=0.8)
            
            ax2.set_xlabel('Campaign')
            ax2.set_ylabel('Revenue ($)')
            ax2.set_title('REVENUE FORECAST SUMMARY', fontweight='bold')
            ax2.set_xticks(x_rev)
            ax2.set_xticklabels([camp.split()[0] for camp in rev_campaigns], rotation=45)
            ax2.legend()
            ax2.grid(True, alpha=0.3, axis='y')
            
            # Add growth percentages
            for i, (hist, fcst, growth) in enumerate(zip(historical_rev, forecast_rev, growth_rates)):
                ax2.text(i, max(hist, fcst) * 1.05, f'{growth:+.1f}%', 
                    ha='center', va='bottom', fontweight='bold', fontsize=10,
                    color='green' if growth > 0 else 'red')
            
            plt.tight_layout()
            plt.show()
            
            # Print actionable recommendations
            print("\n🚀 ACTIONABLE RECOMMENDATIONS:")
            print("-" * 40)

            # prinitng the results 
            for campaign in campaigns:
                if campaign in spend_results and campaign in revenue_results:
                    spend_data = spend_results[campaign]
                    revenue_data = revenue_results[campaign]
                    
                    print(f"\n📱 {campaign}:")
                    print(f"   💰 Spend: ${spend_data['current_avg_spend']:.0f} → ${spend_data['optimal_spend']:.0f} ({spend_data['improvement_pct']:+.1f}%)")
                    print(f"   📈 Revenue: ${revenue_data['historical_avg_revenue']:.0f} → ${revenue_data['forecast_avg_revenue']:.0f}")
                    print(f"   📊 Model R²: Spend={spend_data['r2']:.2f}, Revenue={revenue_data['r2']:.2f}")
                    
                    # Business logic recommendations
                    if spend_data['improvement_pct'] > 15:
                        rec = "STRONGLY INCREASE BUDGET"
                    elif spend_data['improvement_pct'] > 5:
                        rec = "MODERATELY INCREASE BUDGET"
                    elif spend_data['improvement_pct'] < -10:
                        rec = "REDUCE BUDGET"
                    else:
                        rec = "MAINTAIN CURRENT BUDGET"
                    
                    print(f"   ✅ RECOMMENDATION: {rec}")

            
            for campaign in campaigns:
                if campaign in spend_results and campaign in revenue_results:
                    spend_data = spend_results[campaign]
                    revenue_data = revenue_results[campaign]

                    # Business logic recommendation
                    if spend_data['improvement_pct'] > 15:
                        rec = "STRONGLY INCREASE BUDGET"
                    elif spend_data['improvement_pct'] > 5:
                        rec = "MODERATELY INCREASE BUDGET"
                    elif spend_data['improvement_pct'] < -10:
                        rec = "REDUCE BUDGET"
                    else:
                        rec = "MAINTAIN CURRENT BUDGET"

                    # pushing structured result instead of printing
                    recommendations.append({
                        "campaign": campaign,
                        "spend": {
                            "current_avg_spend": float(round(spend_data['current_avg_spend'], 2)),
                            "optimal_spend": float(round(spend_data['optimal_spend'], 2)),
                            "improvement_pct": float(round(spend_data['improvement_pct'], 2)),
                            "r2": float(round(spend_data['r2'], 3))
                        },
                        "revenue": {
                            "historical_avg_revenue": float(round(revenue_data['historical_avg_revenue'], 2)),
                            "forecast_avg_revenue": float(round(revenue_data['forecast_avg_revenue'], 2)),
                            "r2": float(round(revenue_data['r2'], 3))
                        },
                        "recommendation": rec
                    })
        
        create_final_recommendations(spend_results, revenue_results)
        
        return {
            'spend_predictions': spend_results,
            'revenue_forecasts': revenue_results,
            'processed_data': df_clean
        }

    # Run the proper ML predictions
    print("Starting Proper ML Training and Predictions...")
    df = pd.read_csv(f"{selected_category}.csv")
    results = proper_ml_predictions(df)

    print("\n" + "="*60)
    print("ML PREDICTIONS COMPLETED SUCCESSFULLY!")
    print("="*60)

    # printing the object returned by the proper_ml_predictions function
    # print("Here are the results: ", results)







    return {
        "top_performing_product": {
            "name": best_product,
            "score": best_score,
            "second_best": second_best,
            "improvement_over_second": improvement,
        },
        "product_rankings": product_ranking,
        "key_insights": insights,
        "roi_analysis": roi_results,
        "cost_efficiency": cost_efficiency_results,
        "campaign_recommendations": recommendations,
        "message": "Analysis complete",
    }