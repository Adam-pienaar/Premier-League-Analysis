#OLS regression analysis: Premier League wage expenditure vs club performance in the 2023-2024 season
# Models: M1: Final Points ~ Wage costs
#         M2: Final Points ~ Revenue
#         M3: Final Points ~ Wage costs + Revenue
import pandas as pd
import numpy as np
from scipy import stats
import json
import os

INPUT = 'data/processed/cleaned_data.csv'
OUTPUT = 'outputs'

def ols(y_col, x_cols, data, label):
    y = data[y_col].values
    X = np.column_stack([np.ones(len(data))] + [data[c].values for c in x_cols])
    n, k = X.shape

    #COEFFICIENTS
    beta = np.linalg.lstsq(X, y, rcond=None)[0]
    y_hat = X @ beta
    residuals = y - y_hat

    #R-squared
    ss_residuals = residuals @ residuals
    ss_total = ((y - y.mean()) ** 2).sum()
    r_squared = 1 - ss_residuals / ss_total
    r_sqaured_adj = 1 - (1 - r_squared) * (n - 1) / (n - k)

    #Standard errors and p-values
    sigma_squared = ss_residuals / (n - k)
    cov_beta = sigma_squared * np.linalg.inv(X.T @ X)
    se = np.sqrt(np.diag(cov_beta))
    t_stats = beta / se
    p_value = [2 * (1 - stats.t.cdf(abs(t), df=n-k)) for t in t_stats]

    #Build the results row
    names = ['const'] + x_cols
    rows = []
    for nm, b, s, t, p in zip(names, beta, se, t_stats, p_value):
        sig = '***' if p <0.01 else ('**' if p < 0.05 else ('*' if p < 0.1 else ''))
        rows.append({'model': label, 'variable': nm, 'coefficient': round(b, 4), 'se': round(s, 4), 't_stat': round(t, 3), 'p_value': round(p, 4), 'significance': sig})
    return rows, round(r_squared, 4), round(r_sqaured_adj, 4)
    
def main():
    os.makedirs(OUTPUT, exist_ok=True)
    df = pd.read_csv(INPUT)
    print(f"Data loaded: {len(df)} clubs from {INPUT}\n")

    all_rows = []

    #M1: Points ~ Wage Costs
    m1_rows, m1_r2, m1_adj_r2 = ols('Final Points', ['Wage Cost £m'], df, 'M1: Points ~ Wage Costs')
    all_rows += m1_rows
    #M2: Points ~ Revenue
    m2_rows, m2_r2, m2_adj_r2 = ols('Final Points', ['Revenue £m'], df, 'M2: Points ~ Revenue')
    all_rows += m2_rows
    #M3: Points ~ Wage Costs + Revenue
    m3_rows, m3_r2, m3_adj_r2 = ols('Final Points', ['Wage Cost £m', 'Revenue £m'], df, 'M3: Points ~ Wage Cost + Revenue')
    all_rows += m3_rows

    reg_df = pd.DataFrame(all_rows)
    reg_df.to_csv(f'{OUTPUT}/regression_results.csv', index=False)

    #Pearson correlations
    r_wages, p_wages = stats.pearsonr(df['Final Points'], df['Wage Cost £m'])
    r_revenue, p_revenue = stats.pearsonr(df['Final Points'], df['Revenue £m'])
    #Descriptive stats
    desc_stats = df[['Final Points', 'Goals Scored', 'Goals Conceded', 'Wage Cost £m', 'Revenue £m', 'Wage to Revenue Ratio']].describe().round(2)
    desc_stats.to_csv(f'{OUTPUT}/descriptive_stats.csv')
    #Key insights
    insights = {
        'n_clubs': int(len(df)),
        'season': '2023-2024',
        'r_wages_points': round(r_wages, 3),
        'p_wages_points': round(p_wages, 4),
        'r_revenue_points': round(r_revenue, 3),
        'p_revenue_points': round(p_revenue, 4),
        'm1_r_squared': m1_r2,
        'm1_adj_r_squared': m1_adj_r2,
        'm2_r_squared': m2_r2,
        'm2_adj_r_squared': m2_adj_r2,
        'm3_r_squared': m3_r2,
        'm3_adj_r_squared': m3_adj_r2,
        'm1_wage_coef': m1_rows[1]['coefficient'],
        'm1_wage_p': m1_rows[1]['p_value'],
        'highest_wages_club': df.loc[df['Wage Cost £m'].idxmax()]['Club'],
        'highest_wages_m': round(df['Wage Cost £m'].max(), 1),
        'lowest_wages_club': df.loc[df['Wage Cost £m'].idxmin()]['Club'],
        'lowest_wages_m': round(df['Wage Cost £m'].min(), 1),
        'avg_wages_revenue_ratio': round(df['Wage to Revenue Ratio'].mean(), 1),
        'source': 'Deloitte (2025) Annual Review of Football Finance, Table 1, p.44'
    }
    with open(f'{OUTPUT}/key_insights.json', 'w') as f:
        json.dump(insights, f, indent=2)

    #Regression summary
    with open(f'{OUTPUT}/regression_summary.txt', 'w') as f:
        f.write("Premier League Analysis)\n")
        f.write("OLS Regression Analysis: Premier League Wage Expenditure vs Club Performance (2023-2024 Season)\n")
        f.write("Premier League club Performance?\n")
        f.write("=" * 65 + "\n")

        for lable, r2, adj_r2 in [('M1: Points ~ Wage Costs', m1_r2, m1_adj_r2), ('M2: Points ~ Revenue', m2_r2, m2_adj_r2), ('M3: Points ~ Wage Costs + Revenue', m3_r2, m3_adj_r2)]:
            f.write(f"{lable}\n")
            f.write(f"R-squared: {r2}\n")
            f.write(f"Adjusted R-squared: {adj_r2}\n")
            f.write(f"{'variable':<20} {'coef':>8} {'se':>8} {'t_stat':>7} {'p-value':>7} significance\n")
            f.write(" " + "-" * 58 + "\n")
            for row in all_rows:
                f.write(f" {row['variable']:<20} {row['coefficient']:>8.4f} {row['se']:>8.4f} {row['t_stat']:>7.3f} {row['p_value']:>7.4f} {row['significance']}\n")
            f.write("\n")

            f.write(f"Wages-Points Pearson r = {r_wages:.3f} (p={p_wages:.4f})\n")
            f.write(f"Revenue-Points Pearson r = {r_revenue:.3f} (p={p_revenue:.4f})\n")

    with open(f'{OUTPUT}/regression_summary.txt') as f:
              print(f.read())
    
if __name__ == "__main__":
     os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
     main()