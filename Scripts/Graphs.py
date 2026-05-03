#Created in order to anable readers the opportunity to visualise the results of the analysis of the 2023-2024 Premier League season.

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from scipy import stats
import json
import os

INPUT_CSV = 'data/processed/cleaned_data.csv'
INPUT_REG = 'outputs/regression_results.csv'
INPUT_JSON = 'outputs/key_insights.json'
OUTPUT_DIR = 'outputs'

BG     = '#ffffff'
FG     = '#1a1a2e'
GRID   = '#e0e0e0'
ACCENT = '#2196f3'
GREEN  = '#00b4a6'
ORANGE = '#f7c948'
RED    = '#e63946'
PURPLE = '#c1395e'

BIG_SIX = {'Manchester City', 'Arsenal', 'Manchester United', 'Liverpool', 'Chelsea', 'Tottenham Hotspur'}

def base_fig(w=10, h=6):
    fig, ax = plt.subplots(figsize=(w,h), facecolor=BG)
    ax.set_facecolor(BG)
    ax.tick_params(colors=FG, labelsize=9)
    for spine in ax.spines.values():
        spine.set_edgecolor(GRID)
    ax.xaxis.label.set_color(FG)
    ax.yaxis.label.set_color(FG)
    ax.title.set_color(FG)
    ax.grid(color=GRID, linestyle='--', linewidth=0.5, alpha=0.7)
    return fig, ax

def save(fig, name):
    path = f'{OUTPUT_DIR}/{name}'
    fig.savefig(path, dpi=150, bbox_inches = 'tight', facecolor=BG)
    plt.close(fig)
    print(f"Saved: {name}")

def reg_line(ax, x, y):
    m, b, _, _, _ = stats.linregress(x, y)
    x_line = np.linspace(x.min(), x.max(), 100)
    ax.plot(x_line, m * x_line + b, color=ACCENT,
            linewidth=1.5, linestyle='--', alpha=0.8, label='Regression line')
    return m, b

def scatter_clubs(ax, df, x_col, y_col, label_all=False):
    colours = [GREEN if c in BIG_SIX else ORANGE for c in df['Club']]
    ax.scatter(df[x_col], df[y_col], c=colours, s =90, zorder=3, alpha=0.8, edgecolor='white', linewidth=0.5)
    for _, row in df.iterrows():
        if label_all or row['Club'] in BIG_SIX or row['League Position'] >=17:
            short = row['Club'].split()[0]
            ax.annotate(short, (row[x_col], row[y_col]), textcoords="offset points", xytext=(6,4), ha='center', fontsize=8, color=FG, alpha=0.9)

