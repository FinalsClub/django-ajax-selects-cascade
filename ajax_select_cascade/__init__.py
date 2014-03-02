""" Support Dependent AutoCompleteSelectFields. """
__version__ = "0.1.0"

from uuid import uuid4

from django.conf import settings
from django.http import HttpResponse

from ajax_select import LookupChannel


class DependentLookupChannel(LookupChannel):

    def get_dependent_query(self, query, request, upstream):
        """
        Override this in a subquery. By default, ignores upstream.
        """
        return super(AutoCompleteDependentSelectField, self).get_query(query, request)

    def get_query(self, query, request):
        """
        Extracts the dependency from request and calls self.get_dependent_query.
        The dependency, if not chosen, may be passed on as None.

        Override self.get_dependent_query, not this method.
        """
        # (this chunk is more or less copy pasted from ajax_lookup view)
        # dependency should come in as GET unless global
        # $.ajaxSetup({type:"POST"}) has been set # in which case we'll
        # support POST
        param = 'upstream'
        if request.method == "GET":
            # we could also insist on an ajax request
            if param not in request.GET:
                upstream = None
            else:
                upstream = request.GET[param]
        else:
            if param not in request.POST:
                upstream = None
            else:
                upstream = request.POST[param]
        return self.get_dependent_query(query, request, upstream)

class register_channel_name(object):
    """
    Decorates a LookupChannel class to handle the specified channel_name.
    Example:
    @register_channel_name('ajax_school_channel')
    class SchoolLookup(LookupChannel):
        blah

    will register SchoolLookup to handle 'ajax_school_channel' ajax channel.
    """
    def __init__(self, channel_name):
        self.channel_name = channel_name

    def __call__(self, klass):
        if not hasattr(settings, 'AJAX_LOOKUP_CHANNELS'):
            settings.AJAX_LOOKUP_CHANNELS = {}
        settings.AJAX_LOOKUP_CHANNELS[self.channel_name] = (
            klass.__module__, klass.__name__
        )
        return klass

def generate_dom_id():
    """
    Generates some random, unlikely DOM ID.
    """
    return str(uuid4())

def get_dom_id(field):
    """
    Extract the DOM ID from the widget of the given field.

    render() may take in attrs which override the extracted property. It
    is unclear when this would happen, but if things break, look at how
    the upstream Widget's render() is called in situ.
    """
    dom_id = field.widget.attrs.get('id', None)
    if not dom_id:
        dom_id = generate_dom_id()
        # this bit might be unfriendly. Force the Widget to have an ID.
        field.widget.attrs['id'] = dom_id
    return dom_id
