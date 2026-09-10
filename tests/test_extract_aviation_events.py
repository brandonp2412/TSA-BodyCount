import unittest

from scripts.extract_aviation_events import aviation_hijacking


class AviationHijackingTests(unittest.TestCase):
    def test_does_not_match_aviation_keywords_inside_other_words(self):
        row = {
            "summary": "Hostages were taken at a Planet Fitness gym.",
            "target1": "Planet Fitness",
        }

        self.assertFalse(aviation_hijacking(row, ["Hijacking"]))

    def test_matches_standalone_aviation_keyword_case_insensitively(self):
        row = {"summary": "The group hijacked a PLANE after boarding."}

        self.assertTrue(aviation_hijacking(row, ["Hijacking"]))

    def test_non_hijacking_attack_is_not_selected_by_text_alone(self):
        row = {"summary": "An airport was mentioned in the report."}

        self.assertFalse(aviation_hijacking(row, ["Bombing/Explosion"]))


if __name__ == "__main__":
    unittest.main()
