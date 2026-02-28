import bcrypt
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os

class SecurityUtils:
    @staticmethod
    def hash_password(password):
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

    @staticmethod
    def check_password(password, hashed_password):
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

class DocumentUtils:
    @staticmethod
    def generate_ticket_pdf(booking_details, output_path):
        """Generates a professional premium PDF ticket."""
        c = canvas.Canvas(output_path, pagesize=letter)
        width, height = letter
        
        # Draw Dark Background
        c.setFillColorRGB(0.1, 0.1, 0.1)
        c.rect(0, 0, width, height, stroke=0, fill=1)
        
        # Draw Ticket Card
        c.setFillColorRGB(0.15, 0.15, 0.15)
        c.setStrokeColorRGB(0.9, 0.03, 0.08) # Cinema Red
        c.rect(50, height - 400, width - 100, 350, stroke=1, fill=1)
        
        # Header Area
        c.setFillColorRGB(0.9, 0.03, 0.08)
        c.rect(50, height - 120, width - 100, 70, stroke=0, fill=1)
        
        c.setFillColorRGB(1, 1, 1)
        c.setFont("Helvetica-Bold", 32)
        c.drawCentredString(width/2, height - 100, "CINEMA PRO")
        
        # Movie Title
        c.setFont("Helvetica-Bold", 24)
        c.drawString(80, height - 170, str(booking_details['movie_title']).upper())
        
        # Details
        c.setFillColorRGB(0.7, 0.7, 0.7)
        c.setFont("Helvetica", 14)
        
        c.drawString(80, height - 210, "THEATER:")
        c.drawString(300, height - 210, "DATE & TIME:")
        
        c.setFillColorRGB(1, 1, 1)
        c.setFont("Helvetica-Bold", 14)
        c.drawString(80, height - 230, str(booking_details['theater_name']))
        c.drawString(300, height - 230, str(booking_details['show_time']))
        
        # More Details
        c.setFillColorRGB(0.7, 0.7, 0.7)
        c.setFont("Helvetica", 14)
        c.drawString(80, height - 270, "TICKETS:")
        c.drawString(300, height - 270, "TOTAL PAID:")
        
        c.setFillColorRGB(1, 1, 1)
        c.setFont("Helvetica-Bold", 14)
        c.drawString(80, height - 290, str(booking_details['total_tickets']))
        c.drawString(300, height - 290, f"${booking_details['total_price']}")
        
        # Fake Barcode
        c.setFillColorRGB(1, 1, 1)
        c.rect(80, height - 370, 200, 50, stroke=0, fill=1)
        c.setFillColorRGB(0, 0, 0)
        for i in range(85, 275, 4):
            c.rect(i, height - 365, 2 if i%3==0 else 1, 40, stroke=0, fill=1)
            
        c.setFillColorRGB(0.5, 0.5, 0.5)
        c.setFont("Helvetica-Oblique", 10)
        c.drawCentredString(width/2, height - 430, "Please present this digital ticket at the entrance.")
        
        c.save()
        return output_path
