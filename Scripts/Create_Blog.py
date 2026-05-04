# Creates a blog.html file 
#Hosted via GitHub Pages

import base64, json, os

OUTPUT = "Premier_League_Blog.html"

with open('outputs/key_insights.json') as f: findings = json.load(f)

graph_names = {1: 'graph1_points_vs_wage_costs', 2: 'graph2_points_vs_revenue', 3: 'graph3_wage_revenue_ratio_vs_points', 4: 'graph4_wage_bill_bar_chart', 5: 'graph5_predicted_vs_actual_points', 6: 'graph6_goals_scored_vs_wage_cost', 7: 'graph7_goals_conceded_vs_wage_cost'}

graphs = {}
for i in graph_names:
    with open(f'outputs/{graph_names[i]}.png', 'rb') as f:
        graphs[i] = base64.b64encode(f.read()).decode()

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title> Does Spending More on Wages Lead to Better Performance in the Premier League? </title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=DM+Serif+Display:ital@0;1&family=Fira+Code:wght@400;500&display=swap" rel="stylesheet">
<style>
   *, *::before, *::after {{box-sizing: border-box; margin: 0; padding: 0;}}
   :root {{
     --bg:       #ffffff;
     --surface:  #f8f8f8;
     --border:   #e0e0e0;
     --fg:       #1a1a2e;
     --muted:    #888888;
     --accent:   #2196f3;
     --green:    #00b4a6;
     --orange:   #f7c948;
     --red:      #e63946;
}}
html {{ scroll-behavior: smooth; }}
body {{
  font-family: 'Inter', sans-serif;
  background-color: var(--bg);
  color: var(--fg);
  line-height: 1.6;
  padding: 20px;
  font-size: 18px;
}}

/* Progress bar */
#progress-bar {{
  position: fixed; top: 0; left: 0; height: 3px; background: var(--accent); width: 0%; z-index: 999; transition: width 0.1s linear;
}}

/* Nav */
nav {{
  position: fixed; top: 3px; left: 0; right: 0; background: rgba(15,17,23,0.92); backdrop-filter: blur(8px); border-bottom: 1px solid var(--border); padding: 0.75rem 2rem; display: flex; align-items: center; justify-content: space-between; z-index: 99;
}}
nav .logo {{
    font-family: 'Inter'; font-weight: 700; font-size: 0.95rem; color: var(--accent); letter-spacing: 0.05em;
}}
nav .nav-links {{
    display: flex; gap: 1.5rem; list-style: none; 
}}
nav .nav-links a {{
    font-family: 'Inter'; font-weight: 500; color: var(--muted); font-size: 0.9rem; text-decoration: none; letter-spacing: 0.08em; text-transform: uppercase; transition: color 0.2s;
}}
nav .nav-links a:hover {{ color: var(--fg); }}

