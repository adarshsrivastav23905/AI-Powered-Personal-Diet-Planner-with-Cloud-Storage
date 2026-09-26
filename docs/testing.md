# Testing Strategy

## Automated Tests

The project includes automated backend tests in `tests/test_app.py` covering:

- health check
- registration
- duplicate registration
- valid login
- invalid login
- protected route access
- profile creation
- profile retrieval
- diet plan generation
- vegetarian and vegan plan generation
- goal-based plan generation
- authorization checks
- data isolation checks

## Run Tests

```bash
cd backend
python -m pytest ../tests/test_app.py -q
```

## Recommended Test Cases

- register new user
- reject duplicate email
- reject invalid login
- block unauthorized access
- update profile successfully
- generate diet plan with complete profile
- validate vegetarian diet behavior
- validate vegan diet behavior
- ensure plan belongs to the right user only
- check file upload and download restrictions

## Notes

This project focuses on real backend behavior and does not rely on mock-only assertions for user workflows.
