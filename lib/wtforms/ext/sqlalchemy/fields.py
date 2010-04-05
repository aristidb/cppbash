"""
Useful form fields for use with SQLAlchemy ORM.
"""
from operator import attrgetter
from sqlalchemy.orm.util import identity_key

from wtforms import widgets
from wtforms.fields import Field
from wtforms.validators import ValidationError



__all__ = (
    'QuerySelectField', 'ModelSelectField',
)


class QuerySelectField(Field):
    """
    Will display a select drop-down field to choose between ORM results in a
    sqlalchemy `Query`.  The `data` property actually will store/keep an ORM
    model instance, not the ID. Submitting a choice which is not in the query
    will result in a validation error.

    This field only works for queries on models whose primary key column(s)
    have a consistent string representation. This means it mostly only works
    for those composed of string, unicode, and integer types. For the most
    part, the primary keys will be auto-detected from the model, alternately
    pass a one-argument callable to `get_pk` which can return a unique
    comparable key.

    The `query` property on the field can be set from within a view to assign
    a query per-instance to the field. If the property is not set, the
    `query_factory` callable passed to the field constructor will be called to
    obtain a query.

    Specifying `label_attr` in the constructor will use that property of the
    model instance for display in the list, else the model object's `__str__`
    or `__unicode__` will be used.

    If `allow_blank` is set to `True`, then a blank choice will be added to the
    top of the list. Selecting this choice will result in the `data` property
    being `None`. The label for this blank choice can be set by specifying the
    `blank_text` parameter.

    The `pk_attr` parameter is deprecated and will likely be removed in a
    future release.
    """
    widget = widgets.Select()

    def __init__(self, label=u'', validators=None, query_factory=None,
                 get_pk=None, label_attr='', allow_blank=False, blank_text=u'',
                 pk_attr=None, **kwargs):
        super(QuerySelectField, self).__init__(label, validators, **kwargs)
        self.query_factory = query_factory
        if pk_attr is not None:
            self.get_pk = attrgetter(pk_attr)
        elif get_pk is None:
            self.get_pk = get_pk_from_identity
        else:
            self.get_pk = get_pk

        self.label_attr = label_attr
        self.allow_blank = allow_blank
        self.blank_text = blank_text
        self.query = None
        self._object_list = None

    def _get_data(self):
        if self._formdata is not None:
            for pk, obj in self._get_object_list():
                if pk == self._formdata:
                    self._set_data(obj)
                    break
        return self._data

    def _set_data(self, data):
        self._data = data
        self._formdata = None

    data = property(_get_data, _set_data)

    def _get_object_list(self):
        if self._object_list is None:
            query = self.query or self.query_factory()
            get_pk = self.get_pk
            self._object_list = list((unicode(get_pk(obj)), obj) for obj in query)
        return self._object_list

    def iter_choices(self):
        if self.allow_blank:
            yield (u'__None', self.blank_text, self.data is None)

        for pk, obj in self._get_object_list():
            label = self.label_attr and getattr(obj, self.label_attr) or obj
            yield (pk, label, obj == self.data)

    def process_formdata(self, valuelist):
        if valuelist:
            if self.allow_blank and valuelist[0] == u'__None':
                self.data = None
            else:
                self._data = None
                self._formdata = valuelist[0]

    def pre_validate(self, form):
        if not self.allow_blank or self.data is not None:
            for pk, obj in self._get_object_list():
                if self.data == obj:
                    break
            else:
                raise ValidationError('Not a valid choice')


class QueryMultipleSelectField(QuerySelectField):
    """
    Very similar to QuerySelectField with the difference that this will
    display a multiple select. The data property will hold a list with ORM
    model instances and will be an empty list when no value is selected.

    If any of the items in the data list or submitted form data cannot be
    found in the query, this will result in a validation error.
    """
    widget = widgets.Select(multiple=True)

    def __init__(self, label=u'', validators=None, query_factory=None, get_pk=None,
                 label_attr='', default=None, **kwargs):
        if default is None:
            default = []
        super(QueryMultipleSelectField, self).__init__(label, validators, query_factory=query_factory, get_pk=get_pk, label_attr=label_attr, default=default, **kwargs)
        self._invalid_formdata = False

    def _get_data(self):
        formdata = self._formdata
        if formdata is not None:
            data = []
            for pk, obj in self._get_object_list():
                if not formdata:
                    break
                elif pk in formdata:
                    formdata.remove(pk)
                    data.append(obj)
            if formdata:
                self._invalid_formdata = True
            self._set_data(data)
        return self._data

    def _set_data(self, data):
        self._data = data
        self._formdata = None

    data = property(_get_data, _set_data)

    def iter_choices(self):
        for pk, obj in self._get_object_list():
            label = self.label_attr and getattr(obj, self.label_attr) or obj
            yield (pk, label, obj in self.data)

    def process_formdata(self, valuelist):
        self._formdata = set(valuelist)

    def pre_validate(self, form):
        if self._invalid_formdata:
            raise ValidationError('Not a valid choice')
        elif self.data:
            obj_list = list(x[1] for x in self._get_object_list())
            for v in self.data:
                if v not in obj_list:
                    raise ValidationError('Not a valid choice')


class ModelSelectField(QuerySelectField):
    """
    Similar to QuerySelectField, only for model classes.

    Using this field is only meaningful when using scoped sessions in
    SQLAlchemy, because otherwise model instances do not know how to make
    queries of themselves. This field is simply a convenience for using
    `Model.query` as the factory for QuerySelectField.
    """
    def __init__(self, label=u'', validators=None, model=None, get_pk=None,
                 label_attr='', allow_blank=False, blank_text=u'', **kwargs):
        assert model is not None, "Must specify a model."
        query_factory = lambda: model.query
        super(ModelSelectField, self).__init__(label, validators, query_factory=query_factory, get_pk=get_pk, label_attr=label_attr, allow_blank=allow_blank, blank_text=blank_text, **kwargs)


def get_pk_from_identity(obj):
    cls, key = identity_key(instance=obj)
    return u':'.join(unicode(x) for x in key)
