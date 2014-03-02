from django.utils.translation import ugettext as _

from ajax_select.fields import _media
from ajax_select.fields import as_default_help
from ajax_select.fields import AutoCompleteSelectWidget
from ajax_select.fields import AutoCompleteSelectField

from __init__ import get_dom_id

def _depmedia(self):
    form = _media(self)
    # modify the media in place to include this JS file
    form._js.append('ajax_select_cascade/js/ajax_select_cascade.js')
    return form

class AutoCompleteDependentSelectWidget(AutoCompleteSelectWidget):

    media = property(_depmedia)

class AutoCompleteDependentSelectField(AutoCompleteSelectField):

    def __init__(self, channel, *args, **kwargs):
        """
        To select the upstream widget: provide the widget, or provide one of
        two optional kwargs:
          dependsOn   - the AutoCompleteSelectField this Field depends on
          upstream_id - the DOM ID of an AutoCompleteSelectField this field
                        depends on

        If multiple options are given, preference is given to widget, then
        dependsOn, then upstream_id.

        An optional kwarg 'widget_id' may be passed to specify the DOM ID of a
        newly created widget, if this field needs a newly created widget. It
        passes this id through to `attrs['id']` of the Widget.
        """

        # insert the default widget if needed
        widget = kwargs.get("widget", False)
        if widget:
            # Check to see if ambiguous kwargs were passed that aren't needed.
            if 'dependsOn' in kwargs:
                del kwargs['dependsOn']
            if 'upstream_id' in kwargs:
                del kwargs['upstream_id']
            if 'widget_id' in kwargs:
                # maybe we could dynamically rename the widget? (seems bad)
                # or maybe we should fire an exception or log an error?
                del kwargs['widget_id']
        elif not 'dependsOn' in kwargs and 'upstream_id' not in kwargs:
                raise TypeError('You must supply a widget, dependsOn kwarg, or upstream_id kwarg')

        if not widget and 'dependsOn' in kwargs:
            # Find the given field's DOM ID, overriding any DOM ID passed in.
            kwargs['upstream_id'] = get_dom_id(kwargs.pop('dependsOn'))

        if not widget and 'upstream_id' in kwargs:
            # Create the widget pointing at the correct upstream DOM ID.
            attrs = {}
            if 'widget_id' in kwargs:
                attrs['id'] = kwargs.pop('widget_id')
            attrs['data-upstream-id'] = kwargs.pop('upstream_id')
            widget_kwargs = dict(
                channel=channel,
                help_text=kwargs.get('help_text', _(as_default_help)),
                show_help_text=kwargs.pop('show_help_text', True),
                plugin_options=kwargs.pop('plugin_options', {}),
                attrs=attrs,
            )
            kwargs["widget"] = AutoCompleteDependentSelectWidget(**widget_kwargs)

        # Widget should exist now.
        # kwargs should be scrubbed of arguments from this method.
        # Pass it all along to the super()
        super(AutoCompleteDependentSelectField, self).__init__(channel, *args, **kwargs)
