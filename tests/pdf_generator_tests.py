from flask_testing import TestCase
from unittest.mock import patch

from pdf_generator.app import app
from pdf_generator.app import db
from pdf_generator.models import Organization


class PDFGeneratorTests(TestCase):
    def setUp(self):
        db.create_all()
        db.session.commit()

    def create_app(self):
        app.config.from_object('pdf_generator.config.TestingConfig')
        return app

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    @patch('pdf_generator.serializers.get_current_time')
    def test_report_json_api(self, current_time_mock):
        # Annoying to have real dynamic timestamps in a test
        # I'm pretty confident datetime.utcnow() works so let's patch it
        time_now = 'This is a real Timestamp!!'
        current_time_mock.return_value = time_now

        org_name = "RobertCorp"
        reported = '2018-08-14T20:44:34+00:00'

        db.session.add(Organization(name=org_name))
        db.session.commit()

        response = self.client.post('/reports', json={'organization': 1, 'reported': reported})
        self.assertEqual(response.status_code, 201)

        first_report = {
            'id': 1,
            'organization': 1,
            'reported': reported,
            'created': time_now,
            'inventory': [],
        }
        self.assertEqual(response.get_json(), first_report)

        response = self.client.get('/reports')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), [first_report])
