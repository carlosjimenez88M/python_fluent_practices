"""Tests for exceptions."""

import unittest

from news.core.exceptions import (
	AnalysisError,
	APIError,
	ConfigError,
	NewsError,
	SourceError,
)


class TestExceptions(unittest.TestCase):
	"""Test custom exceptions."""

	def test_news_error(self):
		"""Test NewsError base exception."""
		error = NewsError("Test error")
		self.assertIsInstance(error, Exception)
		self.assertEqual(str(error), "Test error")

	def test_config_error(self):
		"""Test ConfigError."""
		error = ConfigError("Config error")
		self.assertIsInstance(error, NewsError)
		self.assertEqual(str(error), "Config error")

	def test_api_error(self):
		"""Test APIError."""
		error = APIError("API error")
		self.assertIsInstance(error, NewsError)
		self.assertEqual(str(error), "API error")

	def test_analysis_error(self):
		"""Test AnalysisError."""
		error = AnalysisError("Analysis error")
		self.assertIsInstance(error, NewsError)
		self.assertEqual(str(error), "Analysis error")

	def test_source_error(self):
		"""Test SourceError."""
		error = SourceError("Source error")
		self.assertIsInstance(error, NewsError)
		self.assertEqual(str(error), "Source error")

	def test_exception_hierarchy(self):
		"""Test exception inheritance hierarchy."""
		errors = [ConfigError(""), APIError(""), AnalysisError(""), SourceError("")]
		for error in errors:
			with self.subTest(error=error):
				self.assertIsInstance(error, NewsError)
				self.assertIsInstance(error, Exception)


if __name__ == "__main__":
	unittest.main()
