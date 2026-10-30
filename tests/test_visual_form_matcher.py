import unittest
from scripts.visual_form_matcher import rank_forms, score_candidate


class VisualFormMatcherTests(unittest.TestCase):
    def setUp(self):
        self.forms = [{
            "form_id": "VFORM-TEST",
            "name": "Test form",
            "applicable_domains": ["physics"],
            "structural_signature": {
                "component_types": ["x_axis", "y_axis", "data_series"],
                "relationship_types": ["plotted_on_axis"]
            }
        }]

    def test_exact_structure_scores_above_partial(self):
        exact = {"component_types": ["x_axis", "y_axis", "data_series"],
                 "relationship_types": ["plotted_on_axis"], "domains": ["physics"]}
        partial = {"component_types": ["x_axis"], "relationship_types": [],
                   "domains": ["biology"]}
        self.assertGreater(score_candidate(exact, self.forms[0])["score"],
                           score_candidate(partial, self.forms[0])["score"])

    def test_required_components_are_reported(self):
        candidate = {"component_types": ["x_axis"], "relationship_types": [],
                     "required_component_types": ["x_axis", "detector"]}
        result = score_candidate(candidate, self.forms[0])
        self.assertEqual(result["evidence"]["missing_required_components"], ["detector"])

    def test_empty_evidence_is_deterministic(self):
        results = rank_forms({}, self.forms)
        self.assertEqual(results[0]["form_id"], "VFORM-TEST")
        self.assertGreaterEqual(results[0]["score"], 0)


if __name__ == "__main__":
    unittest.main()
