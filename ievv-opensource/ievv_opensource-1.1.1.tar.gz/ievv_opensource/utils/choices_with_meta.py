from collections import OrderedDict


class Choice(object):
    """
    A choice in a :class:`.ChoicesWithMeta`.

    This basic choice class supports value, label and description,
    but you should subclass this (and possibly also :class:`.ChoicesWithMeta`)
    if you need more metadata.

    .. attribute:: value

        The value which is typically stored in the database, or
        sent as the actual POST data value in forms.

    .. attribute:: label

        A short user-friendly label for the choice.

    .. attribute:: description

        A user-friendly longer description of the choice.
    """
    def __init__(self, value, label=None, description=''):
        """
        Args:
            value: The value for the choice.
                The value which is typically stored in the database, or
                sent as the actual POST data value in forms.
            label: A user-friendly short label for the choice.
                This is normally marked for translation.
                Defaults to ``value`` if ``bool(label) == False``.
            description: A user-friendly longer description of the choice.
                This is normally marked for translation.
                Not required.
        """
        self.value = value
        self.label = label or value
        self.description = description

    def get_short_label(self):
        """
        Get a short label for the choice.

        Defaults to returning :attr:`~.Choice.label`, but you
        can override this in subclasses.
        """
        return self.label

    def get_long_label(self):
        """
        Get a long label for the choice.

        Generating by joining :attr:`~.Choice.label` and :attr:`~.Choice.description`
        with ``" - "``.
        """
        if self.description:
            return '{} - {}'.format(self.label, self.description)
        else:
            return self.label

    def __str__(self):
        return self.value


class ChoicesWithMeta(object):
    """
    An object oriented structure for model/form field choices.

    Unlike the simple ``(value, label)`` tuple used in
    Django, this miniframework supports more metadata because
    the choices are defined through :class:`.Choice` (which you can subclass
    and extend).

    Compatible with the ``choices``-attribute used in Django
    (I.E.: django.forms.ChoiceField, django.forms.CharField, ...)
    through the :meth:`~.ChoicesWithMeta.iter_as_django_choices` method.

    Examples:

        Usage in Django model::

            class User(models.Model):
                username = models.CharField(max_length=255, unique=True)

                USERTYPE_ADMIN = 'admin'
                USERTYPE_EDITOR = 'editor'
                USERTYPE_NORMAL = 'normal'

                usertype = models.CharField(
                    choices=choices_with_meta.ChoicesWithMeta(
                        choices_with_meta.Choice(value=USERTYPE_ADMIN, label='Admin'),
                        choices_with_meta.Choice(value=USERTYPE_EDITOR, label='Editor'),
                        choices_with_meta.Choice(value=USERTYPE_NORMAL, label='Normal')
                    )
                )
    """
    def __init__(self, *choices):
        self.choices = OrderedDict()
        for choice in self.get_default_choices():
            self.add(choice)
        for choice in choices:
            self.add(choice)

    def get_by_value(self, value, fallback=None):
        """
        Get the :class:`.Choice` with the provided ``value``.

        Args:
            value: The value to lookup.
            fallback: Fallback value if ``value`` is not registered as a choice value.

        Returns:
            The :class:`.Choice` with matching the value if it exists, otherwise return ``fallback``.
        """
        return self.choices.get(value, fallback)

    def __getitem__(self, value):
        """
        Get the :class:`.Choice` with the provided ``value``.

        Raises:
            KeyError: If ``value`` is not in the ChoicesWithMeta.
        """
        return self.choices[value]

    def __contains__(self, value):
        """
        Check if ``value`` is one of the choices.

        Returns:
            True if ``value`` is one of the choices.
        """
        return value in self.choices

    def __len__(self):
        return len(self.choices)

    def get_default_choices(self):
        """
        Lets say you have a field where a set of default choices
        make sense. You then create a subclass of ChoicesWithMeta
        and override this method to return these default choices.

        Developers can still override this method for special
        cases, but the default will be that these default choices
        are included.

        This is most useful when choices are a Django setting
        that users of your app can override.

        Returns:
            An iterable of :class:`.Choice` objects.
        """
        return []

    def get_choice_at_index(self, index):
        """
        Args:
            index: The numeric index of the choice.

        Raises:
            IndexError: If the index does not correspond to a choice.

        Returns:
            The :class:`.Choice` at the provided index.
        """
        keys = list(self.choices.keys())
        value = keys[index]
        return self.choices[value]

    def get_first_choice(self):
        """
        Uses :meth:`.get_choice_at_index` to get the first (index=0) choice.
        If there is no first choice, ``None`` is returned.
        """
        try:
            return self.get_choice_at_index(0)
        except IndexError:
            return None

    def add(self, choice):
        """
        Add a :class:`.Choice`.

        Args:
            choice: A :class:`.Choice` object.
        """
        if choice.value in self.choices:
            raise KeyError('A choice with value "{}" alredy exists.'.format(choice.value))
        self.choices[choice.value] = choice

    def itervalues(self):
        """
        Iterate over the choices yielding only the values in the added order.
        """
        return self.choices.keys()

    def iterchoices(self):
        """
        Iterate over the choices yielding :class:`.Choice` objects in the added order.
        """
        return iter(self.choices.values())

    def iter_as_django_choices_short(self):
        """
        Iterate over the choices as a Django choices list,
        where each item is a ``(value, label)``-tuple.

        Uses :meth:`.Choice.get_short_label` to create the ``label``.
        """
        for choice in self.iterchoices():
            yield choice.value, choice.get_short_label()

    def iter_as_django_choices_long(self):
        """
        Iterate over the choices as a Django choices list,
        where each item is a ``(value, label)``-tuple.

        Uses :meth:`.Choice.get_long_label` to create the ``label``.
        """
        for choice in self.iterchoices():
            yield choice.value, choice.get_long_label()

    def get_values_as_list(self):
        """
        Get the values of all choices in the added order as a list.
        """
        return list(self.itervalues())

    def get_values_as_commaseparated_string(self):
        """
        Get the values as a comma-separated string.

        Perfect for showing available choices in error messages.

        Returns:
            String with all the values separated by comma.
        """
        return ', '.join(self.itervalues())

    def __str__(self):
        return 'ChoicesWithMeta({})'.format(self.get_values_as_commaseparated_string())
