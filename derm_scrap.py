import requests
from bs4 import BeautifulSoup

def scrape_mayo_clinic(disease_name):
    # Construct the Mayo Clinic URL based on the disease name
    disease_name_formatted = disease_name.lower().replace(' ', '-')
    url = f"https://www.mayoclinic.org/diseases-conditions/{disease_name_formatted}/diagnosis-treatment/drc-20352723"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    # Make the request to the Mayo Clinic website
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        return f"Failed to fetch data: {response.status_code}"
    
    # Parse the content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Example: Find the content section (adjust based on the actual website structure)
    content_section = soup.find('div', class_='content')  # You may need to inspect the page for the correct class
    if not content_section:
        return "Content section not found. Update the scraper."
    
    # Extract and return the treatment text
    treatment_text = content_section.get_text(strip=True)
    return treatment_text

# Input the disease name
disease_name = input("Vascular Tumors")
treatment_info = scrape_mayo_clinic(disease_name)

print("\nTreatment Information:")
print(treatment_info)
