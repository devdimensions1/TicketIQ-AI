"""Template-driven reply suggestions, tone-adjusted by sentiment."""
from __future__ import annotations

OPENERS = {
    "negative": "We're truly sorry for the trouble this has caused, and we're prioritising it right away.",
    "neutral": "Thanks for reaching out to us.",
    "positive": "Thank you for the kind words and for contacting us!",
}

BODIES = {
    "billing": "Our billing team will review your account and confirm any refund or correction within 1-2 business days.",
    "technical": "Our engineers are investigating. Please share your browser/app version and any error message so we can resolve it faster.",
    "account": "We'll help update your account settings. For security, we may ask you to verify your identity first.",
    "feature_request": "We've logged your suggestion with our product team and will keep you posted on the roadmap.",
}

SLA = {"high": "within 1 hour", "medium": "within 8 hours", "low": "within 2 business days"}


def suggest_reply(category: str, priority: str, sentiment: str) -> str:
    return (f"{OPENERS[sentiment]} {BODIES[category]} "
            f"You can expect a follow-up {SLA[priority]}.")


def sla_for(priority: str) -> str:
    return SLA[priority]
