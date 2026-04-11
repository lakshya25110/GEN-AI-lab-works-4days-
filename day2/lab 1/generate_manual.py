from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def create_manual_pdf(filename):
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter
    
    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, height - 100, "Nebula-7 Drone - User Manual")
    
    c.setFont("Helvetica", 12)
    text = [
        "Product Overview:",
        "The Nebula-7 is a high-performance cinematography drone with AI-assisted flight modes.",
        "",
        "Technical Specifications:",
        "- Flight Time: 45 minutes",
        "- Max Speed: 70 km/h",
        "- Camera: 8K Ultra HD with 3-axis Gimbal",
        "- Obstacle Avoidance: Omnidirectional (360 degrees)",
        "",
        "Safety Instructions:",
        "1. Do not fly near airports or restricted zones.",
        "2. Keep the drone within visual line of sight at all times.",
        "3. Check battery levels before every mission.",
        "",
        "Warranty Information:",
        "Nebula-7 comes with a 2-year manufacturer warranty covering electronic defects.",
        "Contact support@nebula.com for claims."
    ]
    
    y = height - 130
    for line in text:
        c.drawString(100, y, line)
        y -= 20
        
    c.save()

if __name__ == "__main__":
    create_manual_pdf("nebula_manual.pdf")
    print("nebula_manual.pdf created.")
