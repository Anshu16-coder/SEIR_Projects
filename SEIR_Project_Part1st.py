from urllib import response
import requests
import sys
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse


if len(sys.argv) > 1:
    url_from_command_line = sys.argv[1]
else:
    print("Usage: python get_url.py <url>")


def getting_title(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        if soup.title:
            return soup.title.string.strip() 
        else:
            return "Title tag not found"
            
    except requests.exceptions.RequestException as e:
        return f"Error fetching URL: {e}"
    except Exception as e:
        return f"An error occurred: {e}"


def getting_body(url):
    try:
       response = requests.get(url, timeout=10)
       response.raise_for_status() 
       soup = BeautifulSoup(response.content, 'html.parser')
       body_tag = soup.find('body')
       if body_tag:
            return body_tag.get_text(strip=True, separator=' ')
       else:
            return "No <body> tag found in the document."
    except requests.exceptions.RequestException as e:
        return f"An error occurred: {e}"



from urllib.parse import urljoin


def get_links(url):
    urls = set() 
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

    
        for anchor_tag in soup.find_all('a'):
            href = anchor_tag.get('href')
            if href:
                joined_url = urljoin(url, href)
                urls.add(joined_url)
                    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the URL: {e}")
        
    return urls

print("Page Title:", getting_title(url_from_command_line))
print("Page Body:", getting_body(url_from_command_line))
links = get_links(url_from_command_line)
for link in links:
    print("link:", link)