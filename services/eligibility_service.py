import boto3
import json
REGION = "ap-south-1"

dynamodb = boto3.resource("dynamodb", region_name=REGION)
scheme_table = dynamodb.Table("schemes")


def fetch_schemes():
    response = scheme_table.scan()
    return response.get("Items", [])


def check_eligibility(profile: dict):

    schemes = fetch_schemes()

    eligible_schemes = []
    near_eligible_schemes = []
    all_results = []

    for scheme in schemes:

        eligible = True
        reasons = []

        state_required = scheme.get("state")
        user_state = profile.get("state")

        marks_required = int(scheme.get("min_marks", 0))
        user_marks = profile.get("marks")

        # STATE CHECK
        if state_required:

            if user_state is None:
                eligible = False
                reasons.append("State not provided")

            elif user_state != state_required:
                eligible = False
                reasons.append("State mismatch")

        # MARKS CHECK
        if user_marks is None:
            eligible = False
            reasons.append("Marks not provided")

        elif user_marks < marks_required:
            eligible = False
            reasons.append("Marks below requirement")

        if eligible:
            reasons = ["All criteria satisfied"]

        result = {
            "scheme": scheme["name"],
            "eligible": eligible,
            "reasons": reasons,
            "criteria_checked": {
                "state": {
                    "required": state_required,
                    "user": user_state,
                    "checked": state_required is not None,
                    "passed": None if state_required is None else user_state == state_required
                },
                "min_marks": {
                    "required": marks_required,
                    "user": user_marks,
                    "checked": True,
                    "passed": None if user_marks is None else user_marks >= marks_required
                }
            }
        }

        all_results.append(result)

        # ---- ELIGIBLE LIST ----
        if eligible:
            eligible_schemes.append(result)

        # ---- NEAR ELIGIBLE ----
        else:
            if user_marks and marks_required and abs(user_marks - marks_required) <= 5:
                near_eligible_schemes.append(result)

    return {
        "eligible_schemes": eligible_schemes[:5],
        "near_eligible_schemes": near_eligible_schemes[:3],
        "total_schemes_checked": len(all_results),
        "all_results": all_results
    }
