from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def create_faq_pdf(filename):
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter
    
    # Title
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, "TechFlow Solutions - Company FAQ")
    
    c.setFont("Helvetica", 12)
    y = height - 80
    
    faqs = [
        ("Q: What are the standard working hours?", 
         "A: TechFlow Solutions follows a flexible working arrangement. Our core hours are 10:00 AM to 4:00 PM local time. Employees are expected to complete 40 hours per week."),
        
        ("Q: How do I request vacation time?", 
         "A: Vacation requests should be submitted through the 'Pulse' HR portal at least two weeks in advance. Your direct manager must approve all requests."),
        
        ("Q: What is the company's remote work policy?", 
         "A: We operate on a 'Hybrid-First' model. Employees are encouraged to work from the office at least 2 days a week, typically Tuesday and Wednesday."),
        
        ("Q: Does the company provide a home office stipend?", 
         "A: Yes. All full-time employees are eligible for a one-time home office setup stipend of $500 after successfully completing their 3-month probation period."),
        
        ("Q: Who do I contact for IT support?", 
         "A: For technical issues, please email helpdesk@techflow.com or open a ticket on our Internal IT Slack channel #help-it."),
        
        ("Q: What is the health insurance coverage?", 
         "A: TechFlow offers comprehensive health, dental, and vision insurance through BlueStream Health. Coverage starts from the first day of employment."),
        
        ("Q: Are there any professional development benefits?", 
         "A: Yes! We offer an annual learning budget of $2,000 per employee for certifications, courses, and conferences related to your role."),
        
        ("Q: What is the dress code?", 
         "A: We maintain a 'Business Casual' dress code. On Fridays, we have 'Casual Fridays' where jeans and company branded t-shirts are welcome."),
    ]
    
    for q, a in faqs:
        if y < 100:
            c.showPage()
            y = height - 50
            c.setFont("Helvetica", 12)
            
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y, q)
        y -= 20
        c.setFont("Helvetica", 12)
        # Simple text wrapping logic
        words = a.split()
        line = ""
        for word in words:
            if len(line + word) < 80:
                line += word + " "
            else:
                c.drawString(70, y, line)
                y -= 15
                line = word + " "
        c.drawString(70, y, line)
        y -= 30

    c.save()

if __name__ == "__main__":
    create_faq_pdf("company_faq.pdf")
    print("company_faq.pdf created successfully.")
