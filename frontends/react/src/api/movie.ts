import { queryOptions } from "@tanstack/react-query";
import apiFetch from "./apiFetch";
import { PaginatedResponse, Movie, MovieWithReviews } from "./types";

const BASE_URL = import.meta.env.VITE_BASE_BACKEND_URL;

type getMoviesResponse = {
  data: PaginatedResponse<Movie>;
  errors?: Array<{ message: string }>;
};

export function moviesOptions() {
  return queryOptions({
    queryKey: ["movies"],
    queryFn: fetchMovies,
    staleTime: 
  });
}

type fetchMoviesParams = {
  page?: number,
  sort?: "released_at" | "-released_at" | "title" | "-title",
  filter?: "year"[]
}

async function fetchMovies(page: number, sort?: fetchMoviesSort ,year?: number ): Promise<getMoviesResponse> {
  const params = new URLSearchParams({
    "page": page.toString(),
    ""
});
  const response = await apiFetch("movies/", {});
  return await response.json();
}

type getMovieResponse = {
  data: MovieWithReviews;
  errors?: Array<{ message: string }>;
};

export async function getMovie(movieId: number): Promise<getMovieResponse> {
  const response = await apiFetch(`${BASE_URL}movies/${movieId}/`);
  return await response.json();
}
