import os
import re

# =========================================================================
# CONFIGURATION & METADATA
# =========================================================================
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_FILE = os.path.join(ROOT_DIR, "index.html")

# Define your display folder mapping (Folder Name on Hard Drive : Display Title)
SECTOR_MAPPING = {
    "investing-philosophy": "Investing Philosophy",
    "aerospace-defense": "Aerospace & Defense",
    "SaaS-101": "SaaS 101",
    "healthcare-it": "Healthcare IT"
}

# Default takeaways if a custom .txt file doesn't exist next to the document
DEFAULT_TAKEAWAYS = [
    "Archived research brief added directly to the intelligence pipeline.",
    "Standalone document optimized for independent desktop and mobile review.",
    "Awaiting formal underwriting evaluation and review status toggle."
]

# =========================================================================
# DASHBOARD HTML SOURCE TEMPLATE
# =========================================================================
HTML_TEMPLATE_START = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1.0" name="viewport"/>
<title>Research Queue Dashboard</title>
<style>
:root {
  --bg: #0f172a;
  --panel: #1e293b;
  --panel-light: #334155;
  --border: rgba(148, 163, 184, 0.18);
  --text: #e2e8f0;
  --muted: #94a3b8;
  --emerald: #10b981;
}

* { box-sizing: border-box; }

body {
  margin: 0;
  background: var(--bg);
  color: var(--text);
  font-family: Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  min-height: 100vh;
}

.dashboard {
  min-height: 100vh;
  padding: 24px;
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.header h1 {
  margin: 0;
  font-size: 42px;
  letter-spacing: -0.04em;
}

.header p {
  margin: 8px 0 0;
  color: var(--muted);
}

.sidebar-queue {
  width: 100%;
  background: rgba(30, 41, 59, 0.82);
  border: 1px solid var(--border);
  border-radius: 18px;
  padding: 18px;
}

.section { margin-bottom: 24px; }

.section-title {
  margin: 0 0 12px;
  padding-bottom: 10px;
  border-bottom: 1px solid var(--border);
  font-size: 13px;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: #cbd5e1;
}

.report-row {
  background: rgba(51, 65, 85, 0.45);
  border: 1px solid var(--border);
  border-radius: 14px;
  padding: 14px;
  margin-bottom: 10px;
}

.row-top { display: flex; gap: 10px; align-items: center; }

.review-checkbox {
  width: 15px;
  height: 15px;
  accent-color: var(--emerald);
  cursor: pointer;
}

.report-link {
  color: var(--text);
  text-decoration: none;
  font-weight: 700;
  font-size: 15px;
}

.report-link:hover {
  text-decoration: underline;
  text-decoration-color: var(--emerald);
  text-underline-offset: 4px;
}

.takeaways {
  margin: 8px 0 0 25px;
  padding: 0;
  color: var(--muted);
  font-size: 13px;
  line-height: 1.45;
}

.takeaways li { margin: 3px 0; }

@media (max-width: 560px) {
  .dashboard { padding: 16px; }
  .header h1 { font-size: 32px; }
}
</style>
</head>
<body>
<div class="dashboard">
<header class="header">
<h1>Research Queue</h1>
<p>Personal investment memo tracker and institutional research archive.</p>
</header>
<aside class="sidebar-queue">
"""

HTML_TEMPLATE_END = """
</aside>
</div>
<script>
document.addEventListener("DOMContentLoaded", function () {
  const checkboxes = document.querySelectorAll(".review-checkbox");

  checkboxes.forEach(function (checkbox) {
    const id = checkbox.dataset.id;
    const key = "reviewed-" + id;

    checkbox.checked = localStorage.getItem(key) === "true";

    checkbox.addEventListener("change", function () {
      localStorage.setItem(key, checkbox.checked);
    });
  });
});
</script>
</body>
</html>
"""

# =========================================================================
# CORE SCANNING LOGIC
# =========================================================================
def generate_slug(filename):
    """Generates a clean tracking ID for localStorage checkboxes."""
    slug = filename.lower()
    slug = re.sub(r'[^a-z0-True-9\s-]', '', slug)
    return re.sub(r'[\s_]+', '-', slug).strip('-')

def get_custom_takeaways(file_path):
    """Checks for an adjacent .txt file containing 3 custom bullets."""
    txt_path = os.path.splitext(file_path)[0] + ".txt"
    if os.path.exists(txt_path):
        try:
            with open(txt_path, "r", encoding="utf-8") as f:
                lines = [line.strip().lstrip("-*•").strip() for line in f if line.strip()]
                if len(lines) >= 3:
                    return lines[:3]
        except Exception:
            pass
    return DEFAULT_TAKEAWAYS

def build_dashboard():
    print("🔄 Initializing dynamic directory scan...")
    content_html = ""
    
    # Process categories based on preset structural order
    for folder_name, display_title in SECTOR_MAPPING.items():
        folder_path = os.path.join(ROOT_DIR, folder_name)
        
        if not os.path.exists(folder_path):
            continue
            
        # Scan for HTML and PDF assets
        files = [f for f in os.listdir(folder_path) if f.endswith(('.html', '.pdf'))]
        if not files:
            continue
            
        # Sort files so newest files display cleanly
        files.sort(reverse=True)
        
        print(f"📂 Found sector: {display_title} ({len(files)} items)")
        
        content_html += f'\n<section class="section">\n<h2 class="section-title">{display_title}</h2>\n'
        
        for file in files:
            full_file_path = os.path.join(folder_path, file)
            relative_url_path = f"{folder_name}/{file}"
            tracking_id = generate_slug(file)
            bullets = get_custom_takeaways(full_file_path)
            
            content_html += f'\n'
            content_html += f'<article class="report-row">\n<div class="row-top">\n'
            content_html += f'<input class="review-checkbox" data-id="{tracking_id}" type="checkbox"/>\n'
            content_html += f'<a class="report-link" href="{relative_url_path}" target="_blank">\n'
            content_html += f'        {file}\n'
            content_html += f'      </a>\n</div>\n<ul class="takeaways">\n'
            
            for bullet in bullets:
                content_html += f'<li>{bullet}</li>\n'
                
            content_html += f'</ul>\n</article>\n'
            
        content_html += f'</section>\n'
        
    # Write full output
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(HTML_TEMPLATE_START + content_html + HTML_TEMPLATE_END)
        
    print("✨ Execution complete. 'index.html' has been completely regenerated.")

if __name__ == "__main__":
    build_dashboard()