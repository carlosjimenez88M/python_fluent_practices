"""Tests for news sources."""

import unittest
from unittest.mock import Mock, patch

import requests

from news.core.exceptions import APIError
from news.core.services import NewsService
from news.sources.guardian import GuardianAPI
from news.sources.newsapi import NewsAPI


class TestGuardianAPI(unittest.TestCase):
	"""Test GuardianAPI."""

	@patch("news.config.settings")
	def setUp(self, mock_settings):
		mock_settings.guardian_api_key = "fake_key"
		self.api = GuardianAPI()

	@patch("news.sources.newsapi.requests.get")
	def test_fetch_articles_success(self, mock_get):
		mock_response = Mock()
		mock_response.raise_for_status.return_value = None
		mock_response.json.return_value = {
			"response": {
				"results": [
					{
						"webTitle": "Test Title",
						"webUrl": "http://example.com",
						"fields": {"trailText": "Test description"},
					}
				]
			}
		}
		mock_get.return_value = mock_response

		articles = self.api.fetch_articles("test query")
		self.assertEqual(len(articles), 1)
		self.assertEqual(articles[0].title, "Test Title")
		self.assertEqual(articles[0].description, "Test description")
		self.assertEqual(articles[0].url, "http://example.com")

	@patch("news.sources.guardian.requests.get")
	def test_fetch_articles_error(self, mock_get):
		mock_get.side_effect = requests.RequestException("Network error")
		with self.assertRaises(APIError):
			self.api.fetch_articles("test query")


class TestNewsAPI(unittest.TestCase):
	"""Test NewsAPI."""

	@patch("news.config.settings")
	def setUp(self, mock_settings):
		mock_settings.newsapi_api_key = "fake_key"
		self.api = NewsAPI()

	@patch("news.sources.guardian.requests.get")
	def test_fetch_articles_success(self, mock_get):
		mock_response = Mock()
		mock_response.raise_for_status.return_value = None
		mock_response.json.return_value = {
			"articles": [
				{
					"title": "Test Title",
					"description": "Test description",
					"url": "http://example.com",
				}
			]
		}
		mock_get.return_value = mock_response

		articles = self.api.fetch_articles("test query")
		self.assertEqual(len(articles), 1)
		self.assertEqual(articles[0].title, "Test Title")

	@patch("news.sources.newsapi.requests.get")
	def test_fetch_articles_error(self, mock_get):
		mock_get.side_effect = requests.RequestException("Network error")
		with self.assertRaises(APIError):
			self.api.fetch_articles("test query")


class TestNewsService(unittest.TestCase):
	"""Test NewsService."""

	@patch("news.config.settings")
	@patch("news.core.services.get_analyzer")
	def test_init(self, mock_get_analyzer, mock_settings):
		mock_settings.guardian_api_key = "fake_guardian"
		mock_settings.newsapi_api_key = "fake_newsapi"
		mock_analyzer = Mock()
		mock_get_analyzer.return_value = mock_analyzer

		service = NewsService()
		self.assertIsInstance(service.sources["guardian"], GuardianAPI)
		self.assertIsInstance(service.sources["newsapi"], NewsAPI)
		self.assertEqual(service.analyzer, mock_analyzer)

	def test_get_source_valid(self):
		service = NewsService()
		source = service.get_source("guardian")
		self.assertIsInstance(source, GuardianAPI)

	def test_get_source_invalid(self):
		service = NewsService()
		with self.assertRaises(ValueError):
			service.get_source("invalid")

	@patch("news.core.services.GuardianAPI")
	def test_search_articles(self, mock_guardian):
		mock_source = Mock()
		mock_source.fetch_articles.return_value = [Mock()]
		mock_guardian.return_value = mock_source

		service = NewsService()
		service.sources["guardian"] = mock_source
		articles = service.search_articles("guardian", "query")
		mock_source.fetch_articles.assert_called_once_with("query")
		self.assertEqual(len(articles), 1)

	@patch("news.core.services.get_analyzer")
	def test_analyze_articles(self, mock_get_analyzer):
		mock_analyzer = Mock()
		mock_analyzer.analyze.return_value = "answer"
		mock_get_analyzer.return_value = mock_analyzer

		service = NewsService()
		articles = [Mock()]
		answer = service.analyze_articles(articles, "question")
		mock_analyzer.analyze.assert_called_once_with(articles, "question")
		self.assertEqual(answer, "answer")


if __name__ == "__main__":
	unittest.main()
