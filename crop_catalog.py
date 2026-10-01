"""
Crop Catalog and Agronomic Intelligence Metadata for AgriPredict AI.
Provides rich agronomic insights, category classifications, and sample presets.
"""

CROP_DETAILS = {
    "rice": {
        "name": "Rice",
        "scientific_name": "Oryza sativa",
        "category": "Cereal Grain",
        "icon": "🌾",
        "water_req": "High (150-300 mm)",
        "climate": "Warm and humid tropical climate",
        "soil_type": "Clayey, alluvial soil with good water retention",
        "growing_period": "90 - 150 days",
        "description": "A staple food grain for over half the world's population, thriving in submerged conditions with high humidity and warmth."
    },
    "maize": {
        "name": "Maize (Corn)",
        "scientific_name": "Zea mays",
        "category": "Cereal Grain",
        "icon": "🌽",
        "water_req": "Moderate (60-100 mm)",
        "climate": "Warm temperate to tropical conditions",
        "soil_type": "Well-drained loamy to sandy-loam soil",
        "growing_period": "80 - 120 days",
        "description": "Versatile cereal crop used for human food, livestock feed, and industrial starch/biofuels."
    },
    "chickpea": {
        "name": "Chickpea (Gram)",
        "scientific_name": "Cicer arietinum",
        "category": "Pulse / Legume",
        "icon": "🧆",
        "water_req": "Low to Moderate (40-70 mm)",
        "climate": "Cool and dry climate, post-monsoon crop",
        "soil_type": "Deep well-drained sandy loam or clay loam",
        "growing_period": "90 - 120 days",
        "description": "High-protein legume crop that fixes atmospheric nitrogen into the soil, enriching soil fertility naturally."
    },
    "kidneybeans": {
        "name": "Kidney Beans (Rajma)",
        "scientific_name": "Phaseolus vulgaris",
        "category": "Pulse / Legume",
        "icon": "🫘",
        "water_req": "Moderate (60-120 mm)",
        "climate": "Mild temperate to sub-tropical climate",
        "soil_type": "Rich loamy soil with neutral to slightly acidic pH",
        "growing_period": "100 - 140 days",
        "description": "Nutrient-dense pulse rich in iron, dietary fiber, and plant-based protein."
    },
    "pigeonpeas": {
        "name": "Pigeon Peas (Arhar/Toor)",
        "scientific_name": "Cajanus cajan",
        "category": "Pulse / Legume",
        "icon": "🌱",
        "water_req": "Low to Moderate (60-90 mm)",
        "climate": "Warm tropical and semi-arid regions",
        "soil_type": "Deep loamy soils with good drainage",
        "growing_period": "140 - 200 days",
        "description": "Drought-resilient major legume grain across South Asia and Africa, essential for protein-rich diets."
    },
    "mothbeans": {
        "name": "Moth Beans",
        "scientific_name": "Vigna aconitifolia",
        "category": "Pulse / Legume",
        "icon": "🌿",
        "water_req": "Very Low (30-60 mm)",
        "climate": "Arid to semi-arid tropical climates",
        "soil_type": "Sandy, light textured marginal soils",
        "growing_period": "60 - 90 days",
        "description": "Extremely drought-tolerant legume often cultivated in desert or drought-prone agricultural belts."
    },
    "mungbean": {
        "name": "Mung Bean (Green Gram)",
        "scientific_name": "Vigna radiata",
        "category": "Pulse / Legume",
        "icon": "🫛",
        "water_req": "Low to Moderate (40-60 mm)",
        "climate": "Warm and moderately humid weather",
        "soil_type": "Fertile loamy soils with good internal drainage",
        "growing_period": "60 - 75 days",
        "description": "Fast-maturing short-duration legume suitable for catch-cropping and green manuring."
    },
    "blackgram": {
        "name": "Black Gram (Urad)",
        "scientific_name": "Vigna mungo",
        "category": "Pulse / Legume",
        "icon": "🪴",
        "water_req": "Moderate (60-80 mm)",
        "climate": "Warm, humid tropical climate",
        "soil_type": "Heavy clay loam to loamy soils",
        "growing_period": "70 - 90 days",
        "description": "Popular pulse rich in phosphoric acid and protein, cultivated across tropical river basins."
    },
    "lentil": {
        "name": "Lentil (Masoor)",
        "scientific_name": "Lens culinaris",
        "category": "Pulse / Legume",
        "icon": "🥣",
        "water_req": "Low (40-60 mm)",
        "climate": "Cool winter climate followed by warm harvest",
        "soil_type": "Light loamy to alluvial soils",
        "growing_period": "110 - 130 days",
        "description": "Ancient edible legume celebrated for dietary iron and high protein content in cool-season farming."
    },
    "pomegranate": {
        "name": "Pomegranate",
        "scientific_name": "Punica granatum",
        "category": "Fruit Orchard",
        "icon": "🍎",
        "water_req": "Low to Moderate (100-120 mm)",
        "climate": "Semi-arid tropical and subtropical climates",
        "soil_type": "Deep well-drained loamy or alluvial soils",
        "growing_period": "Perennial shrub / tree",
        "description": "High-value commercial fruit packed with powerful antioxidants and polyphenols."
    },
    "banana": {
        "name": "Banana",
        "scientific_name": "Musa acuminata",
        "category": "Fruit Plantation",
        "icon": "🍌",
        "water_req": "High (90-120 mm regular irrigation)",
        "climate": "Warm, humid tropical climate year-round",
        "soil_type": "Rich, well-drained loamy soil high in organic matter",
        "growing_period": "9 - 12 months",
        "description": "One of the most consumed fruits worldwide, requiring heavy nutrient replenishment particularly potassium."
    },
    "mango": {
        "name": "Mango",
        "scientific_name": "Mangifera indica",
        "category": "Fruit Orchard",
        "icon": "🥭",
        "water_req": "Moderate (90-110 mm)",
        "climate": "Tropical and subtropical with distinct dry season for flowering",
        "soil_type": "Deep, well-drained loamy to alluvial soils",
        "growing_period": "Perennial tree",
        "description": "The king of tropical fruits, celebrated for rich aroma, sweetness, and high commercial orchard value."
    },
    "grapes": {
        "name": "Grapes",
        "scientific_name": "Vitis vinifera",
        "category": "Horticulture / Viticulture",
        "icon": "🍇",
        "water_req": "Moderate (65-80 mm)",
        "climate": "Warm dry summer and mild winter",
        "soil_type": "Well-drained sandy loam or gravelly soil",
        "growing_period": "Perennial vine",
        "description": "Commercial horticulture crop used for fresh table grapes, raisins, and winery production."
    },
    "watermelon": {
        "name": "Watermelon",
        "scientific_name": "Citrullus lanatus",
        "category": "Fruit / Cucurbit",
        "icon": "🍉",
        "water_req": "Moderate (40-60 mm)",
        "climate": "Long, warm dry growing season with abundant sunshine",
        "soil_type": "Sandy or sandy-loam soils with good drainage",
        "growing_period": "75 - 95 days",
        "description": "Refreshing summer fruit with high water content, requiring sandy soil and high temperature."
    },
    "muskmelon": {
        "name": "Muskmelon (Cantaloupe)",
        "scientific_name": "Cucumis melo",
        "category": "Fruit / Cucurbit",
        "icon": "🍈",
        "water_req": "Moderate (20-30 mm during ripening)",
        "climate": "Warm, sunny, dry climate with low humidity",
        "soil_type": "Sandy loam, rich in organic matter",
        "growing_period": "80 - 100 days",
        "description": "Aromatic sweet melon flourishing under intense sunlight and moderate soil warmth."
    },
    "apple": {
        "name": "Apple",
        "scientific_name": "Malus domestica",
        "category": "Temperate Fruit Orchard",
        "icon": "🍏",
        "water_req": "Moderate to High (100-125 mm)",
        "climate": "Cool temperate climates with winter chilling hours",
        "soil_type": "Deep, well-drained loamy soil rich in humus",
        "growing_period": "Perennial tree",
        "description": "Prime temperate orchard fruit requiring cold winter chilling periods for flowering and fruit set."
    },
    "orange": {
        "name": "Orange (Citrus)",
        "scientific_name": "Citrus sinensis",
        "category": "Citrus Orchard",
        "icon": "🍊",
        "water_req": "Moderate (100-120 mm)",
        "climate": "Subtropical to tropical with sunny dry harvest",
        "soil_type": "Well-drained light loamy soils",
        "growing_period": "Perennial evergreen tree",
        "description": "World-famous citrus fruit rich in Vitamin C, flavonoids, and essential nutrients."
    },
    "papaya": {
        "name": "Papaya",
        "scientific_name": "Carica papaya",
        "category": "Tropical Fruit",
        "icon": "🫐",
        "water_req": "Moderate to High (140-250 mm)",
        "climate": "Warm, frost-free tropical climate",
        "soil_type": "Rich loamy soil with excellent drainage (intolerant of waterlogging)",
        "growing_period": "9 - 11 months",
        "description": "Fast-growing herbaceous tropical plant rich in papain enzymes and beta-carotene."
    },
    "coconut": {
        "name": "Coconut",
        "scientific_name": "Cocos nucifera",
        "category": "Plantation Crop",
        "icon": "🥥",
        "water_req": "High (130-220 mm)",
        "climate": "Warm, humid coastal tropical climate",
        "soil_type": "Coastal sandy soils or deep alluvial soils",
        "growing_period": "Perennial palm tree",
        "description": "The 'Tree of Life' yielding water, oil, coir, and copra across tropical island and coastal shorelines."
    },
    "cotton": {
        "name": "Cotton",
        "scientific_name": "Gossypium hirsutum",
        "category": "Commercial Fiber Crop",
        "icon": "☁️",
        "water_req": "Moderate (60-90 mm)",
        "climate": "Warm climate with abundant sunshine and frost-free days",
        "soil_type": "Deep black cotton soils (regur) with moisture retention",
        "growing_period": "150 - 180 days",
        "description": "The world's leading natural textile fiber, driving rural economies and industrial manufacturing."
    },
    "jute": {
        "name": "Jute (Golden Fiber)",
        "scientific_name": "Corchorus olitorius",
        "category": "Commercial Fiber Crop",
        "icon": "🌾",
        "water_req": "High (150-200 mm)",
        "climate": "Warm and highly humid monsoon climate",
        "soil_type": "New alluvial silty clay soil around flood plains",
        "growing_period": "120 - 150 days",
        "description": "Eco-friendly golden fiber used in biodegradable packaging, ropes, and geo-textiles."
    },
    "coffee": {
        "name": "Coffee",
        "scientific_name": "Coffea arabica",
        "category": "Commercial Plantation",
        "icon": "☕",
        "water_req": "High (150-200 mm)",
        "climate": "Cool, humid tropical highland climate with canopy shade",
        "soil_type": "Volcanic red loamy soil with rich humus",
        "growing_period": "Perennial shrub",
        "description": "Global beverage commodity thriving on shaded tropical mountain slopes with well-drained volcanic soil."
    }
}

