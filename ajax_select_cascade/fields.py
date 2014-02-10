from django.utils.translation import ugettext as _

from ajax_select.fields import _media
from ajax_select.fields import as_default_help
from ajax_select.fields import AutoCompleteSelectWidget
from ajax_select.fields import AutoCompleteSelectField

def _depmedia(self):
    form = _media(self)
    # modify the media in place to include this JS file
    form._js.append('ajax_select_cascade/js/ajax_select_cascade.js')
    return form

class AutoCompleteDependentSelectWidget(AutoCompleteSelectWidget):

    media = property(_depmedia)

    def __init__(self, *args, **kwargs):
        """
        Make sure to pass attrs={'id': 'some_unique_dom_id'} into kwargs
        """
        super(AutoCompleteDependentSelectWidget, self).__init__(*args, **kwargs)

class AutoCompleteDependentSelectField(AutoCompleteSelectField):

    def __init__(self, *args, **kwargs):
        """
        Just like AutoCompleteSelectField, but a widget must be in kwargs.
        """

        widget = kwargs.get("widget", False)
        if not widget:
            raise TypeError('Cannot automatically create an AutoCompleteDependentSelectWidget, please supply one.')
        if not isinstance(widget, AutoCompleteDependentSelectWidget):
            # FYI for now.
            #raise TypeError('The provided widget is almost certainly going to fail.')
            pass

        super(AutoCompleteDependentSelectField, self).__init__(*args, **kwargs)
