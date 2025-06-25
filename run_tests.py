import json
import logging
import os
import glob
import smtplib
import asyncio
from browser_use import Agent
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from datetime import datetime
from jinja2 import Template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import argparse

from pyparsing import html_comment
parser = argparse.ArgumentParser()
parser.add_argument('--single-test', help='Run only a single test from file', action='store_true')
args = parser.parse_args()

load_dotenv()

smtp_server = os.getenv("SMTP_SERVER")
smtp_port = int(os.getenv("SMTP_PORT", "587"))
smtp_user = os.getenv("SMTP_USER")
smtp_password = os.getenv("SMTP_PASS")
sender_email = os.getenv("SENDER_EMAIL")
receiver_email = os.getenv("RECEIVER_EMAIL")

prompt = "Open https://swaglabs.in/ website, add red t-shirt to cart and check that t-shirt color should be red"

# Setup logging
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
log_filename = f"test_results_{timestamp}.log"
logging.basicConfig(
    filename=log_filename,
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)

# HTML report generator
def generate_html_report(results, output_file="report.html"):
    passed = len([r for r in results if r['status'] == 'PASSED'])
    failed = len(results) - passed

    template_str = """
    <html>
    <head>
      <title>Prompt Test Report</title>
      <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
      <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        h2 { color: #333; }
        table { border-collapse: collapse; width: 100%; margin-top: 20px; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        tr:nth-child(even) { background-color: #f9f9f9; }
        th { background-color: #4CAF50; color: white; }
        .passed { color: green; font-weight: bold; }
        .failed { color: red; font-weight: bold; }
      </style>
    </head>
    <body>
      <h2>🧪 Prompt Automation Test Report</h2>

      <div style="max-width: 300px; margin-bottom: 20px;">
  <canvas id="summaryChart" width="300" height="300"></canvas>
</div>
      <script>
        const ctx = document.getElementById('summaryChart');
        new Chart(ctx, {
          type: 'pie',
          data: {
            labels: ['Passed', 'Failed'],
            datasets: [{
              data: [{{ passed }}, {{ failed }}],
              backgroundColor: ['green', 'red']
            }]
          },
          options: { responsive: true }
        });
      </script>

      <table>
<tr><th>Test Name</th><th>Status</th><th>Assertion</th><th>Details</th></tr>
        {% for test in results %}
        <tr>
          <td>{{ test.name }}</td>
          <td class="{{ 'passed' if test.status == 'PASSED' else 'failed' }}">{{ test.status }}</td>
          <td>{{ test.assertion }}</td>
          <td>{{ test.result if test.status == 'PASSED' else test.error }}</td>
        </tr>
        {% endfor %}
      </table>
    </body>
    </html>
    """
    template = Template(template_str)
    html = template.render(results=results, passed=passed, failed=failed)
    with open(output_file, "w") as f:
        f.write(html)


async def run_test_case(name, prompt, assertion=None):
    try:
        logging.info(f"Running test: {name}")
        agent = Agent(
            task=prompt,
            llm=ChatGoogleGenerativeAI(model="gemini-2.0-flash-001"),
        )
        result = await agent.run()
         # Handle assertions
        assertion_result = "No assertion"
        if assertion:
            expected = assertion.get("expected")
            source = assertion.get("source", "result")
            actual = str(result) if source == "result" else ""
            if assertion.get("type") == "includes":
                assert expected in actual, f"Expected '{expected}' not found in result"
                assertion_result = f"'{expected}' found in result ✅"
        logging.info(f"Test Passed: {name}")
        return {"name": name, "status": "PASSED", "result": str(result),"assertion": assertion_result}
    except AssertionError as ae:
        logging.error(f"Assertion Failed: {name} - {ae}")
        return {
            "name": name,
            "status": "FAILED",
            "error": str(ae),
            "assertion": "❌ " + str(ae)
        }
    except Exception as e:
        logging.error(f"Test Failed: {name} - {e}")
        return {
            "name": name,
            "status": "FAILED",
            "error": str(e),
            "assertion": "❌ Test Execution error"
        }
   
    

async def main():
     # Delete old test report(s)
    for file in glob.glob("test_report_*.json"):
        try:
            os.remove(file)
            print(f"Deleted old report: {file}")
        except Exception as e:
            print(f"Could not delete {file}: {e}")

 # Load test cases
    if args.single_test:
        test_file = 'dynamic_test_cases.json'
        if not os.path.exists(test_file):
            print(f"⚠️ {test_file} not found.")
            return
        with open(test_file, 'r') as f:
            tests = json.load(f)
    else:
        test_file = 'test_cases.json'
        if not os.path.exists(test_file):
            print(f"⚠️ {test_file} not found.")
            return
        with open(test_file, 'r') as f:
            tests = json.load(f)

# Proceed to run tests in 'tests' list
    results = []
    for test in tests:
        result = await run_test_case(test['name'], test['prompt'], test.get('assertion'))
        results.append(result)

    # Save summary report
    report_filename = f"test_report_{timestamp}.json"
    with open(report_filename, "w") as f:
        json.dump(results, f, indent=4)

    print(f"\nAll tests completed. Summary saved to {report_filename} and logs in {log_filename}")

    # Save HTML report
    html_report_file = f"report_{timestamp}.html"
    generate_html_report(results, html_report_file)
    print(f"\n✅ All tests completed.")
    print(f"🌐 HTML Report: {html_report_file}")
    print(f"📝 Log File: {log_filename}")
    send_email_report(html_report_file,"Automation report", sender_email, receiver_email, smtp_server, smtp_port, smtp_user, smtp_password)
    print("Mail send")

   
   
def send_email_report(html_file, subject, sender_email, receiver_email, smtp_server, smtp_port, smtp_user, smtp_password):
    # Read the HTML content
    with open(html_file, "r") as f:
        html_content = f.read()

    # Create message container
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = receiver_email

    # Attach the HTML body
    msg.attach(MIMEText(html_content, 'html'))

    # Connect to SMTP server and send mail
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()  # Secure connection
        server.login(smtp_user, smtp_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())

    print(f"✅ Email sent to {receiver_email}")


asyncio.run(main())
