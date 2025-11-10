# Weather Agent

This Weather agent is make to fetch real time weather updates and then send it to the user Gmail using the user's email address.

## Components of Agent

1. Agent is simply connected by the gemini llm model 2.5 flash.

2. Further Two Tools are use one Weather tool and other send email tool.

## Weather Tool

```python


# Define the weather fetching tool
@function_tool
def get_weather(city: str):
    # Print which city we're getting weather for
    print(f"Calling weather for: {city}")

    # Step 1: Build the API URL
    url = f"https://wttr.in/{city}?format=j1"

    # Step 2: Fetch the data from the API
    response = requests.get(url)

    # Step 3: Convert the JSON response to a Python dictionary
    parse_data = response.json()

    # Step 4: Extract the current weather (first item in the list)
    data = parse_data["current_condition"][0]

    # Step 5: Return the weather data
    return data


```

## Send Email Tool

```python
# STEP-BY-STEP BREAKDOWN OF send_weather_email() TOOL

@function_tool
def send_weather_email(recipient_email: str, city: str, weather_data: str):
    """Send weather update via email"""

    # ============================================
    # STEP 1: CREATE EMAIL MESSAGE OBJECT
    # ============================================
    try:
        # Create an empty email container (like an envelope)
        message = MIMEMultipart()
        # MIMEMultipart = allows us to add text, HTML, attachments, etc.

        # Add the "From" field (who is sending)
        message["From"] = SENDER_EMAIL
        # Example: message["From"] = "your_email@gmail.com"

        # Add the "To" field (who receives it)
        message["To"] = recipient_email
        # Example: message["To"] = "friend@gmail.com"

        # Add the "Subject" line
        message["Subject"] = f"Weather Update for {city}"
        # Example: message["Subject"] = "Weather Update for Karachi"


        # ============================================
        # STEP 2: CREATE EMAIL BODY (HTML FORMAT)
        # ============================================
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
        # This creates a nicely formatted HTML email with:
        # - Title showing the city name
        # - The weather data in a gray box
        # - Footer text

        # Example output:
        # ╔════════════════════════════════╗
        # ║  Weather Update for Karachi    ║
        # ║                                ║
        # ║  Here's your current weather:  ║
        # ║  ┌──────────────────────────┐  ║
        # ║  │ Temp: 28°C               │  ║
        # ║  │ Condition: Partly cloudy │  ║
        # ║  └──────────────────────────┘  ║
        # ╚════════════════════════════════╝


        # ============================================
        # STEP 3: ATTACH BODY TO MESSAGE
        # ============================================
        message.attach(MIMEText(body, "html"))
        # MIMEText(body, "html") converts the HTML string into email format
        # "html" means format as HTML (not plain text)


        # ============================================
        # STEP 4: CONNECT TO GMAIL SMTP SERVER
        # ============================================
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            # SMTP = Simple Mail Transfer Protocol (how emails are sent)
            # SMTP_SERVER = "smtp.gmail.com" (Gmail's email server)
            # SMTP_PORT = 587 (the port/channel to connect)

            # Example: Connect to Gmail on port 587
            # ┌─────────────────┐
            # │  Gmail Server   │
            # │  (SMTP)         │
            # │  Port: 587      │
            # └─────────────────┘


            # ============================================
            # STEP 5: START TLS ENCRYPTION
            # ============================================
            server.starttls()
            # TLS = Transport Layer Security (encrypts your password)
            # This secures the connection so your password isn't sent in plain text
            #
            # Without TLS: password sent as readable text ❌ UNSAFE
            # With TLS: password encrypted 🔒 SAFE


            # ============================================
            # STEP 6: LOGIN TO GMAIL
            # ============================================
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            # SENDER_EMAIL = "your_email@gmail.com"
            # SENDER_PASSWORD = "your_app_password" (16 characters)
            #
            # This logs into your Gmail account using SMTP


            # ============================================
            # STEP 7: SEND THE EMAIL
            # ============================================
            server.send_message(message)
            # Sends the complete email message through Gmail server
            # The email travels from your computer → Gmail server → recipient's inbox


        # ============================================
        # STEP 8: RETURN SUCCESS MESSAGE
        # ============================================
        return f"✓ Weather email sent successfully to {recipient_email}"
        # Example return: "✓ Weather email sent successfully to friend@gmail.com"


    # ============================================
    # ERROR HANDLING
    # ============================================
    except Exception as e:
        # If anything goes wrong (wrong password, no internet, etc.)
        # catch the error and return a friendly message
        return f"✗ Error sending email: {str(e)}"
        # Example: "✗ Error sending email: [Errno -2] Name or service not known"


# ============================================
# COMPLETE FLOW DIAGRAM
# ============================================
"""
USER INPUT:
"Send weather for Karachi to friend@gmail.com"
        ↓
AGENT processes request
        ↓
CALLS: send_weather_email(
    recipient_email="friend@gmail.com",
    city="Karachi",
    weather_data="Temp: 28°C, Condition: Sunny"
)
        ↓
[STEP 1] Create message container
        ↓
[STEP 2] Build HTML email body
        ↓
[STEP 3] Attach HTML to message
        ↓
[STEP 4] Connect to Gmail (smtp.gmail.com:587)
        ↓
[STEP 5] Encrypt connection with TLS
        ↓
[STEP 6] Login with your Gmail credentials
        ↓
[STEP 7] Send email through Gmail server
        ↓
[STEP 8] Return success message
        ↓
OUTPUT: "✓ Weather email sent successfully to friend@gmail.com"
"""

```
