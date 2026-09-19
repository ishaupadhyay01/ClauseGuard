from typing import List, Dict, Any

SEED_RISK_PATTERNS: List[Dict[str, Any]] = [
    {
        "id": "1",
        "name": "Auto-Renewal Without Clear Opt-Out",
        "category": "Contract Term",
        "keywords": ["automatically renew", "auto-renew", "unless cancelled", "automatically renews"],
        "description": "Traps users into continued charges/obligations without an easy exit",
        "example_phrasing": "This Agreement shall automatically renew for successive one-year terms unless cancelled.",
        "risk_level": "high"
    },
    {
        "id": "2",
        "name": "Unilateral Term Changes",
        "category": "Contract Term",
        "keywords": ["may modify at any time", "sole discretion", "without notice", "modify these terms at any time"],
        "description": "Lets one party change the deal after signing",
        "example_phrasing": "Company reserves the right to modify any terms at any time in its sole discretion.",
        "risk_level": "high"
    },
    {
        "id": "3",
        "name": "Broad Liability Waiver",
        "category": "Liability",
        "keywords": ["waive all liability", "not responsible for any damages", "as-is", "as is"],
        "description": "Removes recourse even for the other party's negligence",
        "example_phrasing": "User agrees to waive all liability and accepts services strictly on an as-is basis.",
        "risk_level": "high"
    },
    {
        "id": "4",
        "name": "Mandatory Arbitration / No Right to Sue",
        "category": "Dispute Resolution",
        "keywords": ["binding arbitration", "waive right to a jury trial", "class action waiver", "jury trial"],
        "description": "Removes access to courts and collective legal action",
        "example_phrasing": "All disputes shall be settled by binding arbitration and user waives right to a jury trial.",
        "risk_level": "high"
    },
    {
        "id": "5",
        "name": "Vague Termination Conditions",
        "category": "Contract Term",
        "keywords": ["may terminate for any reason", "at will"],
        "description": "One-sided exit rights favoring the drafting party",
        "example_phrasing": "Company may terminate this agreement at will for any reason.",
        "risk_level": "medium"
    },
    {
        "id": "6",
        "name": "Excessive/Compounding Late Fees",
        "category": "Financial",
        "keywords": ["late fee", "compounding interest", "penalty of"],
        "description": "Can spiral small delays into large debts",
        "example_phrasing": "Late payments are subject to a 15% late fee and compounding interest.",
        "risk_level": "medium"
    },
    {
        "id": "7",
        "name": "Hidden Insurance Exclusions",
        "category": "Insurance",
        "keywords": ["does not cover", "excluded", "pre-existing condition", "pre existing condition"],
        "description": "Coverage looks comprehensive but has major carve-outs",
        "example_phrasing": "Policy does not cover pre-existing conditions or damages from excluded perils.",
        "risk_level": "high"
    },
    {
        "id": "8",
        "name": "Automatic Data Sharing / Broad Data Use",
        "category": "Privacy",
        "keywords": ["share with third parties", "affiliates", "for any purpose"],
        "description": "Personal data used beyond what's reasonably expected",
        "example_phrasing": "User data may be shared with third parties and affiliates for any purpose.",
        "risk_level": "medium"
    },
    {
        "id": "9",
        "name": "Non-Refundable Clauses",
        "category": "Financial",
        "keywords": ["non-refundable", "no refunds", "non refundable"],
        "description": "Removes standard consumer protection",
        "example_phrasing": "All fees paid under this agreement are strictly non-refundable.",
        "risk_level": "medium"
    },
    {
        "id": "10",
        "name": "Indemnification Shift",
        "category": "Liability",
        "keywords": ["indemnify and hold harmless", "defend at your own expense"],
        "description": "Shifts legal costs/risk onto the weaker party",
        "example_phrasing": "You agree to indemnify and hold harmless the Company and defend at your own expense.",
        "risk_level": "high"
    },
    {
        "id": "11",
        "name": "Rent/Fee Increase Without Cap",
        "category": "Financial",
        "keywords": ["may increase rent", "at landlord's discretion", "landlord's discretion"],
        "description": "Uncapped future cost exposure",
        "example_phrasing": "Landlord may increase rent at landlord's discretion upon 30 days notice.",
        "risk_level": "high"
    },
    {
        "id": "12",
        "name": "Security Deposit Forfeiture Conditions",
        "category": "Financial",
        "keywords": ["forfeit deposit", "non-refundable deposit", "forfeiture of deposit"],
        "description": "Vague conditions that make deposit recovery unlikely",
        "example_phrasing": "Tenant shall forfeit deposit if premises are not returned in original condition.",
        "risk_level": "medium"
    },
    {
        "id": "13",
        "name": "Confession of Judgment",
        "category": "Legal",
        "keywords": ["confess judgment", "waive right to defend"],
        "description": "Waives the right to contest a claim in court entirely",
        "example_phrasing": "Borrower agrees to confess judgment upon default and waives right to defend.",
        "risk_level": "high"
    },
    {
        "id": "14",
        "name": "Cross-Default Clauses",
        "category": "Financial",
        "keywords": ["default under any other agreement"],
        "description": "One missed payment elsewhere triggers this contract's default",
        "example_phrasing": "A default under any other agreement shall constitute a default hereunder.",
        "risk_level": "high"
    },
    {
        "id": "15",
        "name": "Excessive Personal Guarantee",
        "category": "Financial",
        "keywords": ["personally guarantee", "joint and several liability"],
        "description": "Extends business risk onto an individual's personal assets",
        "example_phrasing": "Signatory agrees to personally guarantee all liabilities with joint and several liability.",
        "risk_level": "high"
    }
]
