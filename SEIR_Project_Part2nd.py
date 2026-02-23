import sys
import requests
from bs4 import BeautifulSoup
from collections import Counter
import re

if len(sys.argv) != 3:
    print("Usage: python get_urls_sys.py <URL1> <URL2>")
    sys.exit(1)
url1 = sys.argv[1]
url2 = sys.argv[2]


def body(url):
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


body_text1= body(url1)
body_text2= body(url2)
   


def count_frequency(body_text):
    text = body_text.lower()
    words = re.findall(r'\b\w+\b', text)
    word_counts = Counter(words)

    return dict(word_counts)



def hashfun(s):
    n = len(s)
    p = 53
    m = 2**64
    hashvalue = 0
    pPow = 1
    for i in range(n):
        hashvalue = (hashvalue + (ord(s[i]) - ord('a') + 1) * pPow) % m
        pPow = (pPow * p) % m
    return hashvalue


    

def com_simhash(text):
    weights = count_frequency(text)
    v = [0] * 64  

    for word, weight in weights.items():
        hash_int = hashfun(word)
        for i in range(64):
            bit = (hash_int >> i) & 1
            if bit == 1:
                v[i] += weight
            else:
                v[i] -= weight


    fingerprint = [0] * 64
    for i in range(64):
        if v[i] > 0:
            fingerprint[i] = 1
        else:            
            fingerprint[i] = 0
            
    return fingerprint

simhash_url1 = com_simhash(body_text1)
simhash_url2 = com_simhash(body_text2)
print("SimHash URL1:", simhash_url1)
print("SimHash URL2:", simhash_url2)

countt=0
for i in range(64):
    if simhash_url1[i] == simhash_url2[i]:
        countt+=1
print("Number of bits same:", countt)