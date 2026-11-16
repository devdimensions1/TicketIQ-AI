"""Client-facing CLI demo: python demo.py"""
from ticketiq.engine import TriageEngine

SAMPLES = [
    "I was charged twice this month and I'm furious. Need a refund immediately!",
    "Would be great to have a dark mode. Thanks, love the product!",
    "The app crashes every time I open the dashboard. Production is down for all our users.",
    "How do I add a new team member to our workspace? No rush.",
]


def main():
    engine = TriageEngine()
    for i, text in enumerate(SAMPLES, 1):
        r = engine.triage(text)
        print(f"\n=== Ticket {i} ===\n{text}")
        print(f"Category : {r.category} ({r.category_confidence:.0%})")
        print(f"Priority : {r.priority}   Sentiment: {r.sentiment}   SLA: {r.sla}")
        print(f"Escalate : {'YES' if r.escalate else 'no'}")
        print(f"Reply    : {r.suggested_reply}")
        print("Similar  : " + " | ".join(f"#{s['id']} ({s['similarity']})" for s in r.similar_tickets))


if __name__ == "__main__":
    main()
