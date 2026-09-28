import re

def compute_similarity(str1: str, str2: str) -> float:
    """Computes a normalized token overlap similarity between two strings."""
    tokens1 = set(re.findall(r'\w+', str1.lower()))
    tokens2 = set(re.findall(r'\w+', str2.lower()))
    
    if not tokens1 or not tokens2:
        return 0.0
        
    intersection = tokens1.intersection(tokens2)
    union = tokens1.union(tokens2)
    return len(intersection) / len(union)

def detect_duplicates(new_location: str, new_category: str, new_object: str, open_incidents: list) -> dict:
    """
    Evaluates new incident parameters against open incidents to identify potential duplicates.
    Combines location matching, category matching, and object keyword similarity.
    """
    highest_match = None
    max_score = 0.0

    new_loc_tokens = set(re.findall(r'\w+', new_location.lower()))
    new_obj_clean = new_object.lower()

    for inc in open_incidents:
        # Ignore already closed or resolved incidents
        if inc["status"] in ["Verified Resolved", "Closed"]:
            continue

        score = 0.0
        
        # 1. Location Matching (Highest weight: 50%)
        inc_loc_tokens = set(re.findall(r'\w+', inc["location"].lower()))
        loc_overlap = new_loc_tokens.intersection(inc_loc_tokens)
        if loc_overlap:
            score += 0.45 * (len(loc_overlap) / max(len(new_loc_tokens), len(inc_loc_tokens)))
            # Extra boost for exact room number match (e.g. '204')
            for token in new_loc_tokens:
                if token.isdigit() and token in inc_loc_tokens:
                    score += 0.15

        # 2. Category & Department Matching (Weight: 20%)
        if inc["category"].lower() == new_category.lower():
            score += 0.20

        # 3. Object & Defect Similarity (Weight: 30%)
        inc_obj_clean = (inc["title"] + " " + (inc["description"] or "")).lower()
        obj_sim = compute_similarity(new_obj_clean, inc_obj_clean)
        score += 0.30 * min(1.0, obj_sim * 1.5)

        if score > max_score:
            max_score = score
            highest_match = inc

    # Threshold for duplicate notification: 65% match confidence
    is_dup = max_score >= 0.65
    return {
        "is_duplicate": is_dup,
        "confidence": round(min(0.98, max_score), 2),
        "matched_incident": {
            "id": highest_match["id"],
            "title": highest_match["title"],
            "location": highest_match["location"],
            "status": highest_match["status"],
            "created_at": highest_match["created_at"],
            "upvotes": highest_match["upvotes"]
        } if is_dup and highest_match else None,
        "recommendation": "Upvote existing ticket to avoid administrative duplication" if is_dup else "Unique incident. Proceed with creation."
    }
