import requests
from bs4 import BeautifulSoup

# URL of the webpage you want to scrape
url = "https://www.practo.com/coimbatore/dermatologist"  # Replace with the actual URL of the page

# Send a GET request to the website
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the content of the page using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find all doctor listing containers
    doctor_listings = soup.find_all('div', {'data-qa-id': 'doctor_card'})
    
    # Loop through each listing and extract details
    for doctor in doctor_listings:
        # Extract doctor's name
        doctor_name = doctor.find('h2', {'data-qa-id': 'doctor_name'}).get_text(strip=True) if doctor.find('h2', {'data-qa-id': 'doctor_name'}) else 'N/A'
        
        # Extract practice location
        practice_location = doctor.find('span', {'data-qa-id': 'practice_locality'}).get_text(strip=True) if doctor.find('span', {'data-qa-id': 'practice_locality'}) else 'N/A'
        practice_city = doctor.find('span', {'data-qa-id': 'practice_city'}).get_text(strip=True) if doctor.find('span', {'data-qa-id': 'practice_city'}) else 'N/A'
        
        # Extract clinic name
        clinic_name = doctor.find('span', {'data-qa-id': 'doctor_clinic_name'}).get_text(strip=True) if doctor.find('span', {'data-qa-id': 'doctor_clinic_name'}) else 'N/A'
        
        # Print the extracted information
        print(f"Doctor Name: {doctor_name}")
        print(f"Practice Location: {practice_location}, {practice_city}")
        print(f"Clinic Name: {clinic_name}")
        print("-" * 40)
else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")