# Presets representing typical soil and climate conditions for quick testing
SAMPLE_PRESETS = [
    {
        "label": "Rice (Submerged Delta)",
        "crop": "rice",
        "n": 90, "p": 42, "k": 43,
        "temperature": 20.87, "humidity": 82.0, "ph": 6.5, "rainfall": 202.93
    },
    {
        "label": "Coffee (Tropical Highland)",
        "crop": "coffee",
        "n": 104, "p": 18, "k": 30,
        "temperature": 23.6, "humidity": 60.4, "ph": 6.78, "rainfall": 160.0
    },
    {
        "label": "Cotton (Black Soil Plains)",
        "crop": "cotton",
        "n": 117, "p": 46, "k": 19,
        "temperature": 23.8, "humidity": 79.5, "ph": 6.9, "rainfall": 78.4
    },
    {
        "label": "Maize (Loamy Field)",
        "crop": "maize",
        "n": 71, "p": 54, "k": 20,
        "temperature": 22.6, "humidity": 65.1, "ph": 6.2, "rainfall": 70.8
    },
    {
        "label": "Apple (Temperate Valley)",
        "crop": "apple",
        "n": 20, "p": 134, "k": 199,
        "temperature": 22.1, "humidity": 92.3, "ph": 5.9, "rainfall": 112.5
    },
    {
        "label": "Chickpea (Semi-Arid Gram)",
        "crop": "chickpea",
        "n": 40, "p": 68, "k": 79,
        "temperature": 18.9, "humidity": 16.8, "ph": 7.3, "rainfall": 78.2
    }
]

