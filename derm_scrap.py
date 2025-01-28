import requests
from bs4 import BeautifulSoup
import gradio as gr

def scrape_wikipedia_causes(disease_name):
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
        
        # Locate the "Causes" section
        causes_label = soup.find('th', text="Causes")
        if causes_label:
            causes_data = causes_label.find_next_sibling('td')
            if causes_data:
                causes_text = causes_data.get_text(separator=" ", strip=True)
                return f"Causes of {disease_name}:\n{causes_text}"
            else:
                return f"Causes section found, but no details available for '{disease_name}'."
        else:
            return f"Causes section not found for '{disease_name}'."
    elif response.status_code == 404:
        return f"Page not found for '{disease_name}'. Please check the spelling or try another term."
    else:
        return f"Failed to fetch data from Wikipedia (status code: {response.status_code})."

# Gradio Interface
def fetch_causes(disease_name):
    return scrape_wikipedia_causes(disease_name)

# Create Gradio app
interface = gr.Interface(
    fn=fetch_causes,
    inputs=gr.Textbox(label="Enter Disease Name", placeholder="e.g., Scabies"),
    outputs=gr.Textbox(label="Wikipedia Causes Information"),
    title="Wikipedia Causes Scraper",
    description="Enter a disease name to scrape the 'Causes' section from Wikipedia."
)

# Launch the app
interface.launch()
