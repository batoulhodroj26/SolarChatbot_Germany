# engine/scoring.py

class LeadScoreCard:
    def __init__(self):
        # We track three main categories required by your project
        self.scores = {
            "Technical": 0,  # Roof, house type, shading
            "Financial": 0,  # Budget and price anchor
            "Intent": 0  # Urgency and extra tech (EV/Heat Pump)
        }

    def evaluate_technical(self, ownership, building_type):
        """Module 2: Technical Feasibility Scoring"""
        # Homeowners are the primary target in Germany
        if ownership == "owner":
            self.scores["Technical"] += 5

        # Single-family homes (Einfamilienhaus) are ideal
        if building_type == "einfamilienhaus":
            self.scores["Technical"] += 5

    def evaluate_financial(self, accepts_price_anchor):
        """Module 3: Financial Qualification Scoring"""
        # If they agree to the €18k-€25k range, they get full points
        if accepts_price_anchor:
            self.scores["Financial"] += 10

    def evaluate_intent(self, wants_ev, wants_heat_pump):
        """Module 4: Intent & Upsell Detection"""
        # Planning for an EV or Heat Pump shows high urgency
        if wants_ev:
            self.scores["Intent"] += 5
        if wants_heat_pump:
            self.scores["Intent"] += 5

    def get_total_score(self):
        # Calculate the grand total (out of 30)
        return sum(self.scores.values())