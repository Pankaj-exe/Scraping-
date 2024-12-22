import requests # this is an external module. you have to download it.< in terminals :- pip install requests> for imprt in python code.
from bs4 import BeautifulSoup #same for this < in terminals :-  pip install beautifulsoup4 (depends on the latest version)>. for import it in code 
import re  # The re module in Python stands for regular expressions. It provides tools for working with patterns in text, such as searching, matching, or replacing specific patterns. No need to download externally it's an inbult library

# Start with the homepage don't paste contact us link just paste homepage and the code figure out it self.
# homepage_url = "https://sukhis.com/"
homepage_url = "https://www.indusind.com/in/en/personal.html"
# homepage_url = "https://minionsenterprises.com/"
# homepage_url = "https://pearlbellventures.com"
# homepage_url = "https://www.amazon.in/"


# Fetch the homepage content
response = requests.get(homepage_url)
soup = BeautifulSoup(response.text, 'html.parser')

# Look for links containing the word 'contact'
contact_link = None
for link in soup.find_all('a', href=True): # 'a'for <a> tag where we store the contact us  page link
    if 'contact' in link.text.lower() or 'contact' in link['href'].lower():
        contact_link = link['href']
        break

# Check if we found a contact link
if contact_link:
    # Handle relative URLs
    if not contact_link.startswith("http"):
        contact_link = requests.compat.urljoin(homepage_url, contact_link)
    
    print(f"Contact page URL: {contact_link}")

    # Fetch the contact page content
    contact_response = requests.get(contact_link) #requesting the website to fetch the data for the source code.
    contact_soup = BeautifulSoup(contact_response.text, 'html.parser') # converting & filtering the source.

    # Extract email addresses
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}' # mail verification.
    emails = re.findall(email_pattern, contact_soup.get_text()) 

    if emails:
        print("Emails found:")
        for email in emails:
            print(email)
    else:
        print("No emails found.")
else:
    print("No contact page link found.")
