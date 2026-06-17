from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


class Phase1GovernanceDocsTests(unittest.TestCase):
    def read_doc(self, name: str) -> str:
        return (ROOT / "docs" / name).read_text(encoding="utf-8")

    def test_threat_model_documents_safety_gates(self) -> None:
        text = self.read_doc("threat-model.md")
        self.assertIn("synthetic-agent disclosure", text)
        self.assertIn("ROPA", text)
        self.assertIn("anonymous donation cap remains 2,940 SEK", text)

    def test_inter_node_api_preserves_phase1_constraints(self) -> None:
        text = self.read_doc("inter-node-api.md")
        self.assertIn('"advisory_only": true', text)
        self.assertIn("No wallet/Crossmint/crypto endpoint", text)
        self.assertIn("No personal-data replication", text)

    def test_governance_rules_block_mandate_and_identity_confusion(self) -> None:
        text = self.read_doc("governance-rules.md")
        self.assertIn("must never claim to be human", text)
        self.assertIn("advisory-only", text)
        self.assertIn("No autonomous spending", text)


if __name__ == "__main__":
    unittest.main()
