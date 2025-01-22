import requests
from bs4 import BeautifulSoup
import gradio as gr

def scrape_wikipedia(disease_name):
    # Format the disease name for the Wikipedia URL
    formatted_name = disease_name.replace(" ", "_")
    url = f"https://en.wikipedia.org/wiki/{formatted_name}"
    
    # Set custom headers to mimic a browser
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    # Send a GET request
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract the title of the page
        title = soup.find('h1', id='firstHeading').text.strip()
        
        # Extract the first paragraph under the main content
        paragraphs = soup.find('div', class_='mw-parser-output').find_all('p', recursive=False)
        content = "\n".join([p.text.strip() for p in paragraphs if p.text.strip()])
        
        return f"Title: {title}\n\nIntroduction:\n{content}"
    elif response.status_code == 404:
        return f"Page not found for '{disease_name}'. Please check the spelling or try another term."
    else:
        return f"Failed to fetch data from Wikipedia (status code: {response.status_code})."

# Gradio Interface
def fetch_info(disease_name):
    return scrape_wikipedia(disease_name)

# Create Gradio app
interface = gr.Interface(
    fn=fetch_info,
    inputs=gr.Textbox(label="Enter Disease Name", placeholder="e.g., Scabies"),
    outputs=gr.Textbox(label="Wikipedia Information"),
    title="Wikipedia Disease Scraper",
    description="Enter a disease name to scrape information from Wikipedia."
)

# Launch the app
interface.launch()
