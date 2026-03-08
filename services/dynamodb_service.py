import boto3
import uuid
from datetime import datetime

dynamodb = boto3.resource("dynamodb", region_name="ap-south-1")

table = dynamodb.Table("career_advisory")


def save_result(profile, eligibility, careers, summary):
    for career in careers:
        if "feasibility_score" in career:
            career["feasibility_score"] = Decimal(str(career["feasibility_score"]))
    item = {
        "user_id": str(uuid.uuid4()),
        "timestamp": datetime.utcnow().isoformat(),
        "profile": profile,
        "eligibility": eligibility,
        "career_matches": careers,
        "summary": summary
    }

    table.put_item(Item=item)

    return item
