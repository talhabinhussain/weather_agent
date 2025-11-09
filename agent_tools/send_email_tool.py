from ssl import OPENSSL_VERSION
from agents import function_tool
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os


# Load environment variables from .env file
load_dotenv(dotenv_path=".env.dev",override=True)

# Get credentials from environment (NOT hardcoded)
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))



if not SENDER_EMAIL or not SENDER_PASSWORD:
    raise ValueError("❌ Missing SENDER_EMAIL or SENDER_PASSWORD in .env file")


@function_tool
def send_weather_email(recipient_email: str, city: str, weather_data: str):
    """Send weather update via email"""
    print("Sending mail to",{recipient_email})
    try:
        # Create message
        message = MIMEMultipart()
        message["From"] = SENDER_EMAIL
        message["To"] = recipient_email
        message["Subject"] = f"Weather Update for {city}"

        # Email body
        body = f"""
        <html>
            <body style="font-family: Arial, sans-serif;">
                <h2>Weather Update for {city}</h2>
                <p>Here's your current weather update:</p>
                <div style="background-color: #f0f0f0; padding: 15px; border-radius: 5px;">
                    {weather_data}
                </div>
                <p style="color: #888; font-size: 12px; margin-top: 20px;">
                    This is an automated weather update email.
                </p>
            </body>
        </html>
        """

        message.attach(MIMEText(body, "html"))

        # Send email
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(message)

        return f"✓ Weather email sent successfully to {recipient_email}"

    except Exception as e:
        return f"✗ Error sending email: {str(e)}"
