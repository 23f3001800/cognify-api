cognify-api



POST /ingest        → upload + chunk + embed a document (background job)
GET  /jobs/{id}     → poll ingestion status
POST /chat          → streaming conversational RAG
POST /summarise     → structured summarisation with style options
POST /embed         → batch text embeddings
GET  /health        → health + readiness probe
GET  /docs          → auto Swagger UI (free, automatic)

Features baked in:
  ✓ LangSmith tracing on every LLM call
  ✓ Redis response caching (in-memory fallback)
  ✓ API key authentication
  ✓ Rate limiting per IP
  ✓ Structured JSON logging
  ✓ Retry with exponential backoff
  ✓ Pydantic validation on all endpoints
  ✓ Dockerised + docker-compose ready
  ✓ Deployed to Railway with CI/CD