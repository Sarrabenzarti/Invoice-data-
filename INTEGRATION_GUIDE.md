# Steps to integrate API-based backend/frontend separation (like dentalsync-ai)

1. **Backend (Flask API)**
   - Implement endpoints in `app.py` for each ML task (e.g., `/api/segmentation`, `/api/detection`).
   - Each endpoint receives POST requests, runs the model, and returns results as JSON.
   - Use CORS to allow frontend access.

2. **Frontend**
   - (To be added) Build a UI (React, Next.js, or other) that sends requests to the backend API endpoints.
   - Use fetch/axios to POST data (images, JSON) to `/api/segmentation` or `/api/detection`.
   - Display results from the backend.

3. **Separation**
   - Run backend (Flask) and frontend (React/Next.js) as separate services.
   - Communicate only via HTTP API.

4. **Environment Variables**
   - Store backend URL in frontend config (e.g., `.env.local`).

5. **Testing**
   - Use curl or Postman to test API endpoints before connecting frontend.

---

## Example curl test

```
curl -X POST http://127.0.0.1:5000/api/segmentation -H "Content-Type: application/json" -d '{"test": 1}'
```

---

## Next Steps
- Implement actual ML models in `app.py`.
- Scaffold frontend and connect to API.
- Expand API as needed for new tasks.
