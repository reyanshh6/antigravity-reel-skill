import sys
import requests
from rembg import remove
from PIL import Image
from io import BytesIO
import os

def fetch_and_cutout(query, output_filename="asset.png"):
    print(f"🔍 Wikipedia par '{query}' ki photo dhoondh raha hu...")
    
    # 1. Wikipedia API se photo dhoondhna (100% Free)
    search_url = f"https://en.wikipedia.org/w/api.php?action=query&titles={query}&prop=pageimages&format=json&pithumbsize=1000"
    response = requests.get(search_url).json()
    
    pages = response.get('query', {}).get('pages', {})
    page = list(pages.values())[0]
    
    if 'thumbnail' not in page:
        print(f"❌ Error: '{query}' ki koi valid photo nahi mili.")
        return False
        
    img_url = page['thumbnail']['source']
    print(f"📥 Downloading: {img_url}")
    
    # 2. Image Download karna
    img_response = requests.get(img_url)
    input_image = Image.open(BytesIO(img_response.content))
    
    # 3. AI se Background Remove karna (Local, Zero-cost)
    print("✂️ AI magic chal raha hai... Background hataya ja raha hai...")
    output_image = remove(input_image)
    
    # 4. Transparent PNG save karna
    output_image.save(output_filename, format="PNG")
    print(f"✅ Success: Transparent image '{output_filename}' save ho gayi hai!")
    return True

if __name__ == "__main__":
    # Agent seedha terminal se leader ka naam bhejega
    search_query = sys.argv[1] if len(sys.argv) > 1 else "B. R. Ambedkar"
    out_file = sys.argv[2] if len(sys.argv) > 2 else "leader_cutout.png"
    
    fetch_and_cutout(search_query, out_file)
