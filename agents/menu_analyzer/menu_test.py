import requests

url = "http://127.0.0.1:8000/analyze_menu"
data = {
    "menu_items": ["Pizza", "Pasta"]
}

response = requests.post(url, json=data)
print(response.json())
