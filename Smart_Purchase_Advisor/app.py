from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Sample Product Data
products = [
    # Smartphones
    {"id": 1, "name": "iPhone 15 Pro", "category": "Smartphone", "price": 120000, "features": ["A17 Pro Chip", "Titanium Design", "48MP Main Camera"], "rating": 4.8},
    {"id": 2, "name": "Samsung S24 Ultra", "category": "Smartphone", "price": 115000, "features": ["AI Features", "S Pen", "200MP Camera"], "rating": 4.7},
    {"id": 3, "name": "Google Pixel 8 Pro", "category": "Smartphone", "price": 95000, "features": ["Best AI Camera", "Pure Android", "7 Years Updates"], "rating": 4.6},
    {"id": 4, "name": "OnePlus 12", "category": "Smartphone", "price": 65000, "features": ["Fast Charging", "Snapdragon 8 Gen 3", "Hasselblad Camera"], "rating": 4.5},
    {"id": 5, "name": "Redmi Note 13 Pro+", "category": "Smartphone", "price": 30000, "features": ["200MP Camera", "120W Charging", "Curved Display"], "rating": 4.3},
    
    # Laptops
    {"id": 6, "name": "MacBook Air M3", "category": "Laptop", "price": 110000, "features": ["Thin & Light", "M3 Chip", "18hr Battery"], "rating": 4.9},
    {"id": 7, "name": "Dell XPS 13", "category": "Laptop", "price": 140000, "features": ["InfinityEdge Display", "Premium Build", "Intel Core Ultra"], "rating": 4.7},
    {"id": 8, "name": "HP Spectre x360", "category": "Laptop", "price": 125000, "features": ["2-in-1 Design", "OLED Display", "Intel EVO"], "rating": 4.6},
    {"id": 9, "name": "ASUS Vivobook 16", "category": "Laptop", "price": 55000, "features": ["Large Display", "Ryzen 7", "Good Value"], "rating": 4.2},
    {"id": 10, "name": "Lenovo IdeaPad Slim 3", "category": "Laptop", "price": 40000, "features": ["Portability", "FHD Display", "Reliable Performance"], "rating": 4.0},
    
    # Headphones
    {"id": 11, "name": "Sony WH-1000XM5", "category": "Headphones", "price": 30000, "features": ["Best Noise Cancelling", "30hr Battery", "Touch Controls"], "rating": 4.9},
    {"id": 12, "name": "Bose QC Ultra", "category": "Headphones", "price": 35000, "features": ["Immersive Audio", "Comfortable Fit", "Excellent NC"], "rating": 4.8},
    {"id": 13, "name": "Sennheiser Momentum 4", "category": "Headphones", "price": 28000, "features": ["Superior Sound Quality", "60hr Battery", "Transparent Mode"], "rating": 4.7},
    {"id": 14, "name": "Boat Rockerz 450", "category": "Headphones", "price": 15000, "features": ["Affordable", "Long Playback", "Foldable"], "rating": 4.0},
    {"id": 15, "name": "JBL Tune 760NC", "category": "Headphones", "price": 6000, "features": ["Pure Bass Sound", "Active Noise Cancelling", "Lightweight"], "rating": 4.1},
]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/recommend', methods=['POST'])
def recommend():
    data = request.json
    category = data.get('category')
    budget = float(data.get('budget', 0))
    preferences = data.get('preferences', '').lower()
    
    # Simple recommendation logic
    filtered_products = [p for p in products if p['category'] == category and p['price'] <= budget]
    
    # Sort by rating (primary) and how many preferences match features (secondary)
    def score_product(p):
        pref_matches = sum(1 for feat in p['features'] if any(word in feat.lower() for word in preferences.split()))
        return (p['rating'] * 0.7) + (pref_matches * 0.3)
    
    filtered_products.sort(key=score_product, reverse=True)
    
    return jsonify(filtered_products[:5]) # Return top 5

if __name__ == '__main__':
    app.run(debug=True)
