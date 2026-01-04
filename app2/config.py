"""
Configuration centralisée pour le projet CAN 2025 RAG
"""

# Chemins des fichiers
DATA_FOLDER = "../data/json"
FILES = {
    "matches": "matches.json",
    "teams": "equipes_qualifiees.json",
    "coaches": "coach.json",
    "squads": "joueurs_equipe.json",
    "stadiums": "stades.json",
    "standings": "classement_phase_groupe.json",
    "best_thirds": "classement_meilleurs_trois.json"
}

# Dictionnaire de référence pour les équipes
TEAM_ALIASES = {
    "Maroc": ["Maroc", "Morocco", "MAR", "Lions de l'Atlas", "Al Maghrib"],
    "Burkina Faso": ["Burkina Faso", "Burkina", "BFA", "Étalons"],
    "Cameroun": ["Cameroun", "Cameroon", "CMR", "Lions Indomptables"],
    "Algérie": ["Algérie", "Algeria", "ALG", "Fennecs"],
    "RD Congo": ["RD Congo", "RDC", "DR Congo", "Congo DR", "COD", "Léopards"],
    "Sénégal": ["Sénégal", "Senegal", "SEN", "Lions de la Teranga"],
    "Égypte": ["Égypte", "Egypt", "EGY", "Pharaons"],
    "Angola": ["Angola", "ANG", "Palancas Negras"],
    "Guinée équatoriale": ["Guinée équatoriale", "Equatorial Guinea", "GEQ", "EQG", "Nzalang Nacional"],
    "Côte d'Ivoire": ["Côte d'Ivoire", "Ivory Coast", "CIV", "Éléphants"],
    "Gabon": ["Gabon", "GAB", "Panthères"],
    "Ouganda": ["Ouganda", "Uganda", "UGA", "Cranes"],
    "Afrique du Sud": ["Afrique du Sud", "South Africa", "RSA", "Bafana Bafana"],
    "Tunisie": ["Tunisie", "Tunisia", "TUN", "Aigles de Carthage"],
    "Nigeria": ["Nigeria", "NGA", "Super Eagles"],
    "Mali": ["Mali", "MLI", "Aigles du Mali"],
    "Zambie": ["Zambie", "Zambia", "ZAM", "Chipolopolo"],
    "Zimbabwe": ["Zimbabwe", "ZIM", "Warriors"],
    "Comores": ["Comores", "Comoros", "COM", "Cœlacanthes"],
    "Soudan": ["Soudan", "Sudan", "SDN", "Faucons de Jediane"],
    "Bénin": ["Bénin", "Benin", "BEN", "Guépards"],
    "Tanzanie": ["Tanzanie", "Tanzania", "TAN", "Taifa Stars"],
    "Botswana": ["Botswana", "BOT", "Zebras"],
    "Mozambique": ["Mozambique", "MOZ", "Mambas"]
}

# Configuration des chunks
CHUNK_CONFIG = {
    "match": {
        "max_tokens": 2000,
        "overlap": 200
    },
    "team": {
        "max_tokens": 1500,
        "overlap": 100
    },
    "player": {
        "max_tokens": 500,
        "overlap": 50
    }
}