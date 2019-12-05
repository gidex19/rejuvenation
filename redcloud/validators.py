
def image_validator(value):
    import os
    from django.core.exceptions import ValidationError
    from django.contrib import messages
    ext = os.path.splitext(value.name)[1]
    valid_ext = ['.jpg']
    if not ext.lower() in valid_ext:
        print('Image selected must be of jpeg format')
        raise ValidationError(u'Image selected must be of jpeg format')


