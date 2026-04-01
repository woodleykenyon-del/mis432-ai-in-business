# everycure.py
# A tiny EveryCure-style drug repurposing system
# Follows the AI Factory: Data -> Model -> Prediction -> Decision -> Value

# ── DATA ──────────────────────────────────────────────────────────────────────

# Each drug maps to the disease it currently treats
drug_indications = {
    "Metformin":    "Type 2 Diabetes",
    "Aspirin":      "Heart Disease",
    "Thalidomide":  "Multiple Myeloma",
    "Rapamycin":    "Organ Rejection",
    "Sildenafil":   "Pulmonary Hypertension",
    "Valproate":    "Epilepsy",
}

# Each drug maps to the biological targets it affects
drug_targets = {
    "Metformin":    {"AMPK", "mTOR", "IGF-1R"},
    "Aspirin":      {"COX-1", "COX-2", "NF-kB"},
    "Thalidomide":  {"TNF-alpha", "VEGF", "IL-6"},
    "Rapamycin":    {"mTOR", "PI3K", "IGF-1R"},
    "Sildenafil":   {"PDE5", "cGMP", "VEGF"},
    "Valproate":    {"HDAC", "GSK-3", "mTOR"},
}

# Each disease maps to the biological targets involved in it
disease_targets = {
    "Type 2 Diabetes":      {"AMPK", "mTOR", "IGF-1R"},
    "Heart Disease":        {"COX-1", "COX-2", "VEGF"},
    "Multiple Myeloma":     {"TNF-alpha", "VEGF", "IL-6"},
    "Organ Rejection":      {"mTOR", "PI3K"},
    "Pulmonary Hypertension": {"PDE5", "cGMP", "VEGF"},
    "Epilepsy":             {"HDAC", "GSK-3", "mTOR"},
    "Colorectal Cancer":    {"COX-2", "NF-kB", "VEGF"},
    "Alzheimer's Disease":  {"GSK-3", "mTOR", "HDAC"},
    "Aging":                {"mTOR", "AMPK", "IGF-1R"},
    "Breast Cancer":        {"IGF-1R", "mTOR", "PI3K"},
}

# ── MODEL (scoring rule) ───────────────────────────────────────────────────────
# Score = number of biological targets shared between drug and disease
# The more shared targets, the stronger the repurposing signal

def score_match(drug, disease):
    shared = drug_targets[drug] & disease_targets[disease]
    return shared, len(shared)


# ── PREDICTION + DECISION ─────────────────────────────────────────────────────

def find_repurposing_candidates(min_score=1):
    results = []

    for drug, current_disease in drug_indications.items():
        for candidate_disease in disease_targets:

            # Skip the disease the drug already treats
            if candidate_disease == current_disease:
                continue

            shared_targets, score = score_match(drug, candidate_disease)

            if score >= min_score:
                results.append({
                    "drug":             drug,
                    "current_use":      current_disease,
                    "candidate":        candidate_disease,
                    "shared_targets":   shared_targets,
                    "score":            score,
                })

    # Sort by score descending so best candidates surface first
    results.sort(key=lambda x: x["score"], reverse=True)
    return results


# ── VALUE (output) ─────────────────────────────────────────────────────────────

def print_results(results):
    print("=" * 60)
    print("  DRUG REPURPOSING CANDIDATES")
    print("  Ranked by number of shared biological targets")
    print("=" * 60)

    if not results:
        print("No candidates found.")
        return

    for r in results:
        targets_str = ", ".join(sorted(r["shared_targets"]))
        print(f"\nDrug:              {r['drug']}")
        print(f"Currently used for: {r['current_use']}")
        print(f"May be repurposed for: {r['candidate']}")
        print(f"Shared targets:    {targets_str}")
        print(f"Score:             {r['score']}")
        print(
            f"Explanation:       {r['drug']} may help treat {r['candidate']} "
            f"because both are connected to {targets_str}."
        )
        print("-" * 60)

    print(f"\nTotal candidates found: {len(results)}")


# ── MAIN ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    candidates = find_repurposing_candidates(min_score=1)
    print_results(candidates)
