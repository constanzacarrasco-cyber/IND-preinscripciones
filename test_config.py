"""Pruebas básicas sin datos personales ni servicios externos."""

import unittest

from ind_app.config import CAMPOS_INFORMADOS_SIGI, PAGES


class TestConfig(unittest.TestCase):
    def test_nueve_campos_informados(self):
        self.assertEqual(len(CAMPOS_INFORMADOS_SIGI), 9)
        self.assertEqual(CAMPOS_INFORMADOS_SIGI[0], "RUT")
        self.assertEqual(CAMPOS_INFORMADOS_SIGI[-1], "Comuna")

    def test_pages(self):
        self.assertEqual(PAGES, {"inicio", "profesor", "ind"})


if __name__ == "__main__":
    unittest.main()
