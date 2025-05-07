import csv
import os

# List of the 60 most spoken languages in the world and their main countries
languages_countries = [
    ("Mandarin Chinese", "China"),
    ("Spanish", "Spain"),
    ("English", "United States"),
    ("Hindi", "India"),
    ("Arabic", "Egypt"),
    ("Bengali", "Bangladesh"),
    ("Portuguese", "Brazil"),
    ("Russian", "Russia"),
    ("Japanese", "Japan"),
    ("Punjabi", "Pakistan"),
    ("German", "Germany"),
    ("Javanese", "Indonesia"),
    ("Wu Chinese", "China"),
    ("Telugu", "India"),
    ("Vietnamese", "Vietnam"),
    ("Marathi", "India"),
    ("French", "France"),
    ("Korean", "South Korea"),
    ("Tamil", "India"),
    ("Italian", "Italy"),
    ("Turkish", "Turkey"),
    ("Urdu", "Pakistan"),
    ("Gujarati", "India"),
    ("Polish", "Poland"),
    ("Ukrainian", "Ukraine"),
    ("Persian", "Iran"),
    ("Xiang Chinese", "China"),
    ("Malayalam", "India"),
    ("Kannada", "India"),
    ("Sundanese", "Indonesia"),
    ("Hausa", "Nigeria"),
    ("Burmese", "Myanmar"),
    ("Hakka Chinese", "China"),
    ("Thai", "Thailand"),
    ("Dutch", "Netherlands"),
    ("Yoruba", "Nigeria"),
    ("Sindhi", "Pakistan"),
    ("Romanian", "Romania"),
    ("Bhojpuri", "India"),
    ("Tagalog", "Philippines"),
    ("Swahili", "Tanzania"),
    ("Azerbaijani", "Azerbaijan"),
    ("Malay", "Malaysia"),
    ("Nepali", "Nepal"),
    ("Amharic", "Ethiopia"),
    ("Greek", "Greece"),
    ("Gan Chinese", "China"),
    ("Hungarian", "Hungary"),
    ("Zulu", "South Africa"),
    ("Czech", "Czech Republic"),
    ("Igbo", "Nigeria"),
    ("Swedish", "Sweden"),
    ("Uzbek", "Uzbekistan"),
    ("Kazakh", "Kazakhstan"),
    ("Hebrew", "Israel"),
    ("Sinhala", "Sri Lanka"),
    ("Bulgarian", "Bulgaria"),
    ("Danish", "Denmark"),
    ("Finnish", "Finland"),
    ("Slovak", "Slovakia"),
    ("Norwegian", "Norway")
]

try:
    # Define the output file path
    output_file = os.path.join(os.getcwd(), "BookLanguage.csv")
    
    # Create CSV file
    with open(output_file, 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        # Write header row
        writer.writerow(['LanguageID', 'LanguageName', 'MainCountry'])
        
        # Write data rows
        for i, (language, country) in enumerate(languages_countries, 1):
            writer.writerow([i, language, country])
    
    print(f"CSV file created: {output_file}")
    
    # Display raw values for first 10 rows
    print("\nFirst 10 rows (raw values):")
    
    for i, (language, country) in enumerate(languages_countries[:10], 1):
        print(f"{i},{language},{country}")

except Exception as e:
    print(f"Error occurred: {e}")
