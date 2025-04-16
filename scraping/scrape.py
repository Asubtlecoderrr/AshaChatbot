import requests
from bs4 import BeautifulSoup
import os

urls = [
    "https://oxfordhr.com/thought-leadership/womens-career-progression-pitfalls-and-how-to-avoid-them/",
    "https://www.weforum.org/publications/global-gender-gap-report-2023/digest/",
    "https://www.forbes.com/sites/forbeshumanresourcescouncil/2023/10/06/6-benefits-of-mentoring-in-the-2023-workplace/?sh=597c264820d7",
    "https://www.theguardian.com/world/2022/mar/06/caring-roles-block-career-advancement-for-three-in-five-women",
    "https://www.forbes.com/sites/forbesbusinesscouncil/2023/02/07/why-everyone-wins-with-more-women-in-leadership/?sh=5c8c068c3cdd",
    "https://www.gov.uk/government/collections/gender-equality-at-work-research-on-the-barriers-to-womens-progression",
    "https://www.mckinsey.com/featured-insights/diversity-and-inclusion/women-in-the-workplace",
    "https://www.gov.uk/government/publications/employment-pathways-and-occupational-change-after-childbirth",
    "https://www.gov.uk/government/publications/womens-progression-in-the-workplace",
    "https://www.gov.uk/government/publications/family-friendly-working-policies-and-practices-motivations-influences-and-impacts-for-employers",
    "https://www.bloomberg.com/news/newsletters/2023-04-25/women-ceos-at-big-companies-finally-outnumber-those-named-john?leadSource=uverify%20wall"
    
    
]



output_directory = "knowledgeBase"

def scrape_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        title = soup.title.string.strip() if soup.title else "default_title"
        content = soup.get_text()
        
        filename = os.path.join(output_directory, f"{title}.txt")
        with open(filename, "w", encoding="utf-8") as file:
            file.write(content)
        
        print(f"Scraped and saved: {url} -> {filename}")
    except Exception as e:
        print(f"Failed to scrape {url}: {e}")

for url in urls:
    scrape_url(url)