from django.apps import AppConfig

class ClinicConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'clinic'

    def ready(self):
        from django import forms
        original_init = forms.Field.__init__
        def new_init(self, *args, **kwargs):
            original_init(self, *args, **kwargs)
            if hasattr(self, 'widget'):
                css = self.widget.attrs.get('class', '')
                if 'form-control' not in css and 'form-select' not in css:
                    if isinstance(self.widget, (forms.Select, forms.SelectMultiple)):
                        self.widget.attrs['class'] = css + ' form-select'
                    else:
                        self.widget.attrs['class'] = css + ' form-control'
        forms.Field.__init__ = new_init