import requests
from bs4 import BeautifulSoup
import os

# URL of the main research page
main_url = "https://fairygodboss.com/research"

# Set up headers to mimic a browser visit
headers = {
    "User-Agent": "Mozilla/5.0"
}

# Create a session
session = requests.Session()

# Fetch the main page
response = session.get(main_url, headers=headers)
soup = BeautifulSoup(response.content, "html.parser")

# Find all article links on the page
# Adjust the selector based on the actual HTML structure
article_links = []
for a_tag in soup.find_all("a", href=True):
    href = a_tag['href']
    if href.startswith("/research/"):
        full_url = f"https://fairygodboss.com{href}"
        if full_url not in article_links:
            article_links.append(full_url)

print(f"Found {len(article_links)} article links.")

# Visit each article and save its content
for idx, article_url in enumerate(article_links, start=1):
    print(f"Processing article {idx}: {article_url}")
    article_response = session.get(article_url, headers=headers)
    article_soup = BeautifulSoup(article_response.content, "html.parser")

    # Extract the article title
    title_tag = article_soup.find("h1")
    title = title_tag.get_text(strip=True) if title_tag else f"article_{idx}"

    # Extract the article content
    content_div = article_soup.find("div", class_="article-content")  # Adjust class name as needed
    if content_div:
        paragraphs = content_div.find_all("p")
        content = "\n".join(p.get_text(strip=True) for p in paragraphs)
    else:
        content = "Content not found."

    # Save the content to a text file
    filename = f"../knowledgeBase/{title.replace(' ', '_')}.txt"
    with open(filename, "w", encoding="utf-8") as file:
        file.write(f"{title}\n\n{content}")

    print(f"Saved article to {filename}")
