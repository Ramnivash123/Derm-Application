import requests
from bs4 import BeautifulSoup
import gradio as gr

def scrape_aad(disease_name):
    # Construct the URL for the AAD scabies treatment page
    url = f"https://www.aad.org/public/diseases/a-z/nail-fungus-treatment"
    
    # Send GET request with headers to mimic a real browser request
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    # Send the request to get the page content
    response = requests.get(url, headers=headers)
    
    # Check if the page is successfully retrieved
    if response.status_code == 200:
        # Parse the content using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find the content section (here it seems like it's under 'div' with class 'section__content')
        content_section = soup.find('div', class_='section__content')
        
        if content_section:
            # Extract the content text
            paragraphs = content_section.find_all('p')
            content_text = "\n\n".join([paragraph.get_text(strip=True) for paragraph in paragraphs])
            return content_text
        else:
            return "Content section not found. The page structure might have changed."
    else:
        return f"Failed to retrieve the page. Status code: {response.status_code}, URL: {url}"

# Gradio Interface
iface = gr.Interface(
    fn=scrape_aad, 
    inputs="text", 
    outputs="text", 
    live=False,
    title="AAD Scabies Treatment Scraper",
    description="Enter a disease name (e.g., scabies) to scrape information from the AAD treatment page."
)

# Launch the Gradio app
iface.launch()
