"""Data models for News."""

from dataclasses import dataclass


@dataclass
class Article:
	"""Represents a news article."""

	title: str
	description: str
	url: str
