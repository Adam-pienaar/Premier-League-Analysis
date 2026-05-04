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

<main>

<!-- INTRODUCTION -->
  <section id="introduction" class="reveal">
    <p class="section-tag">Introduction</p>
    <h2>The Research Question</h2>
    <p>
      The Premier League is the most-watched football league in the world, therefore it comes as no surprise that it is one of the most commercially successful sports competitions. The clubs generate a ridiculous amount of money, and combined in the 2024/24 season, their combined revenue was £6.3 billion. Some clubs generate more than others, and as most know, the league standings vary drastically. (Manchester City and Sheffield United had a 75-point difference)
    </p>
    <p>
      This blog analyses how clubs' wage spending may explain differences in performance, drawing on data from the Deloitte Annual Review of Football Finance 2025 and the official Premier League standings. In order to examine the relationship between club finances and league results, an OLS regression model is run.
    </p>
    <div class="callout">
      <p><strong>Research question:</strong> To what extent does higher wage spending result in better Premier League club performance?</p>
    </div>
  </section>

  <!-- DATA -->
  <section id="data" class="reveal">
    <p class="section-tag">The Data</p>
    <h2>Variables and Sources</h2>
    <p>
      Data was collected for all 20 Premier League clubs competing in the 2023/24 season. Financial figures are sourced from Deloitte's Annual Review of Football Finance 2025 (Table 1, p.44), which compiles data from company and group financial statements filed at Companies House. Performance data is sourced from the official Premier League website and verified against Wikipedia.
    </p>
    <table class="reg-table">
      <thead>
        <tr>
          <th>Variable</th>
          <th>Type</th>
          <th>Description</th>
          <th>Source</th>
        </tr>
      </thead>
      <tbody>
        <tr><td>Final Points</td><td>Dependent</td><td>Total points, 2023/24 season</td><td>Premier League</td></tr>
        <tr><td>Goals Scored</td><td>Dependent</td><td>Goals scored, 2023/24</td><td>Premier League</td></tr>
        <tr><td>Goals Conceded</td><td>Dependent</td><td>Goals conceded, 2023/24</td><td>Premier League</td></tr>
        <tr><td>Wage Cost £m</td><td>Independent</td><td>Annual wage bill (£m), year end 2024</td><td>Deloitte (2025)</td></tr>
        <tr><td>Revenue £m</td><td>Independent</td><td>Total revenue (£m), year end 2024</td><td>Deloitte (2025)</td></tr>
        <tr><td>Wage to Revenue Ratio</td><td>Engineered</td><td>Wage costs as % of revenue</td><td>Calculated</td></tr>
      </tbody>
    </table>
  </section>

  <!-- FIGURES -->
<section id="findings" class="reveal">
  <p class="section-tag">Findings</p>
  <h2>Visual Insights</h2>

  <h3>Graph 1 — Wage Costs vs Final Points</h3>
  <p>
    The relationship between wage expenditure and final points is strikingly strong. The Pearson correlation of r = {findings['r_wages_points']} confirms that clubs with higher wage bills consistently finish higher in the table. Manchester City (£{findings['highest_wages_m']}m wages, 91 points) and Luton Town (£{findings['lowest_wages_m']}m wages, 26 points) represent the extremes of this relationship.
  </p>
  <div class="figure-block">
    <img src="data:image/png;base64,{graphs[1]}" alt="Graph 1 — Wage Costs vs Final Points">
    <p class="caption">Graph 1: Wage costs (£m) vs final points for all 20 Premier League clubs in 2023/24. Teal = Big Six, Golden Yellow = other clubs. Dashed blue line = OLS regression fit.</p>
  </div>

  <h3>Graph 2 — Revenue vs Final Points</h3>
  <p>
    Revenue is also strongly correlated with points (r = {findings['r_revenue_points']}), though slightly weaker than wages. This makes intuitive sense as revenue funds wages, but clubs differ in how much of their revenue they allocate to the wage bill.
  </p>
  <div class="figure-block">
    <img src="data:image/png;base64,{graphs[2]}" alt="Graph 2 — Revenue vs Final Points">
    <p class="caption">Graph 2: Total revenue (£m) vs final points. r = {findings['r_revenue_points']}, M2 R² = {findings['m2_r_squared']}.</p>
  </div>

  <h3>Graph 3 — Wage Efficiency vs Final Points</h3>
  <p>
    The wages-to-revenue ratio measures how much of a club's income goes on wages. Interestingly, this ratio does not predict performance as cleanly as some high-spending clubs (Aston Villa, Nottingham Forest) allocated over 90% of revenue to wages yet finished mid-table, while Tottenham allocated just 43% and finished 5th.
  </p>
  <div class="figure-block">
    <img src="data:image/png;base64,{graphs[3]}" alt="Graph 3 — Wage Efficiency vs Final Points">
    <p class="caption">Graph 3: Wage to revenue ratio (%) vs final points. The dotted red line marks 100% — where wage costs equal revenue.</p>
  </div>

</main>
<script>
  // Progress bar
  window.addEventListener('scroll', () => {{
    const doc = document.documentElement;
    const pct = (doc.scrollTop / (doc.scrollHeight - doc.clientHeight)) * 100;
    document.getElementById('progress-bar').style.width = pct + '%';
  }});

  // Reveal on scroll
  const observer = new IntersectionObserver((entries) => {{
    entries.forEach(e => {{ if (e.isIntersecting) e.target.classList.add('visible'); }});
  }}, {{ threshold: 0.1 }});
  document.querySelectorAll('.reveal').forEach(el => observer.observe(el));
</script>
</body>
</html>"""

with open(OUTPUT, 'w') as f:
    f.write(html)

print(f"Blog saved to {OUTPUT}")



