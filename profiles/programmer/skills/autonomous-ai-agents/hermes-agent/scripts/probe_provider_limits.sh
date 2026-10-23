#!/usr/bin/env bash
# Probe an OpenAI-compatible provider BEFORE recommending a switch: reachability,
# latency, and per-minute rate limits read from the response headers.
#
# A provider can answer 200 in under a second and still be unusable for a long
# session -- x-ratelimit-limit-tokens is TOKENS PER MINUTE (TPM), and a turn that
# carries a bloated context cannot fit under a low cap. Always report the MEASURED
# number and compare it to the current prompt size.
#
# Usage:
#   probe_provider_limits.sh <BASE_URL> <MODEL> <ENV_KEY_NAME> [ENV_FILE]
# Example:
#   probe_provider_limits.sh https://api.groq.com/openai/v1 openai/gpt-oss-120b GROQ_API_KEY

set -u
BASE_URL="${1:?usage: probe_provider_limits.sh BASE_URL MODEL ENV_KEY_NAME [ENV_FILE]}"
MODEL="${2:?model required}"
ENV_NAME="${3:?env key name required (e.g. GROQ_API_KEY)}"
ENV_FILE="${4:-${HERMES_HOME:-$HOME/.hermes}/.env}"

if [ ! -f "$ENV_FILE" ]; then
  echo "!! env file not found: $ENV_FILE" >&2
  exit 1
fi

# CRLF-safe: the .env on Windows keeps \r, which corrupts the bearer token.
KEY=$(grep -aE "^${ENV_NAME}=" "$ENV_FILE" | head -1 | cut -d= -f2- | tr -d '\r')
if [ -z "$KEY" ]; then
  echo "!! ${ENV_NAME} not set in ${ENV_FILE}" >&2
  exit 1
fi
echo "key: ${ENV_NAME} present (length ${#KEY})"
echo "model: ${MODEL}"

echo "--- probe ---"
curl -s -D - -o /dev/null -m 25 "${BASE_URL%/}/chat/completions" \
  -H "Authorization: Bearer $KEY" \
  -H "Content-Type: application/json" \
  -d "{\"model\":\"$MODEL\",\"messages\":[{\"role\":\"user\",\"content\":\"ok\"}],\"max_tokens\":5}" \
  -w "\ntime_total: %{time_total}s\n" \
  | grep -aiE "^HTTP/|x-ratelimit|retry-after|time_total"

echo "--- note ---"
echo "x-ratelimit-limit-tokens = tokens per minute (TPM). If the current context"
echo "exceeds it, each turn stalls waiting for the bucket to refill -- a low-cap"
echo "'free' provider can be worse than a paid one for a long-lived session."
