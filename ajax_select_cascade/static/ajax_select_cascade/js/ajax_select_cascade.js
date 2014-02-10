'use strict';

(function ($) {

  $(window).bind('init-autocompletedep', function () {
    // iterate all dependent inputs with data-upstream-id
    $('input[data-upstream-id]').each(function (i, inp) {
      // find the main input's plugin options
      var id = inp.id.substring(0, inp.id.length-5); // strip off "_text"
      var mainOptions = $('#' + id).data('pluginOptions');
      // find the AJAX endpoint for the jQuery Autocomplete Widget
      var endpoint = mainOptions.source;
      // find the autocomplete input that this one depends upon
      var dependOn = $('#' + $(inp).data('upstreamId') + '_on_deck');

      // change the source function depending upon the last object trigged
      // from the independent field's deck.
      // this will probably do bad things with a AutoCompleteSelectMultiple.
      dependOn.bind('added', function (event, pk, item) {
        $(inp).autocomplete("option", "source", function(request, response) {
          // send an AJAX request to the same place as before
          // include the query term AND the primary key from the deck event.
          $.getJSON(endpoint, {"term": request.term, "upstream": pk}, response);
        });
      });
      // if there are no objects bound, reset the source function.
      dependOn.bind('killed', function(event, pk) {
        $(inp).autocomplete("option", "source", endpoint);
      });
    });
  });

  $(document).ready(function () {
    $(window).trigger('init-autocompletedep');
  }); 

})(window.jQuery);
