"""
forms for django-form-utils

Time-stamp: <2009-05-30 13:19:24 carljm forms.py>

"""
from copy import deepcopy

from django import forms
from django.forms.util import flatatt, ErrorDict
from django.utils.safestring import mark_safe

class Fieldset(object):
    """
    An iterable Fieldset with a legend and a set of BoundFields.

    """
    def __init__(self, form, name, boundfields, legend='', description=''):
        self.form = form
        self.boundfields = boundfields
        if legend is None: legend = name
        self.legend = mark_safe(legend)
        self.description = mark_safe(description)
        self.name = name


    def _errors(self):
        return ErrorDict(((k, v) for (k, v) in self.form.errors.iteritems()
                          if k in [f.name for f in self.boundfields]))
    errors = property(_errors)

    def __iter__(self):
        for bf in self.boundfields:
            yield _mark_row_attrs(bf, self.form)

    def __repr__(self):
        return "%s('%s', %s, legend='%s', description='%s')" % (
            self.__class__.__name__, self.name,
            [f.name for f in self.boundfields], self.legend, self.description)

class FieldsetCollection(object):
    def __init__(self, form, fieldsets):
        self.form = form
        self.fieldsets = fieldsets

    def __len__(self):
        return len(self.fieldsets) or 1

    def __iter__(self):
        if not self.fieldsets:
            self.fieldsets = (('main', {'fields': self.form.fields.keys(),
                                        'legend': ''}),)
        for name, options in self.fieldsets:
            try:
                field_names = [n for n in options['fields']
                               if n in self.form.fields]
            except KeyError:
                raise ValueError("Fieldset definition must include 'fields' option." )
            boundfields = [forms.forms.BoundField(self.form, self.form.fields[n], n)
                           for n in field_names]
            yield Fieldset(self.form, name, boundfields,
                           options.get('legend', None),
                           options.get('description', ''))

def _get_meta_attr(attrs, attr, default):
    try:
        ret = getattr(attrs['Meta'], attr)
    except (KeyError, AttributeError):
        ret = default
    return ret
            
def get_fieldsets(bases, attrs):
    """
    Get the fieldsets definition from the inner Meta class.

    """
    fieldsets = _get_meta_attr(attrs, 'fieldsets', None)
    if fieldsets is None:
        #grab the fieldsets from the first base class that has them
        for base in bases:
            fieldsets = getattr(base, 'base_fieldsets', None)
            if fieldsets is not None:
                break
    fieldsets = fieldsets or ()
    # try looping through fieldsets to catch malformed setting early
    try:
        for name, option in fieldsets:
            pass
    except TypeError:
        raise ValueError('"fieldsets" must be an iterable of two-tuples')
    return fieldsets

def get_row_attrs(bases, attrs):
    """
    Get the row_attrs definition from the inner Meta class.

    """
    return _get_meta_attr(attrs, 'row_attrs', {})

def _mark_row_attrs(bf, form):
    row_attrs = deepcopy(form._row_attrs.get(bf.name, {}))
    if bf.field.required:
        req_class = 'required'
    else:
        req_class = 'optional'
    if 'class' in row_attrs:
        row_attrs['class'] = row_attrs['class'] + ' ' + req_class
    else:
        row_attrs['class'] = req_class
    bf.row_attrs = mark_safe(flatatt(row_attrs))
    return bf

class BetterFormBaseMetaclass(type):
    def __new__(cls, name, bases, attrs):
        attrs['base_fieldsets'] = get_fieldsets(bases, attrs)
        attrs['base_row_attrs'] = get_row_attrs(bases, attrs)
        new_class = super(BetterFormBaseMetaclass,
                          cls).__new__(cls, name, bases, attrs)
        return new_class

class BetterFormMetaclass(BetterFormBaseMetaclass,
                            forms.forms.DeclarativeFieldsMetaclass):
    pass

class BetterModelFormMetaclass(BetterFormBaseMetaclass,
                                 forms.models.ModelFormMetaclass):
    pass
    
class BetterBaseForm(object):
    """
    ``BetterForm`` and ``BetterModelForm`` are subclasses of Form
    and ModelForm that allow for declarative definition of fieldsets
    and row_attrs in an inner Meta class.

    The row_attrs declaration is a dictionary mapping field names to
    dictionaries of attribute/value pairs.  The attribute/value
    dictionaries will be flattened into HTML-style attribute/values
    (i.e. {'style': 'display: none'} will become ``style="display:
    none"``), and will be available as the ``row_attrs`` attribute of
    the ``BoundField``.  Also, a CSS class of "required" or "optional"
    will automatically be added to the row_attrs of each
    ``BoundField``, depending on whether the field is required.

    There is no automatic inheritance of ``row_attrs``.
    
    The fieldsets declaration is a list of two-tuples very similar to
    the ``fieldsets`` option on a ModelAdmin class in
    ``django.contrib.admin``.

    The first item in each two-tuple is a name for the fieldset, and
    the second is a dictionary of fieldset options.

    Valid fieldset options in the dictionary include:

    ``fields`` (required): A tuple of field names to display in this
    fieldset.

    ``classes``: A list of extra CSS classes to apply to the fieldset.

    ``legend``: This value, if present, will be the contents of a ``legend``
    tag to open the fieldset.

    ``description``: A string of optional extra text to be displayed
    under the ``legend`` of the fieldset.

    When iterated over, the ``fieldsets`` attribute of a
    ``BetterForm`` (or ``BetterModelForm``) yields ``Fieldset``s.
    Each ``Fieldset`` has a name attribute, a legend attribute, and a
    description attribute, and when iterated over yields its
    ``BoundField``s.

    Subclasses of a ``BetterForm`` will inherit their parent's
    fieldsets unless they define their own.

    A ``BetterForm`` or ``BetterModelForm`` can still be iterated over
    directly to yield all of its ``BoundField``s, regardless of
    fieldsets.

    """
    def __init__(self, *args, **kwargs):
        self._fieldsets = deepcopy(self.base_fieldsets)
        self._row_attrs = deepcopy(self.base_row_attrs)
        super(BetterBaseForm, self).__init__(*args, **kwargs)

    @property
    def fieldsets(self):
        return FieldsetCollection(self, self._fieldsets)

    def __iter__(self):
        for bf in super(BetterBaseForm, self).__iter__():
            yield _mark_row_attrs(bf, self)

class BetterForm(BetterBaseForm, forms.Form):
    __metaclass__ = BetterFormMetaclass
    __doc__ = BetterBaseForm.__doc__

class BetterModelForm(BetterBaseForm, forms.ModelForm):
    __metaclass__ = BetterModelFormMetaclass
    __doc__ = BetterBaseForm.__doc__
    

class BasePreviewForm (object):
    """
    Mixin to add preview functionality to a form.  If the form is submitted with 
    the following k/v pair in its ``data`` dictionary:
        
        'submit': 'preview'    (value string is case insensitive)
    
    Then ``PreviewForm.preview`` will be marked ``True`` and the form will
    be marked invalid (though this invalidation will not put an error in 
    its ``errors`` dictionary).
    
    """
    def __init__(self, *args, **kwargs):
        super(BasePreviewForm, self).__init__(*args, **kwargs)
        self.preview = self.check_preview(kwargs.get('data', None))
    
    def check_preview(self, data):
        if data and data.get('submit', '').lower() == u'preview':
            return True
        return False
    
    def is_valid(self, *args, **kwargs):
        if self.preview:
            return False
        return super(BasePreviewForm, self).is_valid()

class PreviewModelForm(BasePreviewForm, BetterModelForm):
    pass

class PreviewForm(BasePreviewForm, BetterForm):
    pass
