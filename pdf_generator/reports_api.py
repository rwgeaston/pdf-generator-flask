# from flask import request

from flask_restful import Resource
from flask_restful import abort
from flask_restful.reqparse import RequestParser

from dateutil import parser

from .app import api
from .app import db
from .models import Organization
from .models import Report
# from .models import Item


class ReportRequestParser(RequestParser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_argument('organization', help='name of organization this report is for', required=True)
        self.add_argument('reported', type=str, help='name of organization this report is for', required=True)


request_parser = ReportRequestParser()


class ReportsAPIPost(Resource):
    @staticmethod
    def post():
        args = request_parser.parse_args()
        organization = Organization.query.filter_by(name=args['organization']).first()
        if not organization:
            abort('400', message='No Organization with this name to link report to')

        reported = parser.parse(args['reported'])
        report = Report(organization=organization, reported=reported)
        db.session.add(report)
        db.session.commit()

        return report.serialise(), 201

    @staticmethod
    def get():
        # List view, no filters supported yet
        return [report.serialise() for report in Report.query.all()]


# class ReportsAPI(Resource):
#     @staticmethod
#     def get(slug):
#         return None
#
#     def put(self, slug):
#         return None
#
#     @staticmethod
#     def patch(slug):
#         return None
#
#     @staticmethod
#     def delete(slug):
#         return slug, 204


# api.add_resource(ReportsAPI, '/reports/<report_id>')
api.add_resource(ReportsAPIPost, '/reports')
