class LeadScoreCard:
    def __init__(self):
        # We start all scores at 0
        self.scores = {"Technical": 0, "Financial": 0, "Intent": 0}

    def evaluate_all(self, text):
        text = text.lower()

        # Technical Score (Ownership and House Type)
        if any(word in text for word in ["ja", "eigentümer", "besitzer", "haus", "gehört mir"]):
            self.scores["Technical"] = 10

        # Financial Score (Budget and Price)
        if any(word in text for word in ["euro", "budget", "bezahlen", "20.000", "günstig", "passt"]):
            self.scores["Financial"] = 10

        # Intent Score (Future Planning)
        if any(word in text for word in ["auto", "wärmepumpe", "pumpe", "laden", "strom", "planen"]):
            self.scores["Intent"] = 10