/* Hero */
.hero {{
  min-height: 100vh;
  display: flex; flex-direction: column;
  justify-content: center; align-items: center;
  text-align: center;
  padding: 6rem 2rem 4rem;
  background: radial-gradient(ellipse at 50% 60%, #daeeff 0%, var(--bg) 70%);
}}
.hero-tag {{
  font-family: 'Inter', sans-serif;
  font-size: 0.75rem; font-weight: 700;
  letter-spacing: 0.2em; text-transform: uppercase;
  color: var(--accent); margin-bottom: 1.5rem;
}}
.hero h1 {{
  font-family: 'DM Serif Display', serif;
  font-size: clamp(2rem, 5vw, 3.8rem);
  font-weight: 800; line-height: 1.1;
  max-width: 800px; margin-bottom: 1.5rem;
  color: var(--fg);
}}
.hero h1 span {{ color: var(--accent); }}
.hero .subtitle {{
  font-size: 1.1rem; color: var(--muted);
  max-width: 600px; margin-bottom: 3rem;
}}
.hero-stats {{
  display: flex; gap: 3rem; flex-wrap: wrap;
  justify-content: center;
}}
.stat-box {{
  text-align: center;
}}
.stat-box .num {{
  font-family: 'Inter', sans-serif;
  font-size: 2.2rem; font-weight: 800;
  color: var(--accent);
}}
.stat-box .label {{
  font-size: 0.8rem; color: var(--muted);
  font-family: 'Inter', sans-serif;
  text-transform: uppercase; letter-spacing: 0.1em;
}}

/* Main content */
main {{
  max-width: 860px; margin: 0 auto;
  padding: 4rem 2rem;
}}
section {{ margin-bottom: 5rem; }}

.section-tag {{
    font-family: 'Inter', sans-serif;
    font-size: 0.75rem; font-weight: 700;
    letter-spacing: 0.2em; text-transform: uppercase;
    color: var(--accent); margin-bottom: 1rem;
}}

h2 {{
    font-family: 'DM Serif Display', serif;
    font-size: clamp(1.5rem, 4vw, 2.5rem);
    font-weight: 800; line-height: 1.2;
    color: var(--fg); margin-bottom: 1rem;
}}

h3 {{
    font-family: 'Inter', sans-serif;
    font-size: 1.2rem; font-weight: 600;
    color: var(--fg); margin-bottom: 0.75rem;
}}

p {{ margin-bottom: 1.25rem; color: var(--muted);}}

/* Figures */
.figure-block {{
    margin: 2.5rem 0;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    overflow: hidden;
}}
.figure-block img {{
    width: 100%; display: block;
}}
.figure-block .caption {{
    padding: 0.9rem 1.2rem;
    font-size: 0.9rem; color: var(--muted);
    font-style: italic; border-top: 1px solid var(--border);
}}

/* Regression Table */
.reg-table {{
    width: 100%; border-collapse: collapse;
    font-family: 'Fira Code', monospace;
    font-size: 0.9rem; margin: 1.5rem 0;
}}
.reg-table th {{
    background: var(--surface); color: var(--muted); font-weight: 500;
    padding: 0.6rem 0.9rem; text-align: left; border-bottom: 1px solid var(--border); letter-spacing: 0.05em;
}}
.reg-table td {{
    padding: 0.6rem 0.9rem; border-bottom: 1px solid var(--border); color: var(--fg);
}}
.reg-table tr:last-child td {{ border-bottom: none; }}
.sig {{ color: var(--green); font-weight: 600;}}

/* Callout Box */
.callout {{
    background: var(--surface);
    border-left: 3px solid var(--accent);
    border-radius: 0 8px 8px 0;
    padding: 1.2rem 1.5rem;
    margin: 2rem 0;
}}
.callout p {{ margin: 0; color: var(--fg); }}

/* Key findings grid */
.findings-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1rem; margin: 2rem 0;
}}
.finding-card {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 1.2rem;
}}
.finding-card .val {{
    font-family: 'Inter', sans-serif;
    font-size: 1.7rem; font-weight: 800;
    color: var(--accent);
}}
.finding-card .desc {{
    font-size: 0.82rem; color: var(--muted);
    margin-top: 0.3rem;
}}

/* Sources */
.sources {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 1.5rem 2rem;
}}
.sources li {{
    font-size: 0.85rem; color: var(--muted);
    margin-bottom: 0.6rem; line-height: 1.5;
}}
.sources a {{ color: var(--accent); }}

/* Footer */
footer {{
    text-align: center;
    padding: 3rem 2rem;
    border-top: 1px solid var(--border);
    font-size: 0.82rem; color: var(--muted);
    font-family: 'Inter', sans-serif;
}}

/* Reveal animation */
.reveal {{
    opacity: 0; transform: translateY(24px);
    transition: opacity 0.6s ease, transform 0.6s ease;
}}
.reveal.visible {{
    opacity: 1; transform: translateY(0);
}}
</style>
</head>
<body>
<div id="progress-bar"></div>

<nav>
  <span class="logo">PL Finances 2023/24</span>
  <ul class="nav-links">
    <li><a href="#introduction">Intro</a></li>
    <li><a href="#data">Data</a></li>
    <li><a href="#findings">Findings</a></li>
    <li><a href="#conclusion">Conclusion</a></li>
    <li><a href="#sources">Sources</a></li>
  </ul>
</nav>

<!-- HERO -->
<section class="hero">
  <p class="hero-tag">BEE2041 Empirical Project &nbsp;·&nbsp; University of Exeter &nbsp;·&nbsp; 2023/24 Season</p>
  <h1>Does Money Buy Success in the Premier League?</h1>
  <p class="subtitle">An empirical analysis of how wage expenditure and revenue determine club performance across all 20 Premier League clubs in 2023/24.</p>
  <div class="hero-stats">
    <div class="stat-box">
      <div class="num">r = {findings['r_wages_points']}</div>
      <div class="label">Wages–Points Correlation</div>
    </div>
    <div class="stat-box">
      <div class="num">{int(findings['m1_r_squared']*100)}%</div>
      <div class="label">Variation Explained (M1)</div>
    </div>
    <div class="stat-box">
      <div class="num">20</div>
      <div class="label">Premier League Clubs</div>
    </div>
    <div class="stat-box">
      <div class="num">£{findings['highest_wages_m']}m</div>
      <div class="label">Highest Wage Bill (Man City)</div>
    </div>
  </div>
</section>
</body>
</html>"""

with open(OUTPUT, 'w') as f:
    f.write(html)

print(f"Blog saved to {OUTPUT}")