def validate_parameters(n_str, p_str, k_str, temp_str, humidity_str, ph_str, rainfall_str):
    """
    Validate input parameters according to physical and agronomic boundary ranges.
    Returns (cleaned_dict, error_message).
    """
    fields = {
        "Nitrogen (N)": (n_str, 0.0, 200.0, "ppm / kg/ha"),
        "Phosphorus (P)": (p_str, 0.0, 200.0, "ppm / kg/ha"),
        "Potassium (K)": (k_str, 0.0, 300.0, "ppm / kg/ha"),
        "Temperature": (temp_str, -10.0, 60.0, "°C"),
        "Humidity": (humidity_str, 1.0, 100.0, "%"),
        "Soil pH": (ph_str, 0.0, 14.0, "pH units"),
        "Rainfall": (rainfall_str, 0.0, 600.0, "mm")
    }
    
    cleaned = {}
    for name, (raw_val, min_val, max_val, unit) in fields.items():
        if raw_val is None or str(raw_val).strip() == "":
            return None, f"Please provide a numerical value for {name}."
        
        try:
            val = float(raw_val)
        except (ValueError, TypeError):
            return None, f"Please enter a valid numerical value for {name}."
        
        if val < min_val or val > max_val:
            return None, f"{name} must be within realistic bounds ({min_val} to {max_val} {unit})."
        
        cleaned[name] = val
        
    return cleaned, None

def get_crop_metadata(crop_key):
    """Return enriched dictionary of metadata for a given crop name."""
    key = str(crop_key).strip().lower()
    if key in CROP_DETAILS:
        return CROP_DETAILS[key]
    
    # Fallback
    return {
        "name": key.capitalize(),
        "scientific_name": "Cultivated Crop",
        "category": "Agricultural Crop",
        "icon": "🌱",
        "water_req": "Standard agricultural irrigation",
        "climate": "Standard seasonal conditions",
        "soil_type": "Standard arable agricultural soil",
        "growing_period": "Variable by variety",
        "description": "Cultivated agricultural crop identified by model prediction."
    }
