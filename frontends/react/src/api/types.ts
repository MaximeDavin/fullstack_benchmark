export type PaginatedResponse<T> = {
  count: number;
  results: T[];
};

export type Movie = {
  id: number;
  title: string;
  year: number;
  description: string;
  released_at: string;
};

export type MovieWithReviews = Movie & {
  reviews: Review[];
};

export type Review = {
  id: number;
  user: string;
  rating: number;
  review: string;
  created_at: string;
};
