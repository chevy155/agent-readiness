# express-api

A Node.js REST API built with Express. Handles user authentication, product catalog,
and order management for a small e-commerce platform.

## Install

```bash
npm install
```

## Run

```bash
npm start
```

## Test

```bash
npm test
```

## Environment

Copy `.env.example` to `.env` and fill in your database credentials before running locally.

## CI

All pushes run the test suite via GitHub Actions. PRs require passing CI before merge.

## Project Structure

```
src/
  index.js        - Express app entry point
  routes/         - Route handlers
  middleware/     - Auth and validation middleware
tests/
  app.test.js     - Integration tests
```

Follows REST conventions. All routes return JSON. Auth via JWT middleware.
