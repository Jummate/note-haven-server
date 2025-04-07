def generate_html_template(recipient_name, sender_name, reset_link=None):

     
    return f'''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Password Reset</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                color: #333;
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            .email-container {{
                width: 100%;
                max-width: 600px;
                margin: 0 auto;
                background-color: #f9f9f9;
                padding: 20px;
                border-radius: 8px;
                overflow: hidden; /* Prevent any overflow outside the container */
            }}
            .email-header {{
                background-color: #4CAF50;
                color: white;
                padding: 10px;
                text-align: center;
                border-radius: 8px 8px 0 0;
                word-wrap: break-word;
            }}
            .email-body {{
                margin: 20px 0;
                word-wrap: break-word;
            }}

            .cont-reset-link {{
                font-size: 24px;
                font-weight: bold;
                margin: 25px 0
                # color: #4CAF50;
            }}
           
            #reset-link{{
                border:none;
                background-color: #335cff;
                color:white;
                cursor:pointer;
                padding:1rem;
                border-radius: 0.75rem;
            }}

            .footer {{
                margin-top: 20px;
                font-size: 12px;
                color: #888;
                text-align: center;
                word-wrap: break-word;
            }}
            /* Ensure the body elements wrap content if too long */
            p {{
                word-wrap: break-word;
                overflow-wrap: break-word;
            }}
        </style>
    </head>
    <body>
        <div class="email-container">
            <div class="email-header">
                <h2>Password Reset</h2>
            </div>
            <div class="email-body">
                <p>Dear {recipient_name},</p>
                <p>We received a request to reset your password for your NoteHaven account. You can reset your password by clicking the link below:</p>
                <p class="cont-reset-link"><a href="{reset_link}" id="reset-link">Reset Password</a></p>
                <p>This link will expire in 30 minutes. If you didn’t request a password reset, you can safely ignore this email—your password will remain unchanged.</p>
            </div>
            <div>
                <p>If you need help, feel free to contact our support team.</p>
                <p>Best regards, </p>
                <p>The NoteHaven Team</p>
            </div>
            <div class="footer">
                <p>&copy; {sender_name}. All rights reserved.</p>
            </div>
        </div>
    </body>
    </html>
    '''

# Example usage:
# recipient_name = "John Doe"
# sender_name = "Your Company"
# verification_code = "123456"
# html_content = generate_html_template(recipient_name, sender_name, verification_code)

# # Print the generated HTML
# print(html_content)
