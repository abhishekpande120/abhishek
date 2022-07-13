import requests
from bs4 import BeautifulSoup
import json
 
res = requests.get("https://stackoverflow.com/questions")

soup = BeautifulSoup(res.text, "html.parser")

questions_data = {
    "questions": []
}

questions = soup.select(".s-post-summary")

for q in questions:
    x = q.select_one('.s-link').getText()
    vote_count = q.select_one('.s-post-summary--stats-item-number').getText()
    views = q.select_one('.s-post-summary--stats-item:last-child').attrs['title']
    questions_data['questions'].append({
        "question": x,
        "vote_count": vote_count,
        "views": views
    })

json_data = json.dumps(questions_data)
print(json_data) 