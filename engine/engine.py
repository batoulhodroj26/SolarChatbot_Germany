# engine/scoring.py

class LeadScoreCard:
    def __init__(self):
        # Initialize scores for different categories
        self.scores = {"Technical": 0, "Financial": 0, "Intent": 0}

    def evaluate_technical(self, ownership, building_type):
        """Scoring for Module 2: Technical Feasibility"""
        if ownership == "owner":
            self.scores["Technical"] += 5
        if building_type == "einfamilienhaus":
            self.scores["Technical"] += 5

    def evaluate_financial(self, accepted_range):
        """Scoring for Module 3: Financial Qualification"""
        if accepted_range:
            self.scores["Financial"] += 10

    def evaluate_intent(self, has_ev, has_heat_pump):
        """Scoring for Module 4: Intent Detection"""
        if has_ev:
            self.scores["Intent"] += 5
        if has_heat_pump:
            self.scores["Intent"] += 5