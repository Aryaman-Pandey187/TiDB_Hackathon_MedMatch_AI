import json
import smtplib
from email.message import EmailMessage
import boto3
import re

SECRET_NAME = ''  # Replace with your secret name
REGION = 'us-east-1'  # Replace with your region

def get_secrets(secret_name):
    client = boto3.client('secretsmanager', region_name=REGION)
    response = client.get_secret_value(SecretId=secret_name)
    return json.loads(response['SecretString'])

def lambda_handler(event, context):
    try:
        secrets = get_secrets(SECRET_NAME)
        email_from = secrets['EMAIL']
        email_password = secrets['PASSWORD']
        to_email = event['to_email']
        user_input = event['user_input']
        age_group = event['age_group']
        sex = event['sex']
        ranked_results = event['ranked_results']
        explanation = event['explanation']
        trials = event['trials']
        static_map_url = event.get('static_map_url', '')

        ranked_results_html = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', ranked_results)
        ranked_results_html = ranked_results_html.replace('\n', '<br>')

        ranked_results_html = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', ranked_results)
        ranked_results_html = ranked_results_html.replace('\n', '<br>')
        ranked_results_html = re.sub(r'^- (.*?)(<br>|$)', r'<li>\1</li>', ranked_results_html)
        ranked_results_html = f'<ul class="list-disc pl-6">{ranked_results_html}</ul>'

        explanation_html = explanation
        explanation_html = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', explanation_html) 
        explanation_html = explanation_html.replace('\n', '<br>')
        explanation_html = re.sub(r'(\d+\.\s)(.*?)(<br>|$)', r'<li>\1\2</li>', explanation_html)
        explanation_html = re.sub(r'(\d+-\d+%|>\d+%|\d+\.\d+)', r'<span class="text-blue-600">\1</span>', explanation_html)
        explanation_html = f'<ul class="list-decimal pl-6">{explanation_html}</ul>'

        html_body = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Clinical Trial Matches</title>
            <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
            <style>
                body {{
                    font-family: 'Roboto', 'Helvetica Neue', 'Arial', sans-serif;
                    background-color: #f0f4f8;
                    color: #333;
                }}
                .container {{
                    background-color: #ffffff;
                    border-radius: 10px;
                    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
                    overflow: hidden;
                }}
                .header {{
                    background: linear-gradient(90deg, #1e88e5, #4fc3f7);
                    color: white;
                    padding: 20px;
                    text-align: center;
                }}
                .header h1 {{
                    font-size: 28px;
                    font-weight: 700;
                    margin: 0;
                }}
                .section {{
                    padding: 20px;
                    border-bottom: 1px solid #e2e8f0;
                }}
                .table-row {{
                    animation: fadeIn 0.6s ease-in;
                }}
                @keyframes fadeIn {{
                    0% {{ opacity: 0; transform: translateY(10px); }}
                    100% {{ opacity: 1; transform: translateY(0); }}
                }}
                .table-row:hover {{
                    background-color: #e3f2fd;
                    transition: background-color 0.3s ease;
                }}
                table {{
                    border-collapse: collapse;
                    width: 100%;
                }}
                th, td {{
                    border: 1px solid #e2e8f0;
                    padding: 12px;
                    text-align: left;
                }}
                th {{
                    background-color: #1e88e5;
                    color: white;
                    font-weight: 600;
                }}
                img {{
                    max-width: 100%;
                    height: auto;
                    border-radius: 8px;
                }}
                .button {{
                    display: inline-block;
                    padding: 10px 20px;
                    background-color: #4fc3f7;
                    color: white;
                    text-decoration: none;
                    border-radius: 5px;
                    margin-top: 10px;
                    transition: background-color 0.3s ease;
                }}
                .button:hover {{
                    background-color: #039be5;
                }}
                .footer {{
                    background-color: #f8fafc;
                    padding: 15px;
                    text-align: center;
                    font-size: 14px;
                    color: #4a5568;
                }}
                ul {{
                    list-style-type: disc;
                    padding-left: 20px;
                }}
                .list-decimal {{
                    list-style-type: decimal;
                    padding-left: 20px;
                }}
                @media only screen and (max-width: 600px) {{
                    th, td {{
                        font-size: 13px;
                        padding: 8px;
                    }}
                    .section {{
                        padding: 15px;
                    }}
                    .header h1 {{
                        font-size: 22px;
                    }}
                }}
            </style>
        </head>
        <body class="bg-gray-100">
            <div class="max-w-4xl mx-auto my-8 container">
                <div class="header">
                    <h1>Clinical Trial Matches for '{user_input}' 🩺</h1>
                </div>
                <div class="section">
                    <p class="text-base text-gray-700 mb-4">
                        <strong class="text-blue-700">Age Group:</strong> {age_group} | <strong class="text-blue-700">Sex:</strong> {sex}
                    </p>
                </div>
                <div class="section">
                    <h2 class="text-xl font-semibold text-blue-800 mb-3">Ranked Trials</h2>
                    <p class="text-gray-600 mb-4">{ranked_results_html}</p>
                </div>
                <div class="section">
                    <h2 class="text-xl font-semibold text-blue-800 mb-3">Why These Match</h2>
                    <p class="text-gray-600 mb-4">{explanation_html}</p>
                </div>
                <div class="section">
                    <h2 class="text-xl font-semibold text-blue-800 mb-3">Trial Locations 📍</h2>
                    {"<img src='" + static_map_url + "' alt='Trial Location Map' class='shadow-sm mb-4'>" if static_map_url else "<p>No map available</p>"}
                    {"<a href='" + static_map_url + "' class='button'>View Map</a>" if static_map_url else "<p>Map unavailable</p>"}
                </div>
                <div class="section">
                    <h2 class="text-xl font-semibold text-blue-800 mb-3">Matches</h2>
                    <table class="min-w-full bg-white border border-gray-200">
                        <thead>
                            <tr>
                                <th class="py-3 px-4">Trial ID</th>
                                <th class="py-3 px-4">Title</th>
                                <th class="py-3 px-4">Conditions</th>
                                <th class="py-3 px-4">Summary</th>
                                <th class="py-3 px-4">Similarity</th>
                            </tr>
                        </thead>
                        <tbody>
        """
        for trial in trials:
            html_body += f"""
                            <tr class="table-row">
                                <td class="border-gray-200">{trial['nct_number']}</td>
                                <td class="border-gray-200">{trial['title']}</td>
                                <td class="border-gray-200">{trial['conditions']}</td>
                                <td class="border-gray-200">{trial['summary']}</td>
                                <td class="border-gray-200">{trial['distance']:.4f}</td>
                            </tr>
        """
        html_body += """
                        </tbody>
                    </table>
                </div>
                <div class="footer">
                    <p class="italic"><strong>Note:</strong> This is a demo, not medical advice. Consult a doctor.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        msg = EmailMessage()
        msg['Subject'] = 'Your Clinical Trial Matches Report'
        msg['From'] = email_from
        msg['To'] = to_email
        msg.set_content('View your trial matches...')
        msg.add_alternative(html_body, subtype='html')

        with smtplib.SMTP('smtp.gmail.com', 587, timeout=10) as smtp:
            smtp.starttls()
            smtp.login(email_from, email_password)
            smtp.send_message(msg)

        return {'statusCode': 200, 'body': 'Email sent'}
    except Exception as e:
        return {'statusCode': 500, 'body': str(e)}