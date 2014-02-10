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
        Pass in upstream_widget the widget this one depends upon.

        The upstream widget must be a subclass of AutoCompleteSelectWidget.
        """
        if not 'upstream_widget' in kwargs:
            raise TypeError('An upstream widget is required.')
        upstream_widget = kwargs.pop('upstream_widget')
        # this check might be overly cautious
        if not isinstance(upstream_widget, AutoCompleteSelectWidget):
            raise TypeError('Cannot operate with upstream fields which do not use some form of AutoCompleteSelectWidget.')
        self.upstream_widget = upstream_widget
        super(AutoCompleteDependentSelectWidget, self).__init__(*args, **kwargs)

    def build_attrs(self, *args, **kwargs):
        """
        Ensures the attrs are updated with data-upstream-id before being rendered.
        """
        attrs = super(AutoCompleteDependentSelectWidget, self).build_attrs(*args, **kwargs)
        key = 'data-upstream-id'
        if key not in attrs:
            # this relies on the upstream widget having been rendered first.
            # ... but the upstream widget is never actually rendered first. X(
            if not hasattr(self.upstream_widget, 'html_id'):
                raise TypeError('Unable to determine upstream HTML id.')
            # update the attrs
            attrs[key] = self.upstream_widget.html_id
        return attrs

class AutoCompleteDependentSelectField(AutoCompleteSelectField):

    def __init__(self, channel, *args, **kwargs):
        """
        Provide the upstream_field kwarg for which this field is dependent upon.
        The upstream field must be an AutoCompleteSelectField or subclass.
        upstream_field may be omitted if a proper widget is supplied.
        """

        # insert the default widget if needed
        widget = kwargs.get("widget", False)
        if not widget or not isinstance(widget, AutoCompleteDependentSelectWidget):
            if not 'upstream_field' in kwargs:
                raise TypeError('Either an AutoCompleteDependentSelectWidget widget or the upstream field must be supplied.')
            upstream_field = kwargs.pop('upstream_field')
            # this check might be overly cautious
            if not isinstance(upstream_field, AutoCompleteSelectField):
                raise TypeError('Cannot operate with a upstream field that is not derived from AutoCompleteSelectField.')
            widget_kwargs = dict(
                channel=channel,
                help_text=kwargs.get('help_text', _(as_default_help)),
                show_help_text=kwargs.pop('show_help_text', True),
                plugin_options=kwargs.pop('plugin_options', {}),
                upstream_widget=upstream_field.widget
            )
            kwargs["widget"] = AutoCompleteDependentSelectWidget(**widget_kwargs)

        super(AutoCompleteDependentSelectField, self).__init__(channel, *args, **kwargs)
