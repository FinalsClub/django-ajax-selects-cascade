# django-ajax-selects-cascade

Supports the dependence of one AutoCompleteSelectField upon the choice of
another AutoCompleteSelectField.

Requires django-ajax-selects in the Django environment.

It's not very pretty to code yet, but it is functional. Some upstream changes
will need to be made with django-ajax-selects to streamline some of the
ugliness in here.

# Installation

In `settings.py`:
``` python
INSTALLED_APPS = (
   ...
   'ajax_select',
   'ajax_select_cascade',
   ...
```

# Use

Here's an example to choose a phone's make, model, and series.

## RelativeLookupChannel and Channel Decorator

Show how to create Lookups and the convenient channel decorator.

## Forms

        from ajax_select.fields import AutoCompleteSelectField
        from ajax_select.fields import AutoCompleteSelectWidget
        from ajax_select_cascade.fields import AutoCompleteDependentSelectField
        from ajax_select_cascade.fields import AutoCompleteDependentSelectWidget
        
        # Choose phone make from all available phone makes
        class PhoneMakeForm(Form):
            # AutoCompleteSelectField('channel', widget)
            # AutoCompleteSelectWidget('channel', attrs)
            name = AutoCompleteSelectField('ajax_autocomplete_phonemake',
                widget=AutoCompleteSelectWidget(
                    'ajax_autocomplete_phonemake',
                    attrs={
                        # For anyone who cares, I am a make
                        'id': 'dom_autocomplete_phonemake'
                    }
                )
            )
        
        # Choose phone model from the subset of models available for the given make.
        class PhoneModelForm(ModelForm):
            # AutoCompleteDependentSelectField('channel', widget)
            # AutoCompleteDependentSelectWidget('channel', attrs)
            name = AutoCompleteSelectField('ajax_autocomplete_phonemodel',
                widget=AutoCompleteSelectWidget(
                    'ajax_autocomplete_phonemodel',
                    attrs={
                        # For anyone who cares, I am a model
                        'id': 'dom_autocomplete_phonemodel',
                        # My returned data depends on the phone make
                        'data-upstream-id': 'dom_autocomplete_phonemake'
                    }
                )
            )
        
            class Meta:
                model = PhoneModel
        
        # Choose phone series from the subset of series available for the given model.
        class PhoneSeriesForm(ModelForm):
            # AutoCompleteDependentSelectField('channel', widget)
            # AutoCompleteDependentSelectWidget('channel', attrs)
            name = AutoCompleteSelectField('ajax_autocomplete_phoneseries',
                widget=AutoCompleteSelectWidget(
                    'ajax_autocomplete_phoneseries', attrs={
                        # My returned data depends on the phone model
                        'data-upstream-id': 'dom_autocomplete_phonemodel'
                    }
                )
            )
        
            class Meta:
                model = PhoneModel

## Views

Show how to read the data ... although this is sort of up to the end user.
