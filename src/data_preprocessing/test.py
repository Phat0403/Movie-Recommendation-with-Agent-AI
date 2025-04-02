import requests

API_KEY = "YOUR_API_KEY"
query = "Dune"

url = f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={query}"
response = requests.get(url)
data = response.json()

if data["results"]:
    movie = data["results"][0]
    print(f"Title: {movie['title']}")
    print(f"Description: {movie['overview']}")
else:
    print("Không tìm thấy phim.")
