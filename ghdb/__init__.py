"""
New worker template.

Worker description comes here.
"""

from .scrapper import HttpRetriever, GHDBScrapper  # pylint: disable=E0401

worker_class = WasWorker
worker_class_helper = HttpRetriever
