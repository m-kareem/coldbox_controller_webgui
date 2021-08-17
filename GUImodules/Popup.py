import remi.gui as gui
import logging

logger = logging.getLogger('GUIlogger')

class PopupAlert(gui.VBox):
    def __init__(self, title, message, titleColor='#85C1E9', *args, **kwargs):
        gui.VBox.__init__(self, *args, **kwargs)
        self.css_display = "none"
        self.style['margin'] = 'auto'
        self.style['border'] = '3px solid rgba(0,0,0,.12)'
        self.style['background-color'] = '#D5DBDB'
        self.style['align-items']='center'
        self.style['justify-content']='center'
        self.style['opacity'] = '0.95'


        self.css_outline = "3px solid black"
        lbl_title = gui.Label(title, width=400, height=30, style={'font-weight':'bold'})
        lbl_title.style['background-color'] = titleColor
        self.append(lbl_title)

        self.append(gui.Label(message, width=400, height=50, style={'font-size':'15px'}))

        self.bt_confirm = gui.Button("OK",width=70, height=20, margin='5px',style={'font-size': '14px', 'font-weight': 'bold','background-color': '#5DADE2'})
        self.bt_confirm.onclick.do(self.onconfirm)
        self.append(self.bt_confirm)

    @gui.decorate_event
    def onconfirm(self, emitter):
        self.css_display = "none"
        return ()

    def show(self):
        self.css_position = "absolute"
        self.css_display = "flex"

#-----------------------------------------------------------------
class PopupConfirm(gui.VBox):
    def __init__(self, title, message, *args, **kwargs):
        gui.VBox.__init__(self, *args, **kwargs)
        self.css_display = "none"
        self.style['margin'] = 'auto'
        self.style['border'] = '3px solid rgba(0,0,0,.12)'
        self.style['background-color'] = '#D5DBDB'
        self.style['align-items']='center'
        self.style['justify-content']='center'
        self.style['opacity'] = '0.95'

        hContainer = gui.HBox(width = "100%",hight = "100%",)
        hContainer.style['background-color'] = '#D5DBDB'
        hContainer.style['align-items']='center'
        hContainer.style['justify-content']='center'
        hContainer.style['opacity'] = '0.95'



        self.css_outline = "3px solid black"

        self.append(gui.Label(title, width=400, height=30, style={'font-weight':'bold','background-color': '#85C1E9'}))
        self.append(gui.Label(message, width=400, height=50, style={'font-size':'15px'}))

        self.bt_cancel = gui.Button("Cancel",width=70, height=20, margin='5px',style={'font-size': '14px', 'font-weight': 'bold','background-color': '#5DADE2'})
        self.bt_confirm = gui.Button("Confirm",width=70, height=20, margin='5px',style={'font-size': '14px', 'font-weight': 'bold','background-color': '#5DADE2'})
        self.bt_cancel.onclick.do(self.oncancel)
        self.bt_confirm.onclick.do(self.onconfirm)
        hContainer.append([self.bt_cancel, self.bt_confirm])

        self.append(hContainer)

    @gui.decorate_event
    def onconfirm(self, emitter):
        self.css_display = "none"
        return ()

    def oncancel(self, emitter):
        self.css_display = "none"
        return ()

    def show(self):
        self.css_position = "absolute"
        self.css_display = "flex"
