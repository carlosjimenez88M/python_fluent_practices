"""Custom exceptions for News."""


class NewsError(Exception):
	"""Base exception for News application."""

	pass


class ConfigError(NewsError):
	"""Raised when there are configuration issues."""

	pass


class APIError(NewsError):
	"""Raised when there are API-related errors."""

	pass


class AnalysisError(NewsError):
	"""Raised when there are analysis-related errors."""

	pass


class SourceError(NewsError):
	"""Raised when there are news source-related errors."""

	pass
