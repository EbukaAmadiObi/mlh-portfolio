import unittest
import os
os.environ['TESTING'] = 'true'

from app import app

class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_home(self):
        response = self.client.get("/")
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert "<title>Ebuka&#39;s Portfolio</title>" in html
        
        nav_links = [
            '<li><a href="/">Home</a></li>',
            '<li><a href="/about">About</a></li>',
            '<li><a href="/work">Work</a></li>',
            '<li><a href="/education">Education</a></li>',
            '<li><a href="/hobbies">Hobbies</a></li>',
            '<li><a href="/travel">Travel</a></li>',
            '<li><a href="/timeline">Timeline</a></li>'
        ]
        for link in nav_links:
            assert link in html

    def test_timeline(self):
        # Test GET endpoint before posting
        response = self.client.get("/api/timeline_post")
        assert response.status_code == 200
        assert response.is_json
        json = response.get_json()
        assert "timeline_posts" in json
        assert len(json["timeline_posts"]) == 0

        # Test POST endpoint
        post_response = self.client.post('/api/timeline_post', data={
                            'name': 'salim pinapple lover',
                            'email': 'salim@pinapplelover.com',
                            'content': 'This is a test timeline post'
        })
        assert post_response.status_code == 200
        assert post_response.is_json
        post_json = post_response.get_json()
        assert post_json["name"] == 'salim pinapple lover'
        assert post_json["email"] == 'salim@pinapplelover.com'
        assert post_json["content"] == 'This is a test timeline post'

        # Test GET endpoint after posting
        get_response = self.client.get("/api/timeline_post")
        assert get_response.status_code == 200
        assert get_response.is_json
        get_json = get_response.get_json()
        assert "timeline_posts" in get_json
        assert len(get_json["timeline_posts"]) == 1

        # Test timeline page
        page_response = self.client.get("/timeline")
        assert page_response.status_code == 200
        html = page_response.get_data(as_text=True)
        assert "This is a test timeline post" in html
        assert "salim@pinapplelover.com" in html

    def test_malformed_timeline_post(self):
        # POST request missing name
        response = self.client.post("/api/timeline_post", data={"email": "salim@pinapplelover.com", "content": "Hello world, I'm Salim!"})
        assert response.status_code == 500

        # POST request with empty content
        response = self.client.post("/api/timeline_post", data={"name": "salim pinapple lover", "email": "salim@pinapplelover.com", "content": ""})
        assert response.status_code == 500

        # POST request with malformed email
        response = self.client.post("/api/timeline_post", data={"name": "salim pinapple lover", "email": "not-an-email", "content": "Hello world, I'm Salim!"})
        assert response.status_code == 500
