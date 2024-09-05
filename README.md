# Smart-Order-Dispatcher

<figure>
        <img src="https://fieldedge.com/wp-content/uploads/2020/09/dispatching_board_magnified-600x328.png" alt ="Audio Art" style='width:800px;height:500px;'>
        <figcaption>
Automate the process of handling program orders from customers and forwarding them to specific employees using NLP techniques. 
a step-by-step guide with code to automate handling program orders from customer emails and sending them to specific employees using NLP. We'll use Python, spaCy for NLP, and smtplib for email automation. The code will cover the basic flow:
Step 1: Set Up Email Reading

We'll read emails using IMAP, extract the email content, and process it with NLP.
Step 2: Extract Order Information Using NLP

We'll use spaCy to identify and extract key entities from the email, such as product names, quantities, and dates.
Step 3: Classify and Forward Emails

Based on the extracted information, we'll determine which employee should receive the email and use smtplib to send it.
Prerequisites

Ensure you have the following Python packages installed:

```python
pip install spacy email smtplib imaplib python-dotenv
```
We'll also need a pre-trained spaCy model. Download it using:

```python
python -m spacy download en_core_web_sm
```
Explanation of the Code

    Email Fetching with IMAP:
        Connect to the IMAP server and log in using environment variables for security.
        Select the inbox and fetch emails. The code is set to process the latest email, but you can adjust it to process more.

    NLP Processing with spaCy:
        The email body is processed using spaCy to extract relevant entities (products, quantities, dates).
        This extraction is based on pre-trained entity recognition, which you may need to fine-tune or adjust based on your specific data.

    Decision Making:
        The determine_recipient function uses simple logic to decide which employee should receive the order. This should be customized based on your specific rules.

    Sending Emails:
        The send_email function composes an email using the extracted order details and sends it to the selected recipient using SMTP.

Environment Variables

For security, store email credentials and server details in a .env file:
```python
EMAIL_USER=your-email@example.com
EMAIL_PASS=your-email-password
IMAP_SERVER=imap.example.com
SMTP_SERVER=smtp.example.com
SMTP_PORT=587
```

