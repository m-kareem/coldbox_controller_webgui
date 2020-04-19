from remi import gui

class LabelForInputs(gui.Widget, gui._MixinTextualWidget):
    """ Non editable text label widget. Specifically designed to be used in conjunction with checkboxes and radiobuttons
    """

    def __init__(self, text, widget_for_instance, *args, **kwargs):
        """
        Args:
            text (str): The string content that have to be displayed in the Label.
            widget_for_instance (gui.Widget): checkbox or radiobutton instance
            kwargs: See Container.__init__()
        """
        super(LabelForInputs, self).__init__(*args, **kwargs)
        self.type = 'label'
        self.attributes['for'] = widget_for_instance.identifier
        self.set_text(text)

class InputCheckable(gui.Input):
    """It is the base class for checkable widgets (Switch, RadioButton, Checkbox).
        Checkable are the widgets that contains attribute 'checked' to determine the status
        The developer has to pass the the argument _type to the constructor
         to determine the kind of widget.
    """

    def __init__(self, status_on=False, input_type='checkbox', *args, **kwargs):
        """
        Args:
            status_on (bool):
            kwargs: See Widget.__init__()
        """
        super(InputCheckable, self).__init__(input_type, *args, **kwargs)
        self.set_value(status_on)
        self.attributes[gui.Widget.EVENT_ONCHANGE] = \
            "var params={};params['value']=document.getElementById('%(emitter_identifier)s').checked;" \
            "sendCallbackParam('%(emitter_identifier)s','%(event_name)s',params);" % \
            {'emitter_identifier': str(self.identifier), 'event_name': gui.Widget.EVENT_ONCHANGE}

    @gui.decorate_event
    def onchange(self, value):
        value = value in ('True', 'true')
        self.set_value(value)
        self._set_updated()
        return (value,)

    def set_value(self, status_on):
        if status_on:
            self.attributes['checked'] = 'checked'
        else:
            if 'checked' in self.attributes:
                del self.attributes['checked']

    def get_value(self):
        """
        Returns:
            bool:
        """
        return 'checked' in self.attributes



class RadioButton(InputCheckable):
    """RadioButton widget, useful for exclusive selection.
        different radiobuttons have to be assigned to the
        same group name in order to switch exclusively.
    """

    @property
    def attr_name(self):
        return self.attributes.get('name', '')

    @attr_name.setter
    def attr_name(self, value):
        self.attributes['name'] = str(value)

    def __init__(self, status_on=False, group='group', *args, **kwargs):
        """
        Args:
            status_on (bool): the initial value
            group (str): the group name. RadioButtons with same group will be exclusively activated
            kwargs: See Widget.__init__()
        """
        super(RadioButton, self).__init__(status_on, input_type='radio', *args, **kwargs)
        self.attr_name = group

    def set_value(self, status_on):
        InputCheckable.set_value(self, status_on)

        # if on and has a parent, all other radios with same group name are switched off
        if status_on and self.get_parent():
            for w in self.get_parent().children.values():
                if isinstance(w, type(self)):
                    if w.identifier != self.identifier:
                        if w.get_group() == self.get_group():
                            w.set_value(False)

    def set_group(self, group_name):
        self.attr_name = group_name

    def get_group(self):
        return self.attr_name

class RadioButtonWithLabel(gui.Container):
    _radio = None
    _label = None

    @property
    def text(self):
        return self._label.get_text()

    @text.setter
    def text(self, value):
        self._label.set_text(value)

    @property
    def attr_name(self):
        return self._radio.attr_name

    @attr_name.setter
    def attr_name(self, value):
        self._radio.attr_name = str(value)

    def __init__(self, text='radiobutton', status_on=False, group='group', *args, **kwargs):
        """
        Args:
            text (str): the text label
            status_on (bool): the initial value
            group (str): the group name. RadioButtons with same group will be exclusively activated
            kwargs: See Widget.__init__()
        """
        super(RadioButtonWithLabel, self).__init__(*args, **kwargs)

        self._radio = RadioButton(status_on, group=group)
        self.append(self._radio, key='radio')

        self._label = LabelForInputs(text, self._radio)
        self.append(self._label, key='label')

        self._radio.onchange.connect(self.onchange)

    @gui.decorate_event
    def onchange(self, widget, value):
        self.__update_other_radios()
        return (value,)

    def get_text(self):
        return self._label.text

    def set_text(self, text):
        self._label.text = text

    def set_group(self, group_name):
        self.attr_name = group_name

    def get_group(self):
        return self.attr_name

    def get_value(self):
        return self._radio.get_value()

    def set_value(self, value):
        """ Args:
                value (bool): defines the checked status for the radio button
        """
        self._radio.set_value(value)
        self.__update_other_radios()

    def __update_other_radios(self):
        # if on and has a parent,
        # all other radios, in the same container,
        # with same group name are switched off
        if self.get_value() and self.get_parent():
            for w in self.get_parent().children.values():
                if isinstance(w, type(self)):
                    if w.identifier != self.identifier:
                        if w.get_group() == self.get_group():
                            w.set_value(False)
