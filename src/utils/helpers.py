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
        """Generates a professional PDF ticket."""
        c = canvas.Canvas(output_path, pagesize=letter)
        width, height = letter
        
        # Draw Border
        c.setStrokeColorRGB(0.2, 0.2, 0.2)
        c.rect(50, height - 350, width - 100, 300, stroke=1, fill=0)
        
        # Header
        c.setFont("Helvetica-Bold", 24)
        c.drawCentredString(width/2, height - 100, "MOVIE TICKET")
        
        c.setFont("Helvetica", 14)
        c.drawString(70, height - 150, f"Booking ID: #{booking_details['id']}")
        c.drawString(70, height - 180, f"Movie: {booking_details['movie_title']}")
        c.drawString(70, height - 210, f"Theater: {booking_details['theater_name']}")
        c.drawString(70, height - 240, f"Date & Time: {booking_details['show_time']}")
        c.drawString(70, height - 270, f"Tickets: {booking_details['total_tickets']}")
        c.drawString(70, height - 300, f"Total Price: ${booking_details['total_price']}")
        
        c.setFont("Helvetica-Oblique", 10)
        c.drawCentredString(width/2, height - 330, "Please present this ticket at the counter.")
        
        c.save()
        return output_path
