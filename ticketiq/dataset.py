"""Synthetic support-ticket dataset generator.

Produces realistic labelled tickets (category, priority, sentiment) so the
models can be trained and demonstrated without any private customer data.
"""
from __future__ import annotations

import csv
import random
from pathlib import Path

CATEGORIES = {
    "billing": {
        "subjects": ["refund request", "double charged", "invoice missing", "payment failed", "wrong amount billed"],
        "bodies": [
            "I was charged twice for my subscription this month and need a refund.",
            "My invoice for last month never arrived, can you resend it?",
            "The payment on my credit card failed but the money left my account.",
            "I was billed the wrong amount after upgrading my plan.",
            "Please cancel my renewal and refund the annual charge.",
        ],
    },
    "technical": {
        "subjects": ["app crashes", "cannot log in", "error 500", "sync not working", "slow performance"],
        "bodies": [
            "The application crashes every time I open the dashboard.",
            "I cannot log in, it keeps saying my password is invalid.",
            "I get an error 500 whenever I try to export a report.",
            "Data sync between my phone and desktop has stopped working.",
            "The system is extremely slow and pages take a minute to load.",
        ],
    },
    "account": {
        "subjects": ["change email", "delete account", "add team member", "update profile", "reset 2FA"],
        "bodies": [
            "I would like to change the email address on my account.",
            "Please delete my account and all associated personal data.",
            "How do I add a new team member to our workspace?",
            "I need to update my company name and billing profile details.",
            "I lost my phone and need to reset two factor authentication.",
        ],
    },
    "feature_request": {
        "subjects": ["dark mode", "export to excel", "api access", "mobile app", "integration idea"],
        "bodies": [
            "It would be great if you added a dark mode option.",
            "Can you add an option to export data directly to Excel?",
            "We would love public API access to automate our workflows.",
            "Is a native mobile app on your roadmap?",
            "Please consider integrating with Slack for notifications.",
        ],
    },
}

URGENT = ["This is urgent!", "Production is down for all our users.", "We are losing money every minute.", "Need help immediately."]
CALM = ["No rush on this.", "Whenever you get a chance.", "Just a small question.", ""]
ANGRY = ["This is unacceptable.", "I am extremely frustrated with your service.", "Terrible experience, I'm furious."]
HAPPY = ["Thanks, I love the product!", "Great service so far, thank you.", "Really appreciate your help."]
NEUTRAL = ["Please advise.", "Let me know.", ""]


def generate(n: int = 1200, seed: int = 42) -> list[dict]:
    rng = random.Random(seed)
    rows = []
    for i in range(n):
        category = rng.choice(list(CATEGORIES))
        spec = CATEGORIES[category]
        mood = rng.choices(["urgent_angry", "calm_happy", "neutral"], weights=[3, 3, 4])[0]
        if mood == "urgent_angry":
            tail = f"{rng.choice(URGENT)} {rng.choice(ANGRY)}"
            priority = "high" if rng.random() < 0.9 else "medium"
            sentiment = "negative"
        elif mood == "calm_happy":
            tail = f"{rng.choice(CALM)} {rng.choice(HAPPY)}"
            priority = "low" if rng.random() < 0.85 else "medium"
            sentiment = "positive"
        else:
            tail = f"{rng.choice(NEUTRAL)}"
            priority = rng.choice(["medium", "medium", "low", "high"])
            sentiment = "neutral"
        text = f"{rng.choice(spec['subjects'])}. {rng.choice(spec['bodies'])} {tail}".strip()
        rows.append({"id": i + 1, "text": text, "category": category, "priority": priority, "sentiment": sentiment})
    return rows


def write_csv(path: str | Path, n: int = 1200, seed: int = 42) -> Path:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    rows = generate(n, seed)
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    return path


def load_csv(path: str | Path) -> list[dict]:
    with Path(path).open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


if __name__ == "__main__":
    print(f"Wrote {write_csv('data/tickets.csv')}")