def big_six_legend():
    return [
        Line2D([0], [0], marker='o', color='w', markerfacecolor=GREEN,
               markersize=8, label='Big Six'),
        Line2D([0], [0], marker='o', color='w', markerfacecolor=ORANGE,
               markersize=8, label='Other clubs'),
    ]

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    df = pd.read_csv(INPUT_CSV)
    reg = pd.read_csv(INPUT_REG)
    with open(INPUT_JSON) as f:
        insights = json.load(f)

    #Graph 1: Points vs Wage Costs
    fig, ax = base_fig()
    scatter_clubs(ax, df, 'Wage Cost £m', 'Final Points')
    m, b = reg_line(ax, df['Wage Cost £m'], df['Final Points'])
    r = insights['r_wages_points']
    r_squared = insights['m1_r_squared']
    ax.set_xlabel('Wage Cost (£m)', fontsize=10)
    ax.set_ylabel('Final Points', fontsize=10)
    ax.set_title(f'Graph 1: Points vs Wage Costs (2023-2024 Premier League Season)\n' f'r = {r}, M1 R² = {r_squared}', fontsize=11, pad=12)
    ax.legend(handles=big_six_legend() + [ Line2D([0], [0], color=ACCENT, linestyle='--', label='Regression line', linewidth=1.5)], facecolor='#ffffff', edgecolor=GRID, labelcolor=FG, fontsize=9)
    save(fig, 'graph1_points_vs_wage_costs.png')

    #Graph 2: Points vs Revenue
    fig, ax = base_fig()
    scatter_clubs(ax, df, 'Revenue £m', 'Final Points')
    reg_line(ax, df['Revenue £m'], df['Final Points'])
    r_squared = insights['m2_r_squared']
    r = insights['r_revenue_points']
    ax.set_xlabel('Revenue (£m)', fontsize=10)
    ax.set_ylabel('Final Points', fontsize=10)
    ax.set_title(f'Graph 2: Points vs Revenue (2023-2024 Premier League Season)\n' f'r = {r}, M2 R² = {r_squared}', fontsize=11, pad=12)
    ax.legend(handles=big_six_legend() + [ Line2D([0], [0], color=ACCENT, linestyle='--', label='Regression line', linewidth=1.5)], facecolor='#ffffff', edgecolor=GRID, labelcolor=FG, fontsize=9)
    save(fig, 'graph2_points_vs_revenue.png')

    #Graph 3: wages/revenue ratio vs points
    fig, ax = base_fig()
    scatter_clubs(ax, df, 'Wage to Revenue Ratio', 'Final Points', label_all=True)
    r_wr, _= stats.pearsonr(df['Final Points'], df['Wage to Revenue Ratio'])
    ax.axvline(x=100, color=RED, linewidth=1, linestyle=':', alpha=0.6)
    ax.text(101, df['Final Points'].min() + 2, 'wages = revenue', color=RED, fontsize=7.5, alpha=0.7)
    ax.set_xlabel('Wage to Revenue Ratio (%)', fontsize=10)
    ax.set_ylabel('Final Points', fontsize=10)
    ax.set_title(f'Graph 3: Wage to Revenue Ratio vs Points (2023-2024 Premier League Season)\n' f'r = {r_wr:.3f}', fontsize=11, pad=12)
    ax.legend(handles=big_six_legend(), facecolor='#ffffff', edgecolor=GRID, labelcolor=FG, fontsize=9)
    save(fig, 'graph3_wage_revenue_ratio_vs_points.png')

    #Graph 4: Wage Bill bar chart
    fig, ax = base_fig(w=12, h=7)
    df_sorted = df.sort_values('League Position')
    colours = [GREEN if c in BIG_SIX else ORANGE for c in df_sorted['Club']]
    bars = ax.barh(df_sorted['Club'], df_sorted['Wage Cost £m'], color=colours, edgecolor='white', linewidth=0.7)
    for bar, val in zip(bars, df_sorted['Wage Cost £m']):
        ax.text(bar.get_width() + 3, bar.get_y() + bar.get_height()/2, f'{val:.1f}m', va='center', fontsize=8, color=FG)
    ax.set_xlabel('Wage Cost (£m)', fontsize=10)
    ax.set_title('Graph 4: Wage Bill by Final League Position)\n' '2023-2024 Premier League Season', fontsize=11, pad=12)
    ax.invert_yaxis()
    ax.legend(handles=big_six_legend(), facecolor='#ffffff', edgecolor=GRID, labelcolor=FG, fontsize=9)
    save(fig, 'graph4_wage_bill_bar_chart.png')

    #Graph 5: Predcted vs Actual Points
    m1 = reg[reg['model'] == 'M1: Points ~ Wage Costs']
    coefs = dict(zip(m1['variable'], m1['coefficient']))
    df['Predicted Points'] = coefs['const'] + coefs['Wage Cost £m'] * df['Wage Cost £m']
    fig, ax = base_fig()
    colours = [GREEN if c in BIG_SIX else ORANGE for c in df['Club']]
    ax.scatter(df['Predicted Points'], df['Final Points'], c=colours, s=90, zorder=3, linewidths=0.5, edgecolor='white',)
    mn = min(df['Predicted Points'].min(), df['Final Points'].min()) - 5
    mx = max(df['Predicted Points'].max(), df['Final Points'].max()) + 5
    ax.plot([mn, mx], [mn, mx], color=ACCENT, linestyle='--', linewidth=1.5, alpha=0.8, label='Perfect prediction')
    for _, row in df.iterrows():
        ax.annotate(row['Club'].split()[0], (row['Predicted Points'], row['Final Points']), textcoords="offset points", xytext=(6,4), fontsize=8, color=FG, alpha=0.9)
    ax.set_xlabel('Predicted Points (M1)', fontsize=10)
    ax.set_ylabel('Final Points', fontsize=10)
    ax.set_title(f'Graph 5: Predicted vs Actual Points (2023-2024 Premier League Season)\n' f'R² = {insights["m1_r_squared"]}', fontsize=11, pad=12)
    ax.legend(handles=big_six_legend() + [ Line2D([0], [0], color=ACCENT, linestyle='--', label='Perfect prediction', linewidth=1.5)], facecolor='#ffffff', edgecolor=GRID, labelcolor=FG, fontsize=9)
    save(fig, 'graph5_predicted_vs_actual_points.png')

    #Graph 6 : Goals Scorded vs Wages
    fig, ax = base_fig()
    scatter_clubs(ax, df, 'Wage Cost £m', 'Goals Scored')
    reg_line(ax, df['Wage Cost £m'], df['Goals Scored'])
    r_gs, _ = stats.pearsonr(df['Goals Scored'], df['Wage Cost £m'])
    ax.set_xlabel('Wage Cost (£m)', fontsize=10)
    ax.set_ylabel('Goals Scored', fontsize=10)
    ax.set_title(f'Graph 6: Goals Scored vs Wage Cost (2023-2024 Premier League Season)\n' f'r = {r_gs:.3f}', fontsize=11, pad=12)
    ax.legend(handles=big_six_legend() + [ Line2D([0], [0], color=ACCENT, linestyle='--', label='Regression line', linewidth=1.5)], facecolor='#ffffff', edgecolor=GRID, labelcolor=FG, fontsize=9)
    save(fig, 'graph6_goals_scored_vs_wage_cost.png')

    #Graph 7: Goals Conceded vs Wages
    fig, ax = base_fig()
    scatter_clubs(ax, df, 'Wage Cost £m', 'Goals Conceded')
    reg_line(ax, df['Wage Cost £m'], df['Goals Conceded'])
    r_gc, _ = stats.pearsonr(df['Goals Conceded'], df['Wage Cost £m'])
    ax.set_xlabel('Wage Cost (£m)', fontsize=10)
    ax.set_ylabel('Goals Conceded', fontsize=10)
    ax.set_title(f'Graph 7: Goals Conceded vs Wage Cost (2023-2024 Premier League Season)\n' f'r = {r_gc:.3f}', fontsize=11, pad=12)
    ax.legend(handles=big_six_legend() + [ Line2D([0], [0], color=ACCENT, linestyle='--', label='Regression line', linewidth=1.5)], facecolor='#ffffff', edgecolor=GRID, labelcolor=FG, fontsize=9)
    save(fig, 'graph7_goals_conceded_vs_wage_cost.png')

    print("\nAll graphs generated and saved")
if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    main()
    