import os
from datetime import datetime

class ReportManager:
    def __init__(self, filename="PAKYARD_Execution_Report.html"):
        self.filename = filename
        self.steps = []
        self.start_time = datetime.now()

    def log_step(self, step_name, status="PASS", details="", screenshot=None):
        """Logs a test step with status and optional screenshot."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.steps.append({
            "name": step_name,
            "status": status,
            "details": details,
            "screenshot": screenshot,
            "timestamp": timestamp
        })
        print(f"[{status}] {step_name} - {details}")

    def generate_report(self):
        """Generates a styled HTML report."""
        end_time = datetime.now()
        duration = end_time - self.start_time
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>PAKYARD Test Report</title>
            <style>
                body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 20px; background-color: #f4f7f6; }}
                .header {{ background-color: #2c3e50; color: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; }}
                .summary {{ display: flex; gap: 20px; margin-bottom: 20px; }}
                .card {{ background: white; padding: 15px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); flex: 1; }}
                table {{ width: 100%; border-collapse: collapse; background: white; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
                th, td {{ padding: 12px 15px; text-align: left; border-bottom: 1px solid #ddd; }}
                th {{ background-color: #34495e; color: white; }}
                .status-PASS {{ color: #27ae60; font-weight: bold; }}
                .status-FAIL {{ color: #e74c3c; font-weight: bold; }}
                .status-INFO {{ color: #3498db; }}
                .screenshot {{ max-width: 200px; cursor: pointer; border: 1px solid #ddd; border-radius: 4px; }}
                .screenshot:hover {{ transform: scale(1.05); transition: 0.3s; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>PAKYARD Automation Execution Report</h1>
                <p>Generated on: {end_time.strftime("%Y-%m-%d %H:%M:%S")}</p>
            </div>
            <div class="summary">
                <div class="card"><strong>Start Time:</strong><br>{self.start_time.strftime("%H:%M:%S")}</div>
                <div class="card"><strong>Duration:</strong><br>{str(duration).split('.')[0]}</div>
                <div class="card"><strong>Total Steps:</strong><br>{len(self.steps)}</div>
            </div>
            <table>
                <thead>
                    <tr>
                        <th>Timestamp</th>
                        <th>Step Description</th>
                        <th>Status</th>
                        <th>Details</th>
                        <th>Screenshot</th>
                    </tr>
                </thead>
                <tbody>
        """
        
        for step in self.steps:
            screenshot_html = ""
            if step['screenshot']:
                screenshot_html = f'<a href="{step["screenshot"]}" target="_blank"><img src="{step["screenshot"]}" class="screenshot"></a>'
            
            html_content += f"""
                <tr>
                    <td>{step['timestamp']}</td>
                    <td>{step['name']}</td>
                    <td class="status-{step['status']}">{step['status']}</td>
                    <td>{step['details']}</td>
                    <td>{screenshot_html}</td>
                </tr>
            """

        html_content += """
                </tbody>
            </table>
        </body>
        </html>
        """
        
        with open(self.filename, "w", encoding="utf-8") as f:
            f.write(html_content)
        
        print(f"\nReport generated successfully: {os.path.abspath(self.filename)}")