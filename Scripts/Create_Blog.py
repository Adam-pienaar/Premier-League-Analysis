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
  font-family: 'Inter', sans-serif; 'DM Serif Display', 'Fira Code';
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

/*Nav*/
nav {{
  position: fixed; top: 3px; left: 0; right: 0; background: rgba(15,17,23,0.92); backdrop-filter: blur(8px); border-bottom: 1px solid var(--border); padding: 0.75rem 2rem; display: flex; align-items: center; justify-content: space-between; z-index: 99;
}}
nav .logo {{
    font-family: 'Inter'; font-weight: 700; font-size: 0.95rem; color: var(--accent); letter-spacing: 0.05em;
}}
nav .nav-links a {{
    display: flex; gap: 1.5rem; list-style: none; 
}}
nav .nav-links a {{
    font-family: 'Inter'; font-weight: 500; color: var(--muted); font-size: 0.9rem; text-decoration: none; letter-spacing: 0.08em; text-transform: uppercase; transition: color 0.2s;
}}
nav .nav-links a:hover {{ color: var(--fg); }}

</style>
</head>
<body>
</body>
</html>"""

with open(OUTPUT, 'w') as f:
    f.write(html)

print(f"Blog saved to {OUTPUT}")