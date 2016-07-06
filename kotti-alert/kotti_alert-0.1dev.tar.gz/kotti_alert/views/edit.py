# -*- coding: utf-8 -*-

"""
Created on 2016-07-01
:author: Oshane Bailey (b4.oshany@gmail.com)
"""
import datetime
import colander
from kotti.views.edit import ContentSchema
from kotti.views.form import AddFormView
from kotti.views.form import EditFormView
from kotti.security import Principal
from pyramid.view import view_config
from deform.widget import RadioChoiceWidget

from kotti_alert import _
from kotti_alert.resources import Alert


def user_or_group_validator(node, value):
    # Aphanumeric value for the application key or the data release key
    user_or_group = Principal.query.filter(
        (Principal.name == value) |
        (Principal.name == "group:{}".format(value))
    ).first()
    if not user_or_group:
        raise colander.Invalid(
            node, _(u"Invalid username or group.")
        )


class AlertSchema(ContentSchema):
    """ Schema for Alert. """

    alert_type = colander.SchemaNode(
        colander.String(),
        title=_(u'Alert Type'),
        validator=colander.OneOf(["info", "warning", "danger"]),
        widget=RadioChoiceWidget(values=[
            ["info", _("Gernal Message")],
            ["warning", _("Warning")],
            ["danger", _("Important")]]
        )
    )

    active = colander.SchemaNode(
        colander.Boolean(),
        title=_(u'Enable this alert.'),
        default=False   
    )

    end_date = colander.SchemaNode(
        colander.Date(),
        default=(datetime.date.today() + datetime.timedelta(6*365/12))
    )
    
    priority = colander.SchemaNode(
        colander.Integer(),
        title=_(u'Priorty'),
        default=10
    )
    
    username_or_group = colander.SchemaNode(
        colander.String(),
        title=_(u'Username or group'),
        description=_(u'Only the specified user or group will see this alert'),
        validator=colander.All(user_or_group_validator),
        default="",
        missing=""
    )

    # track_user = colander.SchemaNode(
    #     colander.Boolean(),
    #     title=_(u'Track users who\'ve seen this alert'),
    #     default=False
    # )


@view_config(name=Alert.type_info.add_view, 
             permission=Alert.type_info.add_permission,
             renderer='kotti:templates/edit/node.pt')
class AlertAddForm(AddFormView):
    """ Form to add a new instance of Alert. """

    schema_factory = AlertSchema
    add = Alert
    item_type = _(u"Alert")


@view_config(name='edit', context=Alert, permission='edit',
             renderer='kotti:templates/edit/node.pt')
class AlertEditForm(EditFormView):
    """ Form to edit existing Alert objects. """

    schema_factory = AlertSchema
