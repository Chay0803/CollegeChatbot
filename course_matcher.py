"""
course_matcher.py
-----------------
Professional, data-driven course recommendation engine.
Integrates with FastAPI backend for the IFHE Admission Portal.
"""

from typing import Dict, List, Union


class CourseMatcher:
    """
    Handles recommendation logic for undergraduate courses
    based on user profile and preferences.
    """

    # Centralized course mapping for easy maintenance
    COURSE_MAP: Dict[str, Dict[str, List[str]]] = {
        "science": {
            "tech": [
                "B.Tech in Artificial Intelligence & Data Science",
                "B.Tech in Computer Science & Engineering",
                "B.Tech in Electronics & Communication Engineering",
                "B.Sc in Data Analytics",
                "BCA (Bachelor of Computer Applications)",
            ],
            "management": [
                "BBA",
                "BBA in AI & Data Science",
                "BBA in Cloud & Cyber Security",
            ],
            "general": [
                "B.Sc (Mathematics)",
                "B.Sc (Physics)",
                "B.Sc (Chemistry)",
            ],
        },
        "commerce": {
            "management": [
                "BBA",
                "BBA in Financial Analytics",
                "B.Com (Hons.)",
                "BBA in Cloud & Cyber Security",
            ],
            "law": ["BBA-LLB (Hons.)"],
            "general": [
                "B.Com (General)",
                "B.Com (Professional Accounting)",
            ],
        },
        "arts": {
            "law": ["BA-LLB (Hons.)"],
            "economics": ["BA in Economics"],
            "media": [
                "BA in Mass Communication",
                "BA in Psychology & Journalism",
            ],
            "general": ["BA (General)"],
        },
    }

    def __init__(self):
        self.min_percentage = 50  # baseline eligibility

    def is_eligible(self, english: str, tenth: float, twelfth: float) -> Union[bool, str]:
        """
        Eligibility validation based on language proficiency and academics.
        """
        if english.strip().lower() not in {"yes", "good", "fluent", "proficient"}:
            return "English proficiency is mandatory for admission."

        if tenth < self.min_percentage or twelfth < self.min_percentage:
            return (
                f"Minimum academic eligibility is {self.min_percentage}% "
                "in both 10th and 12th."
            )

        return True

    def match_courses(self, candidate: Dict[str, Union[str, float]]) -> Dict[str, Union[bool, str, List[str]]]:
        """
        Matches the user profile to possible courses.
        """

        stream = candidate.get("stream", "").strip().lower()
        interest = candidate.get("interest", "").strip().lower()
        english = candidate.get("english", "").strip().lower()
        tenth = float(candidate.get("tenth", 0))
        twelfth = float(candidate.get("twelfth", 0))

        # Step 1: Eligibility Check
        eligibility = self.is_eligible(english, tenth, twelfth)
        if eligibility is not True:
            return {
                "eligible": False,
                "message": eligibility,
                "recommendations": [],
            }

        # Step 2: Stream & Interest Match
        recommendations: List[str] = []
        stream_data = self.COURSE_MAP.get(stream)

        if stream_data:
            # Match by interest keyword
            matched = False
            for key, courses in stream_data.items():
                if key in interest:
                    recommendations.extend(courses)
                    matched = True
                    break
            # Fallback to general courses if no interest match
            if not matched:
                recommendations.extend(stream_data.get("general", []))
        else:
            # Handle unknown streams gracefully
            recommendations.extend([
                "BBA",
                "BCA (Bachelor of Computer Applications)",
                "BA (Economics)",
            ])

        return {
            "eligible": True,
            "message": "Courses matched successfully.",
            "recommendations": recommendations,
        }


# Example usage
if __name__ == "__main__":
    matcher = CourseMatcher()

    sample_candidate = {
        "stream": "Science",
        "interest": "Tech",
        "english": "Yes",
        "tenth": 85.0,
        "twelfth": 78.0,
    }

    result = matcher.match_courses(sample_candidate)
    print(result)
