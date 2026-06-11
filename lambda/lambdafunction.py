import json
import boto3
import urllib.request
import os
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('your_bucket_name')

API_KEY = os.environ['API_KEY']

cities = [
    "Kochi", "Mumbai", "Delhi", "Bangalore", "Chennai",
    "Hyderabad", "Pune", "Kolkata", "Ahmedabad", "Jaipur",
    "Lucknow", "Surat", "Kanpur", "Nagpur", "Indore",
    "Bhopal", "Patna", "Visakhapatnam", "Vadodara", "Ludhiana",
    "Agra", "Nashik", "Faridabad", "Meerut", "Rajkot",
    "Varanasi", "Srinagar", "Coimbatore", "Mysore", "Trivandrum"
]

def lambda_handler(event, context):

    results = []

    for city in cities:

        try:
            url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

            with urllib.request.urlopen(url) as response:
                data = json.loads(response.read().decode())

            item = {
                "city": city,
                "timestamp": datetime.utcnow().isoformat(),
                "temperature": str(data["main"]["temp"]),
                "humidity": str(data["main"]["humidity"]),
                "description": data["weather"][0]["description"]
            }

            table.put_item(Item=item)

            results.append(item)

        except Exception as e:
            print(f"Error processing {city}: {str(e)}")

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": f"{len(results)} cities processed",
            "records": results
        })
    }