# BenchBoxd

## Overview

This repository contains implementations of a simplified Letterboxd-like app built using various combinations of backend and frontend technologies. The goal is to compare web development stacks based on ease of use, feature implementation, and developer experience for 
a simple use case.

## Product features

### User Management

* Register, login.
* User page with a list of movie reviews.

### Movie Management

* List movies.
* View movie details.

### Reviews and Ratings

* Add, edit, and delete reviews for movies.
* Add ratings (1–5 stars).

## Evaluation criteria

How easy is it to deal with:

* RESTfull api for a read-only model `movie`
* RESTfull api for a model with object-level permissions `review`
* Filtering, pagination, sorting
* Nested serialization: include a list of `review` in the detail view of a `movie`
* Avoid n+1 queries when querying multiple instances `review` in the detail view of a `movie`

## Out of scope

* Deployment in general
* Dealing with static files
* Real authentication system (email verification, account management, social login ...)

## Evaluation (WIP)

Stack | Ease of setup | Documentation and DX | Implementation difficulty | Performance |
|---|---|---|---|---|