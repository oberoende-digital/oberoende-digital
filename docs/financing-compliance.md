# Financing compliance — Phase 0 skeleton

**Project:** Oberoende Digital Quberon 0 backend  
**Scope:** Donations, membership payments, campaign contributions, wallet/payment data structures, treasury transparency  
**Status:** Phase 0 bootstrap; requires legal/admin review before accepting production payments  
**Primary sources:** Swedish law on transparency in party financing, OD White Paper v2.2 financing/risk sections, backend instruction v2.

> MVP position: **read-only wallet/payment integration only**. No autonomous spending. Crypto donations disabled by default. Compliance and auditability take priority over convenience.

## Hard-coded legal/operational constants

These values must be versioned in code before payment features are enabled:

```ts
export const FINANCING_LIMITS = {
  anonymousDonationCapSEK: 2940,
  anonymousDonationCapBasis: "0.05 price base amount; Phase 0 instruction value for Swedish party-financing transparency law",
  cryptoEnabledDefault: false,
  outgoingTransactionsRequireHumanApproval: true,
  phase: "MVP_PHASE_1_READ_ONLY"
} as const;
```

## Core rules

1. **Anonymous donation cap:** An anonymous donor may not be accepted above **2 940 SEK per donor per calendar year**. The backend must refuse, refund/return, or hold for review any anonymous amount exceeding the cap.
2. **KYC threshold:** Donations exceeding the anonymous cap require identity verification before acceptance.
3. **No autonomous spending:** Outgoing transactions require explicit human-admin approval and audit logging.
4. **Crypto off in Phase 1:** `crypto_enabled = false` by default. The flag can exist but must default safe, and enabling requires human-admin review.
5. **Read-only wallet MVP:** Crossmint/fiat wallet integration may read status and transactions, but must not initiate transfers.
6. **Tagged transactions:** Every transaction must have wallet/source and purpose tags.
7. **Audit export:** Financing data must be exportable for human review and future Kammarkollegiet reporting.
8. **GDPR alignment:** Financing records are personal data and may have legal-retention obligations overriding erasure requests.

## Required transaction tags

| Dimension | Allowed values |
|---|---|
| Wallet/account type | `crypto_wallet`, `fiat_cash_wallet` |
| Transaction type | `incoming_donation`, `outgoing_payment`, `membership_payment`, `campaign_related`, `operational_expense` |
| Review status | `pending_review`, `accepted`, `rejected`, `refunded`, `requires_kyc`, `requires_human_approval`, `reported` |
| Donor identity status | `anonymous`, `identified`, `kyc_pending`, `kyc_verified`, `unknown` |
| Phase guard | `read_only_mvp`, `manual_admin_only`, `blocked_autonomous_action` |

## Wallet/payment data model obligations

| Entity | Required fields | Compliance notes | Status |
|---|---|---|---|
| `WalletAccount` | `id`, `provider`, `account_type`, `currency`, `read_only`, `crypto_enabled`, `created_at`, `updated_at` | `read_only=true` and `crypto_enabled=false` by default in MVP | amber |
| `WalletTransaction` | `id`, `provider_tx_id`, `wallet_account_id`, `amount`, `currency`, `sek_equivalent`, `direction`, `type_tag`, `purpose_tag`, `donor_identity_status`, `review_status`, `calendar_year`, `created_at`, `updated_at` | No outgoing transaction execution; store only read/imported transactions | amber |
| `DonationRecord` | `donor_key_hash`, `amount_sek`, `calendar_year`, `anonymous`, `kyc_status`, `acceptance_status`, `reviewer`, `reviewed_at` | Aggregate yearly anonymous donations by donor if donor can be linked; otherwise apply conservative review | amber |
| `HumanApproval` | `action`, `requested_by`, `approved_by`, `timestamp`, `signature_or_attestation`, `reason`, `related_tx_id` | Required for outgoing transactions and KYC-sensitive acceptance | amber |

## Donation acceptance decision table

| Scenario | Backend action | Human/admin action | Audit log |
|---|---|---|---|
| Anonymous donation ≤ 2 940 SEK/year | May accept if other checks pass | Optional review | Log amount, year, anonymous status, source |
| Anonymous donation would exceed 2 940 SEK/year | Do not accept excess automatically; mark `requires_kyc` or `rejected/refunded` | Request identity verification or return excess | Log threshold rule and outcome |
| Identified/KYC donation above cap | Hold for manual review | Verify identity, legality, reporting obligations | Log reviewer, basis, report status |
| Incoming crypto transaction while `crypto_enabled=false` | Mark blocked/requires review; do not treat as accepted donation automatically | Decide return/hold/legal handling | Log safe-default block |
| Any outgoing payment | Block autonomous execution | Explicit human-admin approval required | Log approval and final execution reference |
| Membership payment | Accept only through approved fiat/payment route | Reconcile membership status manually/MVP | Log payment type and member link |

## Phase 1 configuration file target

Create `config/financing.ts` before any wallet module ships:

```ts
export const FINANCING_CONFIG = {
  currency: "SEK",
  anonymousDonationCapSEK: 2940,
  cryptoEnabled: false,
  outgoingTransactionsRequireHumanApproval: true,
  walletMode: "read_only",
  reportingAuthority: "Kammarkollegiet",
  transactionTags: [
    "crypto_wallet",
    "fiat_cash_wallet",
    "incoming_donation",
    "outgoing_payment",
    "membership_payment",
    "campaign_related",
    "operational_expense"
  ]
} as const;
```

## Open legal/admin review items

- Confirm the exact current price-base-amount calculation and whether the 2 940 SEK instruction value needs annual update automation.
- Confirm OD's current legal entity status and whether party-financing reporting duties already apply or are preparatory only.
- Select payment processors and obtain/review DPAs before production use.
- Decide public treasury disclosure format and redaction level.
- Decide how to handle unsolicited crypto deposits while crypto is disabled.

## Evidence paths

- `docs/gdpr-ropa.md` — financing records as ROPA activity ROPA-007.
- `config/financing.ts` — required Phase 1 implementation target.
- `src/wallet/` — read-only wallet import/status module target.
- `reports/safety/YYYY-WW.md` — weekly open compliance items and incidents.
