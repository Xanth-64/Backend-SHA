# -*- coding: utf-8 -*-
"""Test case suite for the App Object File."""

from flask import Flask


class TestApp:
    """Test suite for the App Object File."""

    def test_app_exists(self, server_app):
        """Test that the app exists"""
        assert server_app

    def test_app_is_correct_type(self, server_app):
        """Test that the app is of the correct type"""
        assert isinstance(server_app, Flask)
