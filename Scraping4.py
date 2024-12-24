import requests
from bs4 import BeautifulSoup
import re
from googlesearch import search

# Function to fetch search results from Google
def get_search_results(keyword, num_results=10):
    """
    Fetch a list of website URLs related to the given keyword using Google search.
    """
    print(f"Searching for websites related to: {keyword}")
    urls = []
    try:
        # Use googlesearch to get URLs from Google
        results = search(keyword, num_results=num_results, lang="en")
        for url in results:
            urls.append(url)
    except Exception as e:
        print(f"Error during search: {e}")
    return urls

# Function to fetch emails from a website
def fetch_emails_from_url(url):
    """
    Fetch email addresses from a given website URL, filtering out invalid formats.
    """
    print(f"Scraping website: {url}")
    emails = set()
    try:
        # Send a GET request to the URL
        response = requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()

        # Parse HTML content
        soup = BeautifulSoup(response.text, "html.parser")

        # Find all email addresses using a refined regex
        raw_emails = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', response.text)

        # Filter out invalid email formats (like image URLs)
        for email in raw_emails:
            # Validating email to exclude those that look like image URLs
            if re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
                # Remove emails ending with image extensions like .jpg, .png, .jpeg
                if not (email.endswith('.jpg') or email.endswith('.png') or email.endswith('.jpeg')):
                    emails.add(email)

        # Check for "Contact Us" or similar links and scrape further
        contact_links = [a['href'] for a in soup.find_all('a', href=True) if 'contact' in a['href'].lower()]
        for link in contact_links:
            contact_url = link if link.startswith('http') else f"{url.rstrip('/')}/{link.lstrip('/')}"
            try:
                contact_response = requests.get(contact_url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
                contact_response.raise_for_status()
                contact_emails = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', contact_response.text)
                for email in contact_emails:
                    if re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
                        # Remove emails ending with image extensions like .jpg, .png, .jpeg
                        if not (email.endswith('.jpg') or email.endswith('.png') or email.endswith('.jpeg')):
                            emails.add(email)
            except Exception as e:
                print(f"Error accessing contact page {contact_url}: {e}")
    except Exception as e:
        print(f"Error scraping {url}: {e}")
    return emails

def main():
    """
    Main function to search for websites and scrape email addresses.
    """
    keyword = input("Enter a keyword: ").strip()
    num_results = int(input("Enter the number of websites to scrape (max 10): "))
    
    # Step 1: Search for related websites
    websites = get_search_results(keyword, num_results)
    if not websites:
        print("No websites found. Exiting.")
        return

    print(f"\nFound websites: {websites}")
    
    # Step 2: Scrape each website for emails
    all_emails = set()
    for website in websites:
        emails = fetch_emails_from_url(website)
        all_emails.update(emails)
    
    # Step 3: Display the results
    print("\nEmails found (after filtering out image-related ones):")
    if all_emails:
        for email in all_emails:
            print(email)
    else:
        print("No emails were found.")

if __name__ == "__main__":
    main()
