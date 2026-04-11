import csv
import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def create_pdf():
    try:
        c = canvas.Canvas("hr_policy.pdf", pagesize=letter)
        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, 750, "TechFlow Solutions - HR Policy (2026)")
        
        c.setFont("Helvetica", 12)
        text = [
            "1. Paid Time Off (PTO):",
            "Employees are entitled to 20 days of paid time off per year.",
            "PTO accrues at a rate of 1.66 days per month.",
            "",
            "2. Sick Leave:",
            "Up to 10 days of paid sick leave per year, no questions asked.",
            "",
            "3. Maternity & Paternity Leave:",
            "We offer 16 weeks of fully paid maternity leave and 8 weeks for paternity leave.",
            "",
            "4. Equipment Policy:",
            "If an assigned laptop breaks, please contact IT via Jira immediately.",
            "Do not attempt to repair company hardware yourself."
        ]
        
        y = 700
        for line in text:
            c.drawString(50, y, line)
            y -= 25
            
        c.save()
        print("Created hr_policy.pdf")
    except ImportError:
        print("reportlab not installed, skipping PDF creation.")

def create_csv():
    headers = ["Device_ID", "Type", "Brand", "Assigned_To", "Condition"]
    rows = [
        ["LP-909", "Laptop", "Dell XPS 15", "Jane Smith", "New"],
        ["LP-142", "Laptop", "MacBook Pro M3", "John Doe", "Good"],
        ["MO-231", "Monitor", "LG 27 inch 4K", "Jane Smith", "New"],
        ["PH-882", "Smartphone", "iPhone 15 Pro", "Sarah Connor", "Fair"],
        ["LP-776", "Laptop", "ThinkPad T14", "Alice Johnson", "Needs Repair"]
    ]
    
    with open("inventory.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)
    print("Created inventory.csv")

def create_txt():
    content = """TechFlow Solutions: Company History
    
TechFlow Solutions was founded in 2018 by Eleanor Vance and Marcus Thorne in a small garage in Austin, Texas. 
Initially focused on creating lightweight software for local logistics companies, the breakthrough came in 2021 with the release of 'FlowSync', an AI-powered supply chain management tool.
As of 2026, TechFlow has over 500 employees globally and recently opened an office in London. 
Our mission is to continually innovate by injecting AI into everyday business workflows.
"""
    with open("company_history.txt", "w") as f:
        f.write(content)
    print("Created company_history.txt")

if __name__ == "__main__":
    create_pdf()
    create_csv()
    create_txt()
    print("All mock data generated.")
