from datetime import datetime

from marshmallow import post_dump
from marshmallow import fields

from .app import ma
from .models import Organization
from .models import Report
from .models import Item


def get_current_time():
    # This exists purely to be mocked in tests
    return datetime.utcnow().isoformat()


class OrganizationSchema(ma.ModelSchema):
    class Meta:
        model = Organization


class ItemSchema(ma.ModelSchema):
    class Meta:
        model = Item
        fields = (
            'id',
            'name',
            'price',
        )


class ReportSchema(ma.ModelSchema):
    class Meta:
        model = Report

    inventory = fields.Nested(ItemSchema, many=True)
    inventory = fields.Nested(ItemSchema, many=True)

    @post_dump(pass_many=False)
    def add_created(self, data):  # pylint: disable=no-self-use
        data['created'] = get_current_time()
        return data
