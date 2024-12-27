import os
import httpx

TMDB_KEY = os.environ.get("TMDB_API_KEY")
BASE_URL = "https://api.themoviedb.org/3/movie/top_rated"
PAGE_SIZE = 20

def main():
    client = httpx.Client(headers={'Authorization': f"Bearer {TMDB_KEY}"})

    def get_movies(nb: int = 200):
        movies = []
        for i in range(0, nb, PAGE_SIZE):
            r = client.get(BASE_URL, params={"page": i // PAGE_SIZE})
            movies.extend(r.json().get("results"))
        return movies
    
    def create_users(nb: int = 200):
        



if __name__ == "__main__":
    main()
