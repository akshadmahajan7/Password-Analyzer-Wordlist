# src/strength_analyzer.py

from zxcvbn import zxcvbn
from typing import List, Dict, Any

def analyze_password(password: str, user_inputs: List[str]) -> Dict[str, Any]:
    """
    Analyzes the strength of a given password using zxcvbn,
    taking user-specific data into account to provide a more accurate score.

    Args:
        password: The password string to analyze.
        user_inputs: A list of strings (name, date, pet, etc.) that the 
                     user might use, which zxcvbn should check against.

    Returns:
        A dictionary containing the strength analysis results.
    """
    if not password:
        return {"error": "Password cannot be empty"}

    # zxcvbn calculates a score from 0 (worst) to 4 (best)
    results = zxcvbn(password, user_inputs=user_inputs)

    # Use .get() method to safely access keys and provide a default value 
    # to avoid the KeyError if the key is missing (e.g., for very weak passwords).
    analysis = {
        "password": password,
        "score": results.get('score', 0),
        "crack_time_display": results.get('crack_time_display', 'Instantly'), # FIXED: Use .get() here
        "warning": results.get('feedback', {}).get('warning', 'No warning'),
        "suggestions": results.get('feedback', {}).get('suggestions', []),
        "match_sequences": [
            {
                "pattern": match.get('pattern'),
                "i": match.get('i'),
                "j": match.get('j'),
                "sub": match.get('sub')
            }
            for match in results.get('sequence', [])
        ]
    }
    return analysis

if __name__ == "__main__":
    # --- Example Usage ---
    
    # User provides their name, pet's name, and a year
    known_data = ["johnsmith", "sparky", "1995"]
    
    # 1. A bad password based on known data
    bad_pass = "sparky1995!"
    print(f"--- Analyzing: {bad_pass} ---")
    bad_analysis = analyze_password(bad_pass, known_data)
    print(f"Score: {bad_analysis.get('score')}")
    print(f"Crack Time: {bad_analysis.get('crack_time_display')}")
    print(f"Warning: {bad_analysis.get('warning')}")
    print("-" * 20)

    # 2. A stronger password
    good_pass = "P@$$wOrdG00d_Key!"
    print(f"--- Analyzing: {good_pass} ---")
    good_analysis = analyze_password(good_pass, known_data)
    print(f"Score: {good_analysis.get('score')}")
    print(f"Crack Time: {good_analysis.get('crack_time_display')}")
    print(f"Warning: {good_analysis.get('warning')}")
    print("-" * 20)
