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
Read the form data as per usual Django methods.

## RelativeLookupChannel and Channel Decorator

I would put these into the models file, but it is flexible.

        from ajax_select import LookupChannel
        from ajax_select_cascade import DependentLookupChannel
        from ajax_select_cascade import register_channel_name

        # Channel name corresponds to channel used by AutoCompleteSelectField.
        @register_channel_name('ajax_autocomplete_phonemake')
        def MakeLookup(LookupChannel):
            # PhoneMake is a Django Model defined somewhere.
            # It has a name field.
            model = PhoneMake

            def get_query(self, q, request):
                # Filter the query against PhoneMake.name
                return self.model.objects.filter(name=q)

        @register_channel_name('ajax_autocomplete_phonemodel')
        def ModelGivenMakeLookup(DependentLookupChannel):
            # PhoneModel is a Django Model defined somewhere.
            # It has a name field and a ForeignKey to PhoneMake called make.
            model = PhoneModel

            def get_dependent_query(self, q, request, dependency):
                # Filter the query against PhoneModel.name
                # after filtering the dependency against PhoneMake.
                return self.model.objects.filter(make__id=dependency, name=q)

        @register_channel_name('ajax_autocomplete_phoneseries')
        def SeriesGivenModelLookup(DependentLookupChannel):
            # PhoneSeries is a Django Model defined somewhere.
            # It has a name field and a ForeignKey to PhoneModel called model.
            model = PhoneSeries

            def get_dependent_query(self, q, request, dependency):
                # Filter the query against PhoneSeries.name
                # after filtering the dependency against PhoneModel.
                return self.model.objects.filter(model__id=dependency, name=q)

## Forms

        from ajax_select.fields import AutoCompleteSelectField
        from ajax_select_cascade.fields import AutoCompleteDependentSelectField

        # Choose phone make from all available phone makes
        class PhoneMakeForm(Form):
            # AutoCompleteSelectField('channel')
            name = AutoCompleteSelectField('ajax_autocomplete_phonemake')

        # Choose phone model from the subset of models available for the given
        # make.
        class PhoneModelForm(ModelForm):
            # AutoCompleteDependentSelectField('channel', kwargs)
            name = AutoCompleteSelectField('ajax_autocomplete_phonemodel',
                                           dependsOn=PhoneMakeForm.name)

        # Choose phone series from the subset of series available for the given
        # model.
        class PhoneSeriesForm(ModelForm):
            # AutoCompleteDependentSelectField('channel', kwargs)
            name = AutoCompleteSelectField('ajax_autocomplete_phoneseries',
                                           dependsOn=PhoneModelForm.name)

## Forms (long hand)

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
        
        # Choose phone model from the subset of models available for the given
        # make.
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
        
        # Choose phone series from the subset of series available for the given
        # model.
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
