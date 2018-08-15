from flask import request
from flask import Response
from flask_restful import Resource
from flask_restful import abort

from dicttoxml import dicttoxml

from .app import api
from .app import db
from .models import Report
from .serializers import ReportSchema

report_schema = ReportSchema()


class ReportsAPIPost(Resource):
    @staticmethod
    def post():
        args = request.get_json()
        if not args:
            abort(400, message="Please send json payload")

        report = report_schema.load(args, session=db.session).data
        db.session.add(report)
        db.session.commit()

        return report_schema.dump(report)[0], 201

    @staticmethod
    def get():
        # List view, no filters supported yet
        return [report_schema.dump(report)[0] for report in Report.query.all()]


class ReportsAPI(Resource):
    @staticmethod
    def get_entity(report_id):
        return Report.query.get_or_404(report_id)

    def get(self, report_id):
        response = report_schema.dump(self.get_entity(report_id))[0], 200
        if request.args.get('format') == 'xml':
            response = Response(dicttoxml(response), mimetype='text/xml')

        return response

    def delete(self, report_id):
        db.session.delete(self.get_entity(report_id))
        db.session.commit()
        return report_id, 204


api.add_resource(ReportsAPI, '/reports/<report_id>')
api.add_resource(ReportsAPIPost, '/reports')
