import { authenticatedFetch } from "./auth";
import { PaginatedResponse, Review } from "./types";

const BASE_URL = import.meta.env.VITE_BASE_BACKEND_URL;

type getReviewsResponse = {
  data: PaginatedResponse<Review>;
  errors?: Array<{ message: string }>;
};

export async function getReviews(): Promise<getReviewsResponse> {
  const response = await fetch(`${BASE_URL}reviews/`);
  return await response.json();
}

type getReviewResponse = {
  data: Review;
  errors?: Array<{ message: string }>;
};

export async function getReview(reviewId: number): Promise<getReviewResponse> {
  const response = await fetch(`${BASE_URL}reviews/${reviewId}/`);
  return await response.json();
}

type ReviewPayload = Omit<Review, "id">;

export async function postReview(
  review: ReviewPayload
): Promise<getReviewResponse> {
  const response = await authenticatedFetch(`${BASE_URL}reviews/`, {
    method: "POST",
    body: JSON.stringify(review),
  });
  return await response.json();
}

export async function patchReview(
  review: ReviewPayload
): Promise<getReviewResponse> {
  const response = await authenticatedFetch(`${BASE_URL}reviews/`, {
    method: "PATCH",
    body: JSON.stringify(review),
  });
  return await response.json();
}

export async function deleteReview(reviewId: number): Promise<null> {
  const response = await authenticatedFetch(`${BASE_URL}reviews/${reviewId}/`, {
    method: "DELETE",
  });
  return await response.json();
}
