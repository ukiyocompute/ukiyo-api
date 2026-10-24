# Ukiyo API

## 1. Agents paying with x402 or MPP, no account

Buy GPU blocks at `POST https://pay.u-kiyo.ai/api/machine/gpu-blocks` or jobs at `POST https://pay.u-kiyo.ai/api/machine/gpu-jobs`. Use any standard x402 v2 exact USDC client on Base, or an MPP client for Solana USDC or Tempo USDC.e. No signup or API key is required.

Read [pricing](https://pay.u-kiyo.ai/api/pricing), send the purchase details, current legal acceptance and a P-256 recovery public key, then retry the same URL and body with the standard payment header. Save the returned access token and retain the recovery private key. Read the [complete payment, recovery and Bazaar guide](https://docs.u-kiyo.ai/connect/machine-payments) before paying.

Cloudflare operators: raise the default $0.10 payment cap to cover the approved quote ($5 minimum); `maxPaymentValue: 5_000_000n` covers $5 USDC. Keep a cumulative budget. Live ghost/stall fallback replaces failed provider instances within the purchased specifications and budget, confirms destruction before replacement, and issues exactly-once service credit if provisioning fails. Anonymous cards and inference are unavailable.

## 2. Agents and developers using the API with an account

The existing API-key/account-balance flow is unchanged: CLI `ukiyo` 0.2.5, local MCP `ukiyo-mcp` 0.2.0 and pinned Skill `ukiyo-compute` 1.0.1. These are existing release downloads, not new npm releases. The account instructions below apply to this path. Skill 1.0.1's immutable artifact references CLI 0.2.2; keep the separately installed CLI 0.2.5. See the full guide for artifact links and checksums.


The HTTP API behind Ukiyo: list GPUs and prices, create an account, add credit, rent a GPU, get SSH access and shut it down. Everything the [CLI](https://github.com/ukiyocompute/ukiyo-cli) and [MCP server](https://github.com/ukiyocompute/ukiyo-mcp) do goes through this API.

**Base URL:** `https://pay.u-kiyo.ai/api/v1` · [OpenAPI spec](openapi.json) ([live](https://pay.u-kiyo.ai/api/openapi.json)) · [Docs](https://docs.u-kiyo.ai/connect/api)

## Quick start

Browsing is public:

```bash
curl https://pay.u-kiyo.ai/api/v1/offers   # rentable GPUs and prices
curl https://pay.u-kiyo.ai/api/v1/gpus     # GPU models and price ranges
curl https://pay.u-kiyo.ai/api/v1/terms    # current Terms version, URL and SHA-256
```

Create an account. This needs explicit agreement to the current [Terms](https://u-kiyo.ai/terms/), and returns a scoped agent key once:

```bash
curl -X POST https://pay.u-kiyo.ai/api/v1/signup \
  -H "Content-Type: application/json" \
  -H "Idempotency-Key: $(uuidgen)" \
  -d '{"termsAcceptance": {"version": "2026-10-10", "accepted": true}}'
```

Then send the key as `Authorization: Bearer $UKIYO_API_TOKEN`:

```bash
# Account, balance and limits
curl https://pay.u-kiyo.ai/api/v1/me -H "Authorization: Bearer $UKIYO_API_TOKEN"

# Get a hosted checkout link to add $5 of credit (a person opens and pays it)
curl -X POST https://pay.u-kiyo.ai/api/v1/billing/topups \
  -H "Authorization: Bearer $UKIYO_API_TOKEN" -H "Content-Type: application/json" \
  -H "Idempotency-Key: $(uuidgen)" -d '{"amountMinor": 500}'

# Rent one RTX 4090 at up to $1.00/hour
curl -X POST https://pay.u-kiyo.ai/api/v1/rentals \
  -H "Authorization: Bearer $UKIYO_API_TOKEN" -H "Content-Type: application/json" \
  -H "Idempotency-Key: $(uuidgen)" \
  -d '{"gpuModel": "RTX4090", "gpuCount": 1, "maxHourlyPriceMinor": 100}'

# Check progress until it is ACTIVE, then shut it down when finished
curl https://pay.u-kiyo.ai/api/v1/rentals/<rentalId> -H "Authorization: Bearer $UKIYO_API_TOKEN"
curl -X POST https://pay.u-kiyo.ai/api/v1/deployments/<deploymentId>/terminate -H "Authorization: Bearer $UKIYO_API_TOKEN"
```

Amounts are in US cents (`500` = $5.00). Reuse the same `Idempotency-Key` when retrying after a timeout, so a retry never rents twice.

## Examples

- [`examples/list-offers.py`](examples/list-offers.py): Python, no dependencies
- [`examples/list-offers.mjs`](examples/list-offers.mjs): Node.js, no dependencies

## Good to know

- Responses are `{"data": ...}`; errors are `{"error": {"code", "message", "requestId"}}` with a matching HTTP status.
- Account-balance rentals don't need a budget and stop automatically when your balance runs low. Older prepaid accounts must send `budgetMinor`; check `GET /me` (`billing.budgetRequired`).
- Retrieve SSH details with `POST /deployments/{id}/credentials/reveal`, or let the CLI handle keys for you.
- Billing details: [Billing](https://docs.u-kiyo.ai/guides/billing) · [Terms](https://u-kiyo.ai/terms/) · [Privacy](https://u-kiyo.ai/privacy/)

## Related

- [ukiyo-cli](https://github.com/ukiyocompute/ukiyo-cli) · [ukiyo-mcp](https://github.com/ukiyocompute/ukiyo-mcp) · [ukiyo-skill](https://github.com/ukiyocompute/ukiyo-skill) · [ukiyo-guides](https://github.com/ukiyocompute/ukiyo-guides)

## Support and security

**contact@u-kiyo.ai**. Please don't include API keys or private keys in issues.

## License

The examples in this repository are [MIT](LICENSE) © 2026 Ukiyo Compute LLC. The Ukiyo service and API are governed by the [Terms](https://u-kiyo.ai/terms/).
