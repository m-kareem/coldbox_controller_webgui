"""
   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""

import remi.gui as gui
from remi import start, App
from RadioButton import *
from threading import Timer
from dewPoint import *
import numpy as np
import os

import time,datetime
from influx_query import *




#--------------------------------------------------------------
class MyApp(App):
    def __init__(self, *args):
        res_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), './res/')
        super(MyApp, self).__init__(*args, static_file_path={'my_res':res_path})

    def idle(self):
        #idle function called every update cycle

        self.Sens_T_1.set_text('Temperatue[C]: ' + str(get_Temperatur()))
        self.Sens_rH_1.set_text('Relative H%: ' + str(get_rH()))
        self.Sens_DWP.set_text('DewPoint[C]: ' + str(dewpoint_approximation( get_Temperatur(),get_rH() )))


    def main(self):
        return MyApp.construct_ui(self)


    @staticmethod
    def construct_ui(self):
    #def main(self):
        # the margin 0px auto centers the main container
        verticalContainer_tb1 = gui.Container(width=1200, margin='0px auto', style={'display': 'block', 'overflow': 'hidden'})
        verticalContainer_tb2 = gui.Container(width=1200, margin='0px auto', style={'display': 'block', 'overflow': 'hidden'})
        verticalContainer_tb3 = gui.Container(width=1200, margin='0px auto', style={'display': 'block', 'overflow': 'hidden'})
        verticalContainer_tb4 = gui.Container(width=1200, margin='0px auto', style={'display': 'block', 'overflow': 'hidden'})

        horizontalContainer_logo = gui.Container(width='20%', layout_orientation=gui.Container.LAYOUT_HORIZONTAL, margin='10px', style={'display': 'block', 'overflow': 'auto'})
        horizontalContainer = gui.Container(width='100%', layout_orientation=gui.Container.LAYOUT_HORIZONTAL, margin='10px', style={'display': 'block', 'overflow': 'auto'})
        horizontalContainer_grafana = gui.Container(width='100%', layout_orientation=gui.Container.LAYOUT_HORIZONTAL, margin='10px', style={'display': 'block', 'overflow': 'auto'})


        #--------------------------InfluxDB -----------------
        self.dbClient = InfluxDBClient(INFLUXDB_ADDRESS, 8086, INFLUXDB_USER, INFLUXDB_PASSWORD, None)


        #--------logo Container ---------------
        self.img_logo = gui.Image('/my_res:ITKlogo.png', width=200, height=67)
        horizontalContainer_logo.append(self.img_logo)


        #-------------------------- Left V Container ---------------------
        subContainerLeft = gui.Container(width=400, layout_orientation=gui.Container.LAYOUT_HORIZONTAL, style={'display': 'block', 'overflow': 'auto', 'text-align': 'left'})
        subContainerLeft_1 = gui.Container(width=100, style={'display': 'block', 'overflow': 'auto', 'text-align': 'left'})
        subContainerLeft_2 = gui.Container(width=100, style={'display': 'block', 'overflow': 'auto', 'text-align': 'left'})
        subContainerLeft_3 = gui.Container(width=200, style={'display': 'block', 'overflow': 'auto', 'text-align': 'left'})


        self.lbl_01 = gui.Label('Availab chk.', width=200, height=30, margin='5px',style={'font-size': '15px', 'font-weight': 'bold'})
        self.checkBox_ch1 = gui.CheckBoxLabel('Chuck 1', False, width=70, height=20, margin='25px')
        self.checkBox_ch2 = gui.CheckBoxLabel('Chuck 2', False, width=70, height=20, margin='25px')
        self.checkBox_ch3 = gui.CheckBoxLabel('Chuck 3', False, width=70, height=20, margin='25px')
        self.checkBox_ch4 = gui.CheckBoxLabel('Chuck 4', False, width=70, height=20, margin='25px')
        self.checkBox_ch5 = gui.CheckBoxLabel('Chuck 5', False, width=70, height=20, margin='25px')
        self.list_checkBox_ch = [self.checkBox_ch1,self.checkBox_ch2,self.checkBox_ch3,self.checkBox_ch4,self.checkBox_ch5]
        for checkBox in self.list_checkBox_ch:
            checkBox.onchange.do(self.onchange_checkbox_ch)


        self.lbl_02 = gui.Label('Module Flv.', width=200, height=30, margin='5px',style={'font-size': '15px', 'font-weight': 'bold'})
        self.dropDown_ch1 = gui.DropDown.new_from_list(('LS','SS','R0','R1','R2','R3','R4','R5'), width=50, height=20, margin='25px')
        self.dropDown_ch2 = gui.DropDown.new_from_list(('LS','SS','R0','R1','R2','R3','R4','R5'), width=50, height=20, margin='25px')
        self.dropDown_ch3 = gui.DropDown.new_from_list(('LS','SS','R0','R1','R2','R3','R4','R5'), width=50, height=20, margin='25px')
        self.dropDown_ch4 = gui.DropDown.new_from_list(('LS','SS','R0','R1','R2','R3','R4','R5'), width=50, height=20, margin='25px')
        self.dropDown_ch5 = gui.DropDown.new_from_list(('LS','SS','R0','R1','R2','R3','R4','R5'), width=50, height=20, margin='25px')
        self.list_dropDown_ch = [self.dropDown_ch1,self.dropDown_ch2,self.dropDown_ch3,self.dropDown_ch4,self.dropDown_ch5]
        for dropDown in self.list_dropDown_ch:
            dropDown.select_by_value('LS')
            dropDown.attributes["disabled"] = ""
            dropDown.style['opacity'] = '0.4' #this is to give a disabled apparence


        self.lbl_03 = gui.Label('Serial #', width=200, height=30, margin='5px',style={'font-size': '15px', 'font-weight': 'bold'})
        self.textinput_ch1 = gui.TextInput(width=120, height=20,margin='25px')
        self.textinput_ch2 = gui.TextInput(width=120, height=20,margin='25px')
        self.textinput_ch3 = gui.TextInput(width=120, height=20,margin='25px')
        self.textinput_ch4 = gui.TextInput(width=120, height=20,margin='25px')
        self.textinput_ch5 = gui.TextInput(width=120, height=20,margin='25px')
        self.list_textinput_ch = [self.textinput_ch1,self.textinput_ch2,self.textinput_ch3,self.textinput_ch4,self.textinput_ch5]
        for textinput in self.list_textinput_ch:
            textinput.set_value('20UXXYY#######')
            textinput.attributes["disabled"] = ""

        subContainerLeft_1.append([self.lbl_01, self.list_checkBox_ch])
        subContainerLeft_2.append([self.lbl_02, self.list_dropDown_ch])
        subContainerLeft_3.append([self.lbl_03, self.list_textinput_ch])

        subContainerLeft.append([subContainerLeft_1,subContainerLeft_2,subContainerLeft_3])



        #-------------------------- Right V Container ---------------------
        # the arguments are	width - height - layoutOrientationOrizontal
        subContainerRight = gui.Container(width=400, style={'display': 'block', 'overflow': 'auto', 'text-align': 'left'})

        self.subContainerRight_1 = gui.Container(width=400, layout_orientation=gui.Container.LAYOUT_HORIZONTAL, style={'display': 'block', 'overflow': 'auto', 'text-align': 'left'})
        self.subContainerRight_2 = gui.Container(width=400, layout_orientation=gui.Container.LAYOUT_HORIZONTAL, style={'display': 'block', 'overflow': 'auto', 'text-align': 'left'})
        self.subContainerRight_3 = gui.Container(width=400, layout_orientation=gui.Container.LAYOUT_VERTICAL, style={'display': 'block', 'overflow': 'auto', 'text-align': 'left'})

        self.lbl_04 = gui.Label('Controles', width=200, height=30, margin='5px',style={'font-size': '15px', 'font-weight': 'bold'})


        self.btStart = gui.Button('START', width=100, height=30, margin='10px',style={'font-size': '16px', 'font-weight': 'bold','background-color': '#28B463'})
        self.btStart.onclick.do(self.on_btStart_pressed)




        self.btStop = gui.Button('STOP', width=100, height=30, margin='10px',style={'font-size': '16px', 'font-weight': 'bold','background-color': '#C0392B'})
        self.btStop.attributes["disabled"] = ""
        self.btStop.onclick.do(self.on_btStop_pressed)

        self.subContainerRight_1.append([self.btStart,self.btStop])


        self.lbl_spin = gui.Label('# of cycles', width=100, height=20, margin='5px')
        self.spin = gui.SpinBox(10, 1, 100, width=100, height=20, margin='10px')
        self.spin.onchange.do(self.on_spin_change)

        self.subContainerRight_2.append([self.lbl_spin,self.spin])

        self.lbl_status = gui.Label('Status', width=200, height=30, margin='1px',style={'font-size': '15px', 'font-weight': 'bold'})
        self.statusBox = gui.TextInput(False,width=300, height=160, margin='1px')

        self.subContainerRight_3.append([self.lbl_status,self.statusBox])


        self.lbl = gui.Label('This is a LABEL!', width=200, height=30, margin='10px')

        self.bt = gui.Button('Press me!', width=200, height=30, margin='10px')
        # setting the listener for the onclick event of the button
        self.bt.onclick.do(self.on_button_pressed)

        #-------



        self.txt = gui.TextInput(width=200, height=30, margin='10px')
        self.txt.set_text('This is a TEXTAREA')
        self.txt.onchange.do(self.on_text_area_change)



        self.progress = gui.Progress(1, 100, width=200, height=5)

        self.check = gui.CheckBoxLabel('Label checkbox', True, width=200, height=30, margin='10px')
        self.check.onchange.do(self.on_check_change)

        self.btInputDiag = gui.Button('Open InputDialog', width=200, height=30, margin='10px')
        self.btInputDiag.onclick.do(self.open_input_dialog)

        self.btFileDiag = gui.Button('File Selection Dialog', width=200, height=30, margin='10px')
        self.btFileDiag.onclick.do(self.open_fileselection_dialog)

        self.btUploadFile = gui.FileUploader('./', width=200, height=30, margin='10px')
        self.btUploadFile.onsuccess.do(self.fileupload_on_success)
        self.btUploadFile.onfailed.do(self.fileupload_on_failed)

        items = ('One','Two','Thee','Four','Five')
        self.listView = gui.ListView.new_from_list(items, width=300, height=120, margin='10px')
        self.listView.onselection.do(self.list_view_on_selected)

        self.dropDown = gui.DropDown.new_from_list(('DropDownItem 0', 'DropDownItem 1','DropDownItem 2','DropDownItem 3'),
                                                   width=200, height=20, margin='10px')
        self.dropDown.onchange.do(self.drop_down_changed)
        self.dropDown.select_by_value('DropDownItem 0')

        self.slider = gui.Slider(10, 0, 100, 5, width=200, height=20, margin='10px')
        self.slider.onchange.do(self.slider_changed)

        self.colorPicker = gui.ColorPicker('#ffbb00', width=200, height=20, margin='10px')
        self.colorPicker.onchange.do(self.color_picker_changed)

        self.date = gui.Date('2015-04-13', width=200, height=20, margin='10px')
        self.date.onchange.do(self.date_changed)

        self.grafana_plot_01 = gui.Widget( _type='iframe', width=550, height=300, margin='10px')
        self.grafana_plot_01.attributes['src'] = "http://petra.phys.yorku.ca/d-solo/mG6wuGvZk/yorklab-monitoring?orgId=1&refresh=2s&panelId=2"

        self.grafana_plot_01.attributes['width'] = '100%'
        self.grafana_plot_01.attributes['height'] = '100%'
        self.grafana_plot_01.attributes['controls'] = 'true'
        self.grafana_plot_01.style['border'] = 'none'

        self.grafana_plot_02 = gui.Widget( _type='iframe', width=550, height=300, margin='10px')
        self.grafana_plot_02.attributes['src'] = "http://petra.phys.yorku.ca/d-solo/mG6wuGvZk/yorklab-monitoring?orgId=1&refresh=2s&panelId=5"

        self.grafana_plot_02.attributes['width'] = '100%'
        self.grafana_plot_02.attributes['height'] = '100%'
        self.grafana_plot_02.attributes['controls'] = 'true'
        self.grafana_plot_02.style['border'] = 'none'

        self.tree = gui.TreeView(width='100%', height=300)
        ti1 = gui.TreeItem("Item1")
        ti2 = gui.TreeItem("Item2")
        ti3 = gui.TreeItem("Item3")
        subti1 = gui.TreeItem("Sub Item1")
        subti2 = gui.TreeItem("Sub Item2")
        subti3 = gui.TreeItem("Sub Item3")
        subti4 = gui.TreeItem("Sub Item4")
        subsubti1 = gui.TreeItem("Sub Sub Item1")
        subsubti2 = gui.TreeItem("Sub Sub Item2")
        subsubti3 = gui.TreeItem("Sub Sub Item3")
        self.tree.append([ti1, ti2, ti3])
        ti2.append([subti1, subti2, subti3, subti4])
        subti4.append([subsubti1, subsubti2, subsubti3])

        subContainerRight.append([self.lbl_04,self.subContainerRight_1 ,self.subContainerRight_2, self.subContainerRight_3])



        #-------------------------- Middle V Container ---------------------
        subContainerMiddle = gui.Container(width=400, layout_orientation=gui.Container.LAYOUT_HORIZONTAL, style={'display': 'block', 'overflow': 'auto', 'text-align': 'left'})
        subContainerMiddle_1 = gui.Container(width=300, style={'display': 'block', 'overflow': 'auto', 'text-align': 'left'})
        self.subContainerMiddle_2 = gui.Container(width=300, style={'display': 'block', 'overflow': 'auto', 'text-align': 'left','border':'2px solid black'})


        self.lbl_05 = gui.Label('Tests', width=200, height=30, margin='5px',style={'font-size': '15px', 'font-weight': 'bold'})
        self.radioButton_stTest = RadioButtonWithLabel('Standard tests',True, 'groupTests', width=200, height=20, margin='10px')
        self.radioButton_cuTest = RadioButtonWithLabel('Custom tests',False, 'groupTests', width=200, height=20, margin='10px')

        self.checkBox_t1 = gui.CheckBoxLabel('Stobe Delay', False, width=100, height=20, margin='10px',style={'display': 'block', 'overflow': 'auto', 'text-align': 'left'})
        self.checkBox_t2 = gui.CheckBoxLabel('Three Point Gain', False, width=130, height=20, margin='10px',style={'display': 'block', 'overflow': 'auto', 'text-align': 'left'})
        self.checkBox_t3 = gui.CheckBoxLabel('Trimm Range', False, width=110, height=20, margin='10px',style={'display': 'block', 'overflow': 'auto', 'text-align': 'left'})
        self.checkBox_t4 = gui.CheckBoxLabel('Three Point Gain part 2', False, width=180, height=20, margin='10px')
        self.checkBox_t5 = gui.CheckBoxLabel('Response Curve', False, width=130, height=20, margin='10px')
        self.checkBox_t6 = gui.CheckBoxLabel('Three Point Gain High Stats', False, width=210, height=20, margin='10px')
        self.checkBox_t7 = gui.CheckBoxLabel('Noise Occupancy', False, width=140, height=20, margin='10px')

        #subContainerMiddle_1.append([self.lbl_05, self.dropDown_tests])
        subContainerMiddle_1.append([self.lbl_05, self.radioButton_stTest, self.radioButton_cuTest])
        self.subContainerMiddle_2.append([self.checkBox_t1,self.checkBox_t2,self.checkBox_t3,self.checkBox_t4,self.checkBox_t5,self.checkBox_t6,self.checkBox_t7])


        self.subContainerMiddle_2.style['pointer-events'] = 'none'
        self.subContainerMiddle_2.style['opacity'] = '0.4' #this is to give a disabled apparence

        self.radioButton_stTest.onchange.do(self.radio_changed)
        self.radioButton_cuTest.onchange.do(self.radio_changed)

        subContainerMiddle.append([subContainerMiddle_1,self.subContainerMiddle_2])




        #--------------------------- Wrapping the containers -----------------------------------------
        horizontalContainer.append([subContainerLeft, subContainerMiddle, subContainerRight])

        horizontalContainer_grafana.append([self.grafana_plot_01,self.grafana_plot_02])


        #--------------------------- TAB 1 -----------------------------------------
        verticalContainer_tb1.append([horizontalContainer_logo, horizontalContainer,horizontalContainer_grafana])



        #===================================== TAB 2 =================================================
        horizontalContainer_tb2 = gui.Container(width='100%', layout_orientation=gui.Container.LAYOUT_HORIZONTAL, margin='10px', style={'display': 'block', 'overflow': 'auto'})

        #------ Left Container ---------
        subContainerLeft_tb2 = gui.Container(width=400, layout_orientation=gui.Container.LAYOUT_HORIZONTAL, style={'display': 'block', 'overflow': 'auto', 'text-align': 'left'})
        self.lbl_temp = gui.Label('Temperature[C]', width=200, height=30, margin='5px',style={'font-size': '15px', 'font-weight': 'bold'})

        subContainerLeft_tb2.append([self.lbl_temp])

        #------ Middle Container ---------
        subContainerMiddle_tb2 = gui.Container(width=400, layout_orientation=gui.Container.LAYOUT_HORIZONTAL, style={'display': 'block', 'overflow': 'auto', 'text-align': 'left'})
        self.lbl_peltiers = gui.Label('Peltiers', width=200, height=30, margin='5px',style={'font-size': '15px', 'font-weight': 'bold'})

        subContainerMiddle_tb2.append([self.lbl_peltiers])

        #------ Right Container ---------
        subContainerRight_tb2 = gui.Container(width=400, layout_orientation=gui.Container.LAYOUT_HORIZONTAL, style={'display': 'block', 'overflow': 'auto', 'text-align': 'left'})
        self.lbl_Box = gui.Label('ColdBox Ambient', width=200, height=30, margin='5px',style={'font-size': '15px', 'font-weight': 'bold'})

        self.Sens_T_1 = gui.TextInput(width=200, height=30, margin='10px')
        self.Sens_rH_1 = gui.TextInput(width=200, height=30, margin='10px')
        self.Sens_DWP = gui.TextInput(width=200, height=30, margin='10px')


        subContainerRight_tb2.append([self.lbl_Box,self.Sens_T_1,self.Sens_rH_1,self.Sens_DWP])

        horizontalContainer_tb2.append([subContainerLeft_tb2, subContainerMiddle_tb2, subContainerRight_tb2])

        verticalContainer_tb2.append([horizontalContainer_logo, horizontalContainer_tb2, horizontalContainer_grafana])

        #this flag will be used to stop the display_counter Timer
        self.stop_flag = False

        # returning the root widget
        #return verticalContainer_tb1

        #===================================== TAB 3 =================================================
        self.lbl_placeHolder = gui.Label('Place holder content', width=200, height=30, margin='5px',style={'font-size': '15px', 'font-weight': 'bold'})
        verticalContainer_tb3.append([horizontalContainer_logo, self.lbl_placeHolder])


        #===================================== TAB 4 =================================================
        self.lbl_swName = gui.Label('ColdBox Controller V 0.1', width=200, height=30, margin='5px',style={'font-size': '15px', 'font-weight': 'bold'})
        verticalContainer_tb4.append([horizontalContainer_logo, self.lbl_swName])


        #===================================== Wrapping all tabs together =================================================

        tabBox = gui.TabBox(width='40%',style={'font-size': '16px', 'font-weight': 'bold','background-color': '#3498DB'})
        tabBox.append(verticalContainer_tb1, 'Controles')
        tabBox.add_tab(verticalContainer_tb2, 'Monitoring', None)
        tabBox.add_tab(verticalContainer_tb3, 'Advance', None)
        tabBox.add_tab(verticalContainer_tb4, 'About', None)

        return tabBox



    #=============================== SLOT functions =====================================================
    def radio_changed(self, emitter, value):
        if emitter==self.radioButton_cuTest:
            if value:
                del self.subContainerMiddle_2.style['pointer-events']
                del self.subContainerMiddle_2.style['opacity']
        if emitter==self.radioButton_stTest:
            if value:
                self.subContainerMiddle_2.style['pointer-events'] = 'none'
                self.subContainerMiddle_2.style['opacity'] = '0.4' #this is to give a disabled apparence




    def onchange_checkbox_ch(self, emitter, value):
        id=self.list_checkBox_ch.index(emitter)
        if value:
            del self.list_dropDown_ch[id].attributes["disabled"]
            del self.list_textinput_ch[id].attributes["disabled"]
            del self.list_dropDown_ch[id].style['opacity']
        else:
            self.list_dropDown_ch[id].attributes["disabled"] = ""
            self.list_dropDown_ch[id].style['opacity'] = '0.4' #this is to give a disabled apparence
            self.list_textinput_ch[id].attributes["disabled"] = ""



    def read_user_options(self):
        ncycle = self.spin.get_value()
        availavle_chucks = [self.checkBox_ch1.get_value(),self.checkBox_ch2.get_value(),self.checkBox_ch3.get_value(),self.checkBox_ch4.get_value(),self.checkBox_ch5.get_value()]
        self.total_selected_chucks = np.sum(list(map(int,availavle_chucks)))
        #print('total_selected_chucks: '+str(self.total_selected_chucks))

        if self.radioButton_stTest.get_value():
            selected_tests = ' standard'
        else:
            selected_tests_helper = [self.checkBox_t1.get_value(),self.checkBox_t2.get_value(),self.checkBox_t3.get_value(),self.checkBox_t4.get_value(),self.checkBox_t5.get_value(),self.checkBox_t6.get_value(),self.checkBox_t7.get_value()]
            selected_tests = str(list(map(int,selected_tests_helper)))
            self.total_selected_tests = np.sum(list(map(int,selected_tests_helper)))
            #print('custom tests is running: '+str(total_selected_tests)+' tests')

        user_options = 'User options set:\n'+'-Cycles:'+ str(ncycle) +'\n-Available_chucks:'+str(list(map(int,availavle_chucks)))+'\n-Selected_test(s):'+selected_tests+'\n------\n'
        #user_options = 'User options set:\n'+'-Cycles:'+ str(ncycle) +'\n-Available_chucks:'+str(list(map(int,availavle_chucks)))+'\n-Selected_test(s):'+'TEST LIST'+'\n------\n'
        return user_options

    def menu_dialog_clicked(self, widget):
        self.dialog = gui.GenericDialog(title='Dialog Box', message='Click Ok to transfer content to main page', width='500px')
        self.dtextinput = gui.TextInput(width=200, height=30)
        self.dtextinput.set_value('Initial Text')
        self.dialog.add_field_with_label('dtextinput', 'Text Input', self.dtextinput)

        self.dcheck = gui.CheckBox(False, width=200, height=30)
        self.dialog.add_field_with_label('dcheck', 'Label Checkbox', self.dcheck)
        values = ('Danny Young', 'Christine Holand', 'Lars Gordon', 'Roberto Robitaille')
        self.dlistView = gui.ListView.new_from_list(values, width=200, height=120)
        self.dialog.add_field_with_label('dlistView', 'Listview', self.dlistView)

        self.ddropdown = gui.DropDown.new_from_list(('DropDownItem 0', 'DropDownItem 1','DropDownItem 2'), width=200, height=20)
        self.dialog.add_field_with_label('ddropdown', 'Dropdown', self.ddropdown)

        self.dspinbox = gui.SpinBox(min=0, max=5000, width=200, height=20)
        self.dspinbox.set_value(10)
        self.dialog.add_field_with_label('dspinbox', 'Spinbox', self.dspinbox)

        self.dslider = gui.Slider(10, 0, 100, 5, width=200, height=20)
        self.dspinbox.set_value(50)
        self.dialog.add_field_with_label('dslider', 'Slider', self.dslider)

        self.dcolor = gui.ColorPicker(width=200, height=20)
        self.dcolor.set_value('#ffff00')
        self.dialog.add_field_with_label('dcolor', 'Colour Picker', self.dcolor)

        self.ddate = gui.Date(width=200, height=20)
        self.ddate.set_value('2000-01-01')
        self.dialog.add_field_with_label('ddate', 'Date', self.ddate)

        self.dialog.confirm_dialog.do(self.dialog_confirm)
        self.dialog.show(self)

    def dialog_confirm(self, widget):
        result = self.dialog.get_field('dtextinput').get_value()
        self.txt.set_value(result)

        result = self.dialog.get_field('dcheck').get_value()
        self.check.set_value(result)

        result = self.dialog.get_field('ddropdown').get_value()
        self.dropDown.select_by_value(result)

        result = self.dialog.get_field('dspinbox').get_value()
        self.spin.set_value(result)

        result = self.dialog.get_field('dslider').get_value()
        self.slider.set_value(result)

        result = self.dialog.get_field('dcolor').get_value()
        self.colorPicker.set_value(result)

        result = self.dialog.get_field('ddate').get_value()
        self.date.set_value(result)

        result = self.dialog.get_field('dlistView').get_value()
        self.listView.select_by_value(result)

    # listener function
    def on_img_clicked(self, widget):
        self.lbl.set_text('Image clicked!')

    def on_table_row_click(self, table, row, item):
        self.lbl.set_text('Table Item clicked: ' + item.get_text())

    def on_button_pressed(self, widget):
        self.lbl.set_text('Button pressed! ')
        self.bt.set_text('Hi!')

    def on_btStart_pressed(self, widget):
        currentDT = datetime.datetime.now()
        current_text=self.read_user_options()
        print("process started!")
        #current_text= self.statusBox.get_text()
        self.statusBox.set_text(current_text+"["+currentDT.strftime("%H:%M:%S")+"] -- process started\n")
        self.btStart.attributes["disabled"] = ""
        del self.btStop.attributes["disabled"]
        #self.subContainerRight_1.style['pointer-events'] = 'none'
        #self.subContainerRight_1.style['opacity'] = '0.4' #this is to give a disabled apparence


    def on_btStop_pressed(self, widget):
        currentDT = datetime.datetime.now()
        current_text= self.statusBox.get_text()
        self.statusBox.set_text(current_text+"["+currentDT.strftime("%H:%M:%S")+"] -- process stopped!\n")
        self.btStop.attributes["disabled"] = ""
        del self.btStart.attributes["disabled"]
        #del self.subContainerRight_1.style['pointer-events']
        #del self.subContainerRight_1.style['opacity']




    def on_text_area_change(self, widget, newValue):
        self.lbl.set_text('Text Area value changed!')

    def on_spin_change(self, widget, newValue):
        self.lbl.set_text('SpinBox changed, new value: ' + str(newValue))

    def on_check_change(self, widget, newValue):
        self.lbl.set_text('CheckBox changed, new value: ' + str(newValue))

    def open_input_dialog(self, widget):
        self.inputDialog = gui.InputDialog('Input Dialog', 'Your name?',
                                           initial_value='type here',
                                           width=500, height=160)
        self.inputDialog.confirm_value.do(
            self.on_input_dialog_confirm)

        # here is returned the Input Dialog widget, and it will be shown
        self.inputDialog.show(self)

    def on_input_dialog_confirm(self, widget, value):
        self.lbl.set_text('Hello ' + value)

    def open_fileselection_dialog(self, widget):
        self.fileselectionDialog = gui.FileSelectionDialog('File Selection Dialog', 'Select files and folders', False,
                                                           '.')
        self.fileselectionDialog.confirm_value.do(
            self.on_fileselection_dialog_confirm)

        # here is returned the Input Dialog widget, and it will be shown
        self.fileselectionDialog.show(self)

    def on_fileselection_dialog_confirm(self, widget, filelist):
        # a list() of filenames and folders is returned
        self.lbl.set_text('Selected files: %s' % ','.join(filelist))
        if len(filelist):
            f = filelist[0]
            # replace the last download link
            fdownloader = gui.FileDownloader("download selected", f, width=200, height=30)
            self.subContainerRight.append(fdownloader, key='file_downloader')

    def list_view_on_selected(self, widget, selected_item_key):
        """ The selection event of the listView, returns a key of the clicked event.
            You can retrieve the item rapidly
        """
        self.lbl.set_text('List selection: ' + self.listView.children[selected_item_key].get_text())

    def drop_down_changed(self, widget, value):
        self.lbl.set_text('New Combo value: ' + value)

    def slider_changed(self, widget, value):
        self.lbl.set_text('New slider value: ' + str(value))

    def color_picker_changed(self, widget, value):
        self.lbl.set_text('New color value: ' + value)

    def date_changed(self, widget, value):
        self.lbl.set_text('New date value: ' + value)

    def menu_save_clicked(self, widget):
        self.lbl.set_text('Menu clicked: Save')

    def menu_saveas_clicked(self, widget):
        self.lbl.set_text('Menu clicked: Save As')

    def menu_open_clicked(self, widget):
        self.lbl.set_text('Menu clicked: Open')

    def menu_view_clicked(self, widget):
        self.lbl.set_text('Menu clicked: View')

    def fileupload_on_success(self, widget, filename):
        self.lbl.set_text('File upload success: ' + filename)

    def fileupload_on_failed(self, widget, filename):
        self.lbl.set_text('File upload failed: ' + filename)

    def on_close(self):
        """ Overloading App.on_close event to stop the Timer.
        """
        self.stop_flag = True
        super(MyApp, self).on_close()


if __name__ == "__main__":
    # starts the webserver
    # optional parameters
    # start(MyApp,address='127.0.0.1', port=8081, multiple_instance=False,enable_file_cache=True, update_interval=0.1, start_browser=True)
    start(MyApp, debug=False, address='localhost', port=5000, start_browser=True, multiple_instance=True, enable_file_cache=True)
