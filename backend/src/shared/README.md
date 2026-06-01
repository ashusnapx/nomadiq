# Shared Infrastructure Utilities

## Purpose
Collects shared infrastructural tools: database connection lifecycles, caching interfaces, circuit breakers, and exponential backoff retry wrappers.

## Ownership
Engineering Platform Team

## Structure
- `database.py`: Async connection pooling utilizing pgvector.
- `redis_client.py`: In-memory cache layer fallback options.
- `circuit_breaker.py`: Fault isolation mechanics.
- `retry.py`: Retries with exponential backoff + random jitter.

## Extension Strategy
Add generic helper utilities here if they don't depend on specific business logic components, maintaining low file sizes.
