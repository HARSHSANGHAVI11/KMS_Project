# agents/incident_logger.py
from __future__ import annotations
import re
from datetime import datetime
from typing import Dict, List, Optional

def _clean(s: Optional[str]) -> str:
    return (s or "").strip()

def _first_match(text: str, patterns: List[str]) -> Optional[str]:
    for pat in patterns:
        m = re.search(pat, text, flags=re.IGNORECASE | re.DOTALL)
        if m:
            grp = m.group(1) if m.lastindex else m.group(0)
            return grp.strip()
    return None

def extract_incident_from_update(
    project: str,
    category: str,
    update_text: str,
    tags: Optional[List[str]] = None,
    author: Optional[str] = None,
) -> Dict:
    """
    Heuristic extraction of goal / incident / solution from a free-form update.
    Works well when the text uses keywords like 'Goal:', 'Issue:', 'Fix:' etc.
    Falls back to sensible defaults.
    """
    text = update_text.strip()

    goal = _first_match(text, [
        r"(?:^|\n)\s*(?:goal|objective|target)\s*[:\-]\s*(.+?)(?:\n[A-Z][a-z]+:|\Z)",
    ])
    incident = _first_match(text, [
        r"(?:^|\n)\s*(?:issue|incident|problem|bug)\s*[:\-]\s*(.+?)(?:\n[A-Z][a-z]+:|\Z)",
        r"(?:blocked by|failing because)\s*(.+?)(?:\.|\n|\Z)",
    ])
    solution = _first_match(text, [
        r"(?:^|\n)\s*(?:solution|fix|resolution|mitigation)\s*[:\-]\s*(.+?)(?:\n[A-Z][a-z]+:|\Z)",
        r"(?:we fixed|resolved|mitigated)\s*(.+?)(?:\.|\n|\Z)",
    ])
    impact = _first_match(text, [
        r"(?:^|\n)\s*(?:impact|effect)\s*[:\-]\s*(.+?)(?:\n[A-Z][a-z]+:|\Z)",
        r"(?:caused|resulted in)\s*(.+?)(?:\.|\n|\Z)",
    ])
    root_cause = _first_match(text, [
        r"(?:^|\n)\s*(?:root\s*cause|rca)\s*[:\-]\s*(.+?)(?:\n[A-Z][a-z]+:|\Z)",
        r"(?:because|due to)\s*(.+?)(?:\.|\n|\Z)",
    ])
    next_actions = _first_match(text, [
        r"(?:^|\n)\s*(?:next\s*steps|todo|actions?)\s*[:\-]\s*(.+?)(?:\n[A-Z][a-z]+:|\Z)",
    ])

    # Fallbacks
    if not goal and " to " in text[:180].lower():
        goal = _clean(text.split("\n")[0])
    if not incident:
        incident = _clean(text if len(text) < 240 else text[:240] + " …")
    if not solution:
        solution = "Documented for triage. Solution will be updated after RCA."

    record = {
        "id": f"{project.lower().replace(' ','-')}-{int(datetime.utcnow().timestamp())}",
        "timestamp": datetime.utcnow().isoformat(timespec="seconds"),
        "project": project,
        "category": category,
        "author": author,
        "goal": _clean(goal),
        "incident": _clean(incident),
        "root_cause": _clean(root_cause),
        "impact": _clean(impact),
        "solution": _clean(solution),
        "next_actions": _clean(next_actions),
        "raw_update": text,
        "tags": list({*(tags or []), *([category] if category else [])}),
        "status": "resolved" if solution and "will be updated" not in solution.lower() else "open",
        "version": 1,
    }
    return record
