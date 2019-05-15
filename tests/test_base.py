from flask_testing import TestCase
from flask import current_app, url_for
from main import app


class mainTest(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        return app

    def test_app_exist(self):
        self.assertIsNotNone(current_app)

    def test_app_in_test_mode(self):
        self.assertTrue(current_app.config['TESTING'])

    def test_index_redirect(self):
        responde = self.client.get(url_for('index'))
        self.assertRedirects(responde, url_for('hello'))

    # def test_hello_get(self):
    #     response = self.client.get(url_for('hello'))
    #     self.assert200(response)

    # def test_contact_post(self):
    #     data_form = {
    #         'name': 'Andres',
    #         'email': 'abecerra@gmail.com'
    #     }
    #     response = self.client.post(url_for('contact'), data=data_form)
    #     self.assertRedirects(response, url_for('contact'))

    def test_auth_blueprint_exist(self):
        self.assertIn('auth', self.app.blueprints)

    def test_auth_login(self):
        response = self.client.get(url_for('auth.login'))
        self.assert200(response)

    def test_template_login(self):
        self.client.get(url_for('auth.login'))
        self.assertTemplateUsed('login.html')
