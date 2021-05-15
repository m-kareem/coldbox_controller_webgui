#!/usr/bin/python3
"""
   REMI library:
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

'''
Configuration file can be specified with option -c filename.conf
Mohammad Kareem, 2020
https://gitlab.cern.ch/mkareem/coldbox_controller_webgui
'''

import remi.gui as gui
from remi import start, App
from GUImodules.RadioButton import *
import GUImodules.Popup as Popup
from threading import Timer
import configparser as conf
import GUImodules.configreader as configreader
from GUImodules.dewPoint import *
import GUImodules.CBChelp as CBChelp
import numpy as np
import os, sys, getopt
import importlib
try:
    from io import StringIO
except:
    from cStringIO import StringIO

import time,datetime

from GUImodules.influx_query import *

#import coldjiglib

#import user_manager
#from user_manager import *

import GUIlogging

import threading



#--------------------------------------------------------------
class ColdBoxGUI(App):
    def __init__(self, *args):

        res_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), './res/')
        super(ColdBoxGUI, self).__init__(*args, static_file_path={'my_res':res_path})

        self.dbClient= influx_init(config_influx)

    def idle(self):
        #idle function called every update cycle (e.g. update_interval=0.1 argument in 'start' function)

        # -- updating the logBox
        if not verbose:
            stdout_string_io.seek(0)
            lines = stdout_string_io.readlines()
            lines.reverse()
            self.stdout_LogBox.set_text("".join(lines))

        # ======== updating tables in TAB 2 with realtime data

        #--- chucks / Modules temperature
        self.table_t.children['row1'].children['col2'].set_text(self.readout_table_t['row1_col2'])
        self.table_t.children['row2'].children['col2'].set_text(self.readout_table_t['row2_col2'])
        self.table_t.children['row3'].children['col2'].set_text(self.readout_table_t['row3_col2'])
        self.table_t.children['row4'].children['col2'].set_text(self.readout_table_t['row4_col2'])

        self.table_t.children['row1'].children['col3'].set_text(self.readout_table_t['row1_col3'])
        self.table_t.children['row2'].children['col3'].set_text(self.readout_table_t['row2_col3'])
        self.table_t.children['row3'].children['col3'].set_text(self.readout_table_t['row3_col3'])
        self.table_t.children['row4'].children['col3'].set_text(self.readout_table_t['row4_col3'])
        if n_chucks==5:
            self.table_t.children['row5'].children['col2'].set_text(self.readout_table_t['row5_col2'])
            self.table_t.children['row5'].children['col3'].set_text(self.readout_table_t['row5_col3'])

        #----------- Ambient data
        self.table_amb.children['row0'].children['col2'].set_text(self.readout_table_amb['row0_col2'])
        self.table_amb.children['row1'].children['col2'].set_text(self.readout_table_amb['row1_col2'])
        self.table_amb.children['row2'].children['col2'].set_text(self.readout_table_amb['row2_col2'])
        self.table_amb.children['row3'].children['col2'].set_text(self.readout_table_amb['row3_col2'])
        self.table_amb.children['row4'].children['col2'].set_text(self.readout_table_amb['row4_col2'])
        self.table_amb.children['row5'].children['col2'].set_text(self.readout_table_amb['row5_col2'])

        #--- current / voltage
        if (plt_field):
            self.table_Plt.children['row1'].children['col2'].set_text(self.readout_table_plt['row1_col2'])
            self.table_Plt.children['row2'].children['col2'].set_text(self.readout_table_plt['row2_col2'])
            self.table_Plt.children['row3'].children['col2'].set_text(self.readout_table_plt['row3_col2'])
            self.table_Plt.children['row4'].children['col2'].set_text(self.readout_table_plt['row4_col2'])

            self.table_Plt.children['row1'].children['col3'].set_text(self.readout_table_plt['row1_col3'])
            self.table_Plt.children['row2'].children['col3'].set_text(self.readout_table_plt['row2_col3'])
            self.table_Plt.children['row3'].children['col3'].set_text(self.readout_table_plt['row3_col3'])
            self.table_Plt.children['row4'].children['col3'].set_text(self.readout_table_plt['row4_col3'])
            if n_chucks==5:
                self.table_Plt.children['row5'].children['col2'].set_text(self.readout_table_plt['row5_col2'])
                self.table_Plt.children['row5'].children['col3'].set_text(self.readout_table_plt['row5_col3'])


    def main(self):
        return ColdBoxGUI.construct_ui(self)


    @staticmethod
    def construct_ui(self):
        # the margin 0px auto centers the main container
        verticalContainer_tb1 = gui.VBox(width = "100%", height=550)
        verticalContainer_tb2 = gui.VBox(width = "100%", height=550)
        verticalContainer_tb3 = gui.VBox(width = "100%", height=550)
        verticalContainer_tb4 = gui.VBox(width = "100%", height=550)

        horizontalContainer_logo = gui.Container(width='20%', layout_orientation=gui.Container.LAYOUT_HORIZONTAL, margin='10px', style={'display': 'block', 'overflow': 'auto'})
        horizontalContainer = gui.HBox(width = "95%")

        horizontalContainer_grafana_dash = gui.HBox(width = "100%")
        horizontalContainer_grafana_dash.style['justify-content'] ='flex-start'
        horizontalContainer_grafana_dash.style['align-items'] = 'flex-start'

        horizontalContainer_grafana_intrl = gui.HBox(width = "100%")
        horizontalContainer_grafana_intrl.style['justify-content'] ='flex-start'
        horizontalContainer_grafana_intrl.style['align-items'] = 'flex-start'

        horizontalContainer_grafana_panels = gui.HBox(width = "100%")
        horizontalContainer_grafana_panels.style['justify-content'] ='flex-start'
        horizontalContainer_grafana_panels.style['align-items'] = 'flex-start'

        #--------------------------InfluxDB -----------------
        self.dbClient = InfluxDBClient(INFLUXDB_ADDRESS, 8086, INFLUXDB_USER, INFLUXDB_PASSWORD, None)

        #--------logo Container ---------------
        self.img_logo = gui.Image('/my_res:ITKlogo.png', width=200, height=67)
        horizontalContainer_logo.append(self.img_logo)


        #============================================= Tab 1 =============================================
        #-------------------------- Left V Container ---------------------
        subContainerLeft = gui.HBox(width = "100%", style={'align-items':'flex-start', 'justify-content':'flex-start'})
        subContainerLeft_1 = gui.VBox(width = "100%", style={'align-items':'flex-start', 'justify-content':'flex-start'})
        subContainerLeft_2 = gui.VBox(width = "100%", style={'align-items':'flex-start', 'justify-content':'flex-start'})
        subContainerLeft_3 = gui.VBox(width = "100%", style={'align-items':'flex-start', 'justify-content':'flex-start'})


        self.lbl_01 = gui.Label('Available chk.', width=100, height=20, margin='20px',style={'font-size': '14px', 'font-weight': 'bold'})
        self.checkBox_ch1 = gui.CheckBoxLabel('Chuck 1', False, width=85, height=20, margin='15px')
        self.checkBox_ch2 = gui.CheckBoxLabel('Chuck 2', False, width=85, height=20, margin='15px')
        self.checkBox_ch3 = gui.CheckBoxLabel('Chuck 3', False, width=85, height=20, margin='15px')
        self.checkBox_ch4 = gui.CheckBoxLabel('Chuck 4', False, width=85, height=20, margin='15px')
        self.list_checkBox_ch = [self.checkBox_ch1,self.checkBox_ch2,self.checkBox_ch3,self.checkBox_ch4]
        if n_chucks ==5:
            self.checkBox_ch5 = gui.CheckBoxLabel('Chuck 5', False, width=85, height=20, margin='15px')
            self.list_checkBox_ch.append(self.checkBox_ch5)

        for checkBox in self.list_checkBox_ch:
            checkBox.onchange.do(self.onchange_checkbox_ch)


        self.lbl_02 = gui.Label('Module Flv.', width=100, height=20, margin='20px',style={'font-size': '14px', 'font-weight': 'bold'})
        self.dropDown_ch1 = gui.DropDown.new_from_list(('LS','SS','R0','R1','R2','R3','R4','R5'), width=60, height=20, margin='15px')
        self.dropDown_ch2 = gui.DropDown.new_from_list(('LS','SS','R0','R1','R2','R3','R4','R5'), width=60, height=20, margin='15px')
        self.dropDown_ch3 = gui.DropDown.new_from_list(('LS','SS','R0','R1','R2','R3','R4','R5'), width=60, height=20, margin='15px')
        self.dropDown_ch4 = gui.DropDown.new_from_list(('LS','SS','R0','R1','R2','R3','R4','R5'), width=60, height=20, margin='15px')
        self.list_dropDown_ch = [self.dropDown_ch1,self.dropDown_ch2,self.dropDown_ch3,self.dropDown_ch4]
        if n_chucks ==5:
            self.dropDown_ch5 = gui.DropDown.new_from_list(('LS','SS','R0','R1','R2','R3','R4','R5'), width=60, height=20, margin='15px')
            self.list_dropDown_ch.append(self.dropDown_ch5)

        for dropDown in self.list_dropDown_ch:
            dropDown.select_by_value('LS')
            dropDown.attributes["disabled"] = ""
            dropDown.style['opacity'] = '0.4' #this is to give a disabled apparence


        self.lbl_03 = gui.Label('Serial #', width=100, height=20, margin='20px',style={'font-size': '14px', 'font-weight': 'bold'})
        self.textinput_ch1 = gui.TextInput(width=130, height=20,margin='15px')
        self.textinput_ch2 = gui.TextInput(width=130, height=20,margin='15px')
        self.textinput_ch3 = gui.TextInput(width=130, height=20,margin='15px')
        self.textinput_ch4 = gui.TextInput(width=130, height=20,margin='15px')
        self.list_textinput_ch = [self.textinput_ch1,self.textinput_ch2,self.textinput_ch3,self.textinput_ch4]
        if n_chucks ==5:
            self.textinput_ch5 = gui.TextInput(width=130, height=20,margin='15px')
            self.list_textinput_ch.append(self.textinput_ch5)

        for textinput in self.list_textinput_ch:
            textinput.set_value('20UXXYY#######')
            textinput.attributes["disabled"] = ""



        subContainerLeft_1.append([self.lbl_01, self.list_checkBox_ch])
        subContainerLeft_2.append([self.lbl_02, self.list_dropDown_ch])
        subContainerLeft_3.append([self.lbl_03, self.list_textinput_ch])

        subContainerLeft_1.style['justify-content'] ='space-around'
        subContainerLeft_1.style['align-items'] = 'flex-start'

        subContainerLeft_2.style['justify-content'] ='space-around'
        subContainerLeft_2.style['align-items'] = 'flex-start'

        subContainerLeft_3.style['justify-content'] ='space-around'
        subContainerLeft_3.style['align-items'] = 'flex-start'

        subContainerLeft.append([subContainerLeft_1,subContainerLeft_2,subContainerLeft_3])
        subContainerLeft.style['justify-content'] ='space-around'
        subContainerLeft.style['align-items'] = 'flex-start'

        #-------------------------- Middle V Container ---------------------
        subContainerMiddle = gui.VBox(width = "100%", style={'align-items':'flex-start', 'justify-content':'space-around'})
        subContainerMiddle_1 = gui.VBox(width = "100%", style={'align-items':'flex-start', 'justify-content':'space-around'})
        self.subContainerMiddle_2 = gui.VBox(width = "100%", style={'align-items':'flex-start', 'justify-content':'space-around'})

        self.lbl_05 = gui.Label('Tests', width=200, height=20, margin='15px',style={'font-size': '15px', 'font-weight': 'bold'})
        self.radioButton_stTest = RadioButtonWithLabel('Standard tests',True, 'groupTests', width=250, height=20, margin='10px')
        self.radioButton_cuTest = RadioButtonWithLabel('Custom tests',False, 'groupTests', width=250, height=20, margin='10px')

        self.checkBox_t1 = gui.CheckBoxLabel('Strobe Delay', False,  height=20, margin='10px',style={'font-size': '15px','display': 'block',  'text-align': 'left'})
        self.checkBox_t2 = gui.CheckBoxLabel('Three Point Gain', False,  height=20, margin='10px',style={'font-size': '15px','display': 'block',  'text-align': 'left'})
        self.checkBox_t3 = gui.CheckBoxLabel('Trim Range', False,  height=20, margin='10px',style={'font-size': '15px','display': 'block',  'text-align': 'left'})
        self.checkBox_t4 = gui.CheckBoxLabel('Three Point Gain part 2', False,  height=20, margin='10px',style={'font-size': '15px','display': 'block',  'text-align': 'left'})
        self.checkBox_t5 = gui.CheckBoxLabel('Response Curve', False,  height=20, margin='10px',style={'font-size': '15px','display': 'block',  'text-align': 'left'})
        self.checkBox_t6 = gui.CheckBoxLabel('Three Point Gain High Stats', False,  height=20, margin='10px',style={'font-size': '15px','display': 'block',  'text-align': 'left'})
        self.checkBox_t7 = gui.CheckBoxLabel('Noise Occupancy', False,  height=20, margin='10px',style={'font-size': '15px','display': 'block',  'text-align': 'left'})
        subContainerMiddle_1.append([self.lbl_05, self.radioButton_stTest, self.radioButton_cuTest])
        self.subContainerMiddle_2.append([self.checkBox_t1,self.checkBox_t2,self.checkBox_t3,self.checkBox_t4,self.checkBox_t5,self.checkBox_t6,self.checkBox_t7])


        self.subContainerMiddle_2.style['pointer-events'] = 'none'
        self.subContainerMiddle_2.style['opacity'] = '0.4' #this is to give a disabled apparence

        subContainerMiddle_1.style['justify-content'] ='space-around'
        subContainerMiddle_1.style['align-items'] = 'flex-start'
        self.subContainerMiddle_2.style['justify-content'] ='space-around'
        self.subContainerMiddle_2.style['align-items'] = 'flex-start'

        self.radioButton_stTest.onchange.do(self.radio_changed)
        self.radioButton_cuTest.onchange.do(self.radio_changed)

        subContainerMiddle.append([subContainerMiddle_1,self.subContainerMiddle_2])

        #-------------------------- Right V Container ---------------------
        # the arguments are	width - height - layoutOrientationOrizontal
        subContainerRight = gui.VBox(width = "100%", style={'align-items':'flex-start', 'justify-content':'flex-start'})
        self.subContainerRight_1 = gui.HBox(width = "100%", style={'align-items':'flex-start', 'justify-content':'flex-start'})
        self.subContainerRight_2 = gui.HBox(width = "100%", style={'align-items':'flex-start', 'justify-content':'flex-start'})
        self.subContainerRight_3 = gui.VBox(width = "100%", style={'align-items':'flex-start', 'justify-content':'flex-start'})

        self.lbl_04 = gui.Label('Controls', width=200, height=30, margin='5px',style={'font-size': '15px', 'font-weight': 'bold'})


        self.btStart = gui.Button('START', width=100, height=30, margin='15px', style={'font-size': '16px', 'font-weight': 'bold','background-color': '#28B463'})
        self.btStart.onclick.do(self.on_btStart_pressed)

        self.btStop = gui.Button('STOP', width=100, height=30, style={'font-size': '16px', 'font-weight': 'bold','background-color': '#C0392B'})
        self.btStop.attributes["disabled"] = ""
        self.btStop.onclick.do(self.on_btStop_pressed)
        self.TC_term_popup_confirm = Popup.PopupConfirm("ColdBox webGUI", "Are you sure you want to terminate the Thermocycling?")
        self.TC_term_popup_alert = Popup.PopupAlert("ColdBox webGUI", "Thermocycling terminated!")


        self.subContainerRight_1.append([self.btStart,self.btStop])
        self.subContainerRight_1.style['justify-content'] ='flex-start'
        self.subContainerRight_1.style['align-items'] = 'center'

        self.lbl_spin = gui.Label('# of cycles', width=100, height=20, margin='15px')
        self.spin = gui.SpinBox(10, 1, 100, width=100, height=20)
        #self.spin.onchange.do(self.on_spin_change)

        self.subContainerRight_2.append([self.lbl_spin,self.spin])
        self.subContainerRight_2.style['justify-content'] ='flex-start'
        self.subContainerRight_2.style['align-items'] = 'center'

        self.lbl_status = gui.Label('Status', height=20, margin='1px', style={'font-size': '15px', 'font-weight': 'bold'})
        self.statusBox = gui.TextInput(False,width=280, height=160)

        self.subContainerRight_3.append([self.lbl_status,self.statusBox])
        subContainerRight.append([self.lbl_04,self.subContainerRight_1 ,self.subContainerRight_2, self.subContainerRight_3])
        self.subContainerRight_3.style['justify-content'] ='space-between'
        self.subContainerRight_3.style['align-items'] = 'flex-start'

        subContainerRight.style['justify-content'] ='space-around'
        subContainerRight.style['align-items'] = 'flex-start'

        #-------------------------- Log Container ---------------------
        # the arguments are	width - height - layoutOrientationOrizontal
        subContainerLog = gui.VBox(width = "100%", style={'align-items':'flex-start', 'justify-content':'flex-start'})
        self.subContainerLog_1 = gui.VBox(width = "100%", style={'align-items':'flex-start', 'justify-content':'flex-start'})

        self.lbl_LogBox = gui.Label('Log', width=200, height=20, margin='1px',style={'font-size': '15px', 'font-weight': 'bold'})
        self.stdout_LogBox = gui.TextInput(False,width=380, height=395, margin='1px')

        self.subContainerLog_1.append([self.lbl_LogBox, self.stdout_LogBox])
        subContainerLog.append(self.subContainerLog_1)

        self.subContainerLog_1.style['justify-content'] ='space-around'
        self.subContainerLog_1.style['align-items'] = 'flex-start'

        #- Wrapping the subcontainers
        horizontalContainer.append([subContainerLeft, subContainerMiddle, subContainerRight, subContainerLog,self.TC_term_popup_alert , self.TC_term_popup_confirm])
        #horizontalContainer.style['justify-content'] ='flex-start'
        #horizontalContainer.style['align-items'] = 'flex-start'
        horizontalContainer.style['justify-content'] ='space-around'
        horizontalContainer.style['align-items'] = 'flex-start'


        verticalContainer_tb1.append([horizontalContainer_logo, horizontalContainer])
        verticalContainer_tb1.style['justify-content'] ='flex-start'
        verticalContainer_tb1.style['align-items'] = 'flex-start'


        #===================================== TAB 2 =================================================

        horizontalContainer_tb2 = gui.HBox(width='70%')

        self.lbl_placeHolder = gui.Label('Place holder content', width=200, height=30, margin='10px',style={'font-size': '15px', 'font-weight': 'bold','color': 'red'})

        #------ Left Container ---------
        subContainerLeft_tb2 = gui.VBox(width='100%')
        self.lbl_temp = gui.Label('Temperature[C]', height=20, margin='10px', style={'font-size': '15px', 'font-weight': 'bold'})


        # Temperatues table
        self.table_t = gui.Table(children={
            'row0': gui.TableRow({'col1':'  #  ', 'col2':'Chuck', 'col3':'Module'}),
            'row1': gui.TableRow({'col1':'1','col2':'', 'col3':''}),
            'row2': gui.TableRow({'col1':'2','col2':'', 'col3':''}),
            'row3': gui.TableRow({'col1':'3','col2':'', 'col3':''}),
            'row4': gui.TableRow({'col1':'4','col2':'', 'col3':''})
            },
            width=250, height=200)
        if n_chucks==5:
            self.table_t.add_child('row5', gui.TableRow({'col1':'5','col2':'', 'col3':''}) )

        subContainerLeft_tb2.append([self.lbl_temp, self.table_t])
        subContainerLeft_tb2.style['justify-content'] ='space-around'
        subContainerLeft_tb2.style['align-items'] = 'flex-start'

        #------ Middle Container ---------

        #subContainerMiddle_tb2 = gui.Container(width=300, layout_orientation=gui.Container.LAYOUT_HORIZONTAL, style={'display': 'block', 'overflow': 'auto', 'text-align': 'left','border':'0px solid black'})
        subContainerMiddle_tb2 = gui.VBox(width='100%')

        if (plt_field):
            self.lbl_peltiers = gui.Label('Peltiers', height=20, margin='10px', style={'font-size': '15px', 'font-weight': 'bold'})
            # Peltiers I/V table
            self.table_Plt = gui.Table(children={
                'row0': gui.TableRow({'col1':'  #  ', 'col2':'Current[mA]', 'col3':'Voltage[V]'}),
                'row1': gui.TableRow({'col1':'1','col2':'', 'col3':''}),
                'row2': gui.TableRow({'col1':'2','col2':'', 'col3':''}),
                'row3': gui.TableRow({'col1':'3','col2':'', 'col3':''}),
                'row4': gui.TableRow({'col1':'4','col2':'', 'col3':''}),
                },
                width=250, height=200)
            if n_chucks==5:
                self.table_Plt.add_child('row5', gui.TableRow({'col1':'5','col2':'', 'col3':''}) )

            subContainerMiddle_tb2.append([self.lbl_peltiers,self.table_Plt])
            subContainerMiddle_tb2.style['justify-content'] ='space-around'
            subContainerMiddle_tb2.style['align-items'] = 'flex-start'

        #------ Right Container ---------
        subContainerRight_tb2 = gui.VBox(width='100%')

        self.lbl_Box = gui.Label('ColdBox Ambient', height=20, margin='10px', style={'font-size': '15px', 'font-weight': 'bold'})

        # Ambient table
        self.table_amb = gui.Table(children={
            'row0': gui.TableRow({'col1':'Relative H[%]', 'col2':''}),
            'row1': gui.TableRow({'col1':'Temperature[C]','col2':''}),
            'row2': gui.TableRow({'col1':'DewPoint[C]','col2':''}),
            'row3': gui.TableRow({'col1':'Flow N2/DryAir[l/s]','col2':''}),
            'row4': gui.TableRow({'col1':'Coolant temperature[C]','col2':''}),
            'row5': gui.TableRow({'col1':'Flow Coolant[l/s]','col2':''})
            },
            width=250, height=200, style={'text-align': 'left'})

        subContainerRight_tb2.append([self.lbl_Box,self.table_amb])
        subContainerRight_tb2.style['justify-content'] ='space-around'
        subContainerRight_tb2.style['align-items'] = 'flex-start'

        horizontalContainer_tb2.append([subContainerLeft_tb2, subContainerMiddle_tb2, subContainerRight_tb2])
        horizontalContainer_tb2.style['justify-content'] ='space-around'
        horizontalContainer_tb2.style['align-items'] = 'center'

        verticalContainer_tb2.append([horizontalContainer_logo, self.lbl_placeHolder, horizontalContainer_tb2])
        verticalContainer_tb2.style['justify-content'] ='space-around'
        verticalContainer_tb2.style['align-items'] = 'center'

        #this flag will be used to stop the display_counter Timer
        self.stop_flag = False


        #===================================== TAB 3 =================================================
        self.lbl_warning = gui.Label('WARNING: thses options are compatible with BNL coldbox type only', width=600, height=30, margin='10px',style={'font-size': '15px', 'font-weight': 'bold','color': 'red'})
        self.data_dict = coldjigcontroller.data_dict
        #------------HV controls-----------
        subContainerADV_HV = gui.GridBox(width = "20%", hight = "100%", style={'margin':'20px auto','align-items':'flex-start', 'justify-content':'flex-start'})
        #subContainerADV_HV.style['border'] = '3px solid rgba(0,0,0,.12)'

        self.lbl_HV = gui.Label('High-Voltage', width=110, height=20, margin='5px',style={'font-size': '14px', 'font-weight': 'bold'})

        self.btHVon = gui.Button('ON', width=75, height=20, margin='5px', style={'font-size': '16px', 'font-weight': 'bold','background-color': '#27AE60'})
        self.btHVoff = gui.Button('OFF', width=75, height=20, margin='5px', style={'font-size': '16px', 'font-weight': 'bold','background-color': '#E74C3C'})

        self.lbl_textinput_HV0 = gui.Label('CH0', width=50, height=20, margin='5px',style={'font-size': '14px'})
        self.lbl_textinput_HV1 = gui.Label('CH1', width=50, height=20, margin='5px',style={'font-size': '14px'})
        self.lbl_textinput_HV2 = gui.Label('CH2', width=50, height=20, margin='5px',style={'font-size': '14px'})
        self.lbl_textinput_HV3 = gui.Label('CH3', width=50, height=20, margin='5px',style={'font-size': '14px'})

        self.textinput_HV0 = gui.TextInput(width=50, height=20,margin='5px')
        self.textinput_HV1 = gui.TextInput(width=50, height=20,margin='5px')
        self.textinput_HV2 = gui.TextInput(width=50, height=20,margin='5px')
        self.textinput_HV3 = gui.TextInput(width=50, height=20,margin='5px')

        self.list_textinput_HV = [self.textinput_HV0, self.textinput_HV1,self.textinput_HV2,self.textinput_HV3]
        for textinput in self.list_textinput_HV:
            textinput.set_value('0.00')

        self.btHVon_1 = gui.Button('ON', width=50, height=20, margin='5px', style={'font-size': '16px', 'font-weight': 'bold','background-color': '#27AE60'})
        self.btHVon_2 = gui.Button('ON', width=50, height=20, margin='5px', style={'font-size': '16px', 'font-weight': 'bold','background-color': '#27AE60'})
        self.btHVon_3 = gui.Button('ON', width=50, height=20, margin='5px', style={'font-size': '16px', 'font-weight': 'bold','background-color': '#27AE60'})
        self.btHVon_0 = gui.Button('ON', width=50, height=20, margin='5px', style={'font-size': '16px', 'font-weight': 'bold','background-color': '#27AE60'})

        self.btHVoff_1 = gui.Button('OFF', width=50, height=20, margin='5px', style={'font-size': '16px', 'font-weight': 'bold','background-color': '#E74C3C'})
        self.btHVoff_2 = gui.Button('OFF', width=50, height=20, margin='5px', style={'font-size': '16px', 'font-weight': 'bold','background-color': '#E74C3C'})
        self.btHVoff_3 = gui.Button('OFF', width=50, height=20, margin='5px', style={'font-size': '16px', 'font-weight': 'bold','background-color': '#E74C3C'})
        self.btHVoff_0 = gui.Button('OFF', width=50, height=20, margin='5px', style={'font-size': '16px', 'font-weight': 'bold','background-color': '#E74C3C'})

        self.btHVset_1 = gui.Button('SET', width=50, height=20, margin='5px', style={'font-size': '16px', 'font-weight': 'bold','background-color': '#6495ED'})
        self.btHVset_2 = gui.Button('SET', width=50, height=20, margin='5px', style={'font-size': '16px', 'font-weight': 'bold','background-color': '#6495ED'})
        self.btHVset_3 = gui.Button('SET', width=50, height=20, margin='5px', style={'font-size': '16px', 'font-weight': 'bold','background-color': '#6495ED'})
        self.btHVset_0 = gui.Button('SET', width=50, height=20, margin='5px', style={'font-size': '16px', 'font-weight': 'bold','background-color': '#6495ED'})


        subContainerADV_HV.set_from_asciiart("""
            |HV_label |HV_label| HV_on  | HV_off   |       | |
            |         |ch0     | ch0_on | ch0_off | textinput_0| set_0 |
            |         |ch1     | ch1_on | ch1_off | textinput_1| set_1 |
            |         |ch2     | ch2_on | ch2_off | textinput_2| set_2 |
            |         |ch3     | ch3_on | ch3_off | textinput_3| set_3 |
            """, 10, 10)

        subContainerADV_HV.append({'HV_label':self.lbl_HV, 'HV_on':self.btHVon ,'HV_off':self.btHVoff,
                                    'ch0':self.lbl_textinput_HV0, 'ch0_on':self.btHVon_0 , 'ch0_off':self.btHVoff_0 ,'textinput_0': self.textinput_HV0, 'set_0':self.btHVset_0 ,
                                    'ch1':self.lbl_textinput_HV1, 'ch1_on':self.btHVon_1 , 'ch1_off':self.btHVoff_1 ,'textinput_1': self.textinput_HV1, 'set_1':self.btHVset_1 ,
                                    'ch2':self.lbl_textinput_HV2, 'ch2_on':self.btHVon_2 , 'ch2_off':self.btHVoff_2 ,'textinput_2': self.textinput_HV2, 'set_2':self.btHVset_2 ,
                                    'ch3':self.lbl_textinput_HV3, 'ch3_on':self.btHVon_3 , 'ch3_off':self.btHVoff_3 ,'textinput_3': self.textinput_HV3, 'set_3':self.btHVset_3
        })

        self.btHVoff.attributes["disabled"] = ""
        self.list_btHV = [self.btHVon_0,self.btHVon_1,self.btHVon_2,self.btHVon_3,self.btHVoff_0,self.btHVoff_1,self.btHVoff_2,self.btHVoff_3]
        self.list_btHVon = [self.btHVon_0,self.btHVon_1,self.btHVon_2,self.btHVon_3]
        self.list_btHVoff = [self.btHVoff_0,self.btHVoff_1,self.btHVoff_2,self.btHVoff_3]
        self.list_btHVset = [self.btHVset_0,self.btHVset_1,self.btHVset_2,self.btHVset_3]

        for bt in self.list_btHVon:
            bt.attributes["disabled"] = ""
        for bt in self.list_btHVoff:
            bt.attributes["disabled"] = ""
        for bt in self.list_btHVset:
            bt.attributes["disabled"] = ""

        self.btHVon.onclick.do(self.on_btHVon_pressed)
        self.btHVoff.onclick.do(self.on_btHVoff_pressed)

        self.list_btHVon[0].onclick.do(self.on_btHVon_0_pressed)
        self.list_btHVon[1].onclick.do(self.on_btHVon_1_pressed)
        self.list_btHVon[2].onclick.do(self.on_btHVon_2_pressed)
        self.list_btHVon[3].onclick.do(self.on_btHVon_3_pressed)

        self.list_btHVoff[0].onclick.do(self.on_btHVoff_0_pressed)
        self.list_btHVoff[1].onclick.do(self.on_btHVoff_1_pressed)
        self.list_btHVoff[2].onclick.do(self.on_btHVoff_2_pressed)
        self.list_btHVoff[3].onclick.do(self.on_btHVoff_3_pressed)

        self.list_btHVset[0].onclick.do(self.on_btHVset_0_pressed)
        self.list_btHVset[1].onclick.do(self.on_btHVset_1_pressed)
        self.list_btHVset[2].onclick.do(self.on_btHVset_2_pressed)
        self.list_btHVset[3].onclick.do(self.on_btHVset_3_pressed)


        #------------LV controls-----------
        subContainerADV_LV1 = gui.GridBox(width = "15%",hight = "100%", style={'margin':'20px auto','align-items':'flex-start', 'justify-content':'flex-start'})
        subContainerADV_LV1.style['border-left'] = '3px solid rgba(0,0,0,.12)'

        self.lbl_LV1 = gui.Label('Low-Voltage 1', width=110, height=20, margin='5px',style={'font-size': '14px', 'font-weight': 'bold'})

        self.btLV1on = gui.Button('ON', width=50, height=20, margin='5px', style={'font-size': '16px', 'font-weight': 'bold','background-color': '#27AE60'})
        self.btLV1off = gui.Button('OFF', width=50, height=20, margin='5px', style={'font-size': '16px', 'font-weight': 'bold','background-color': '#E74C3C'})

        self.lbl_textinput_LV1_0 = gui.Label('CH0', width=50, height=20, margin='5px',style={'font-size': '14px'})
        self.lbl_textinput_LV1_1 = gui.Label('CH1', width=50, height=20, margin='5px',style={'font-size': '14px'})

        self.textinput_LV1_0 = gui.TextInput(width=50, height=20,margin='5px')
        self.textinput_LV1_1 = gui.TextInput(width=50, height=20,margin='5px')

        self.list_textinput_LV1 = [self.textinput_LV1_0,self.textinput_LV1_1]
        for textinput in self.list_textinput_LV1:
            textinput.set_value('0.00')

        self.btLV1set = gui.Button('SET', width=50, height=50, margin='5px', style={'font-size': '16px', 'font-weight': 'bold','background-color': '#6495ED'})


        subContainerADV_LV1.set_from_asciiart("""
            |LV1_label| LV1_label | LV1_on       | LV1_off |
            |         | ch1_1     | textinput1_1 | set_VL1 |
            |         | ch1_2     | textinput1_2 | set_VL1 |
            """, 10, 10)

        subContainerADV_LV1.append({'LV1_label':self.lbl_LV1, 'LV1_on':self.btLV1on ,'LV1_off':self.btLV1off,
                                    'ch1_1':self.lbl_textinput_LV1_0,'textinput1_1': self.textinput_LV1_0,
                                    'ch1_2':self.lbl_textinput_LV1_1,'textinput1_2': self.textinput_LV1_1,
                                    'set_VL1':self.btLV1set
        })

        self.btLV1off.attributes["disabled"] = ""
        self.btLV1on.onclick.do(self.on_btLV1on_pressed)
        self.btLV1off.onclick.do(self.on_btLV1off_pressed)
        self.btLV1set.onclick.do(self.on_btLV1set_pressed)


        subContainerADV_LV2 = gui.GridBox(width = "15%",hight = "100%", style={'margin':'20px auto','align-items':'flex-start', 'justify-content':'flex-start'})
        subContainerADV_LV2.style['border-left'] = '3px solid rgba(0,0,0,.12)'

        self.lbl_LV2 = gui.Label('Low-Voltage 2', width=110, height=20, margin='5px',style={'font-size': '14px', 'font-weight': 'bold'})

        self.btLV2on = gui.Button('ON', width=50, height=20, margin='5px', style={'font-size': '16px', 'font-weight': 'bold','background-color': '#27AE60'})
        self.btLV2off = gui.Button('OFF', width=50, height=20, margin='5px', style={'font-size': '16px', 'font-weight': 'bold','background-color': '#E74C3C'})

        self.lbl_textinput_LV2_0 = gui.Label('CH0', width=50, height=20, margin='5px',style={'font-size': '14px'})
        self.lbl_textinput_LV2_1 = gui.Label('CH1', width=50, height=20, margin='5px',style={'font-size': '14px'})

        self.textinput_LV2_0 = gui.TextInput(width=50, height=20,margin='5px')
        self.textinput_LV2_1 = gui.TextInput(width=50, height=20,margin='5px')

        self.list_textinput_LV2 = [self.textinput_LV2_0,self.textinput_LV2_1]
        for textinput in self.list_textinput_LV2:
            textinput.set_value('0.00')

        self.btLV2set = gui.Button('SET', width=50, height=50, margin='5px', style={'font-size': '16px', 'font-weight': 'bold','background-color': '#6495ED'})




        subContainerADV_LV2.set_from_asciiart("""
            |LV2_label| LV2_label | LV2_on       | LV2_off |
            |         | ch2_1     | textinput1_1 | set_LV2 |
            |         | ch2_2     | textinput1_2 | set_LV2 |
            """, 10, 10)

        subContainerADV_LV2.append({'LV2_label':self.lbl_LV2, 'LV2_on':self.btLV2on ,'LV2_off':self.btLV2off,
                                    'ch2_1':self.lbl_textinput_LV2_0,'textinput1_1': self.textinput_LV2_0,
                                    'ch2_2':self.lbl_textinput_LV2_1,'textinput1_2': self.textinput_LV2_1,
                                    'set_LV2':self.btLV2set
        })
        self.btLV2off.attributes["disabled"] = ""
        self.btLV2on.onclick.do(self.on_btLV2on_pressed)
        self.btLV2off.onclick.do(self.on_btLV2off_pressed)
        self.btLV2set.onclick.do(self.on_btLV2set_pressed)

        #------------Chiller controls-----------
        subContainerADV_Chiller = gui.GridBox(width = "10%",hight = "100%", style={'margin':'20px auto','align-items':'flex-start', 'justify-content':'flex-start'})
        subContainerADV_Chiller.style['border-left'] = '3px solid rgba(0,0,0,.12)'

        self.lbl_Chiller = gui.Label('Chiller', width=110, height=20, margin='5px',style={'font-size': '14px', 'font-weight': 'bold'})

        self.btChillerOn = gui.Button('ON', width=50, height=20, margin='5px', style={'font-size': '16px', 'font-weight': 'bold','background-color': '#27AE60'})
        self.btChillerOff = gui.Button('OFF', width=50, height=20, margin='5px', style={'font-size': '16px', 'font-weight': 'bold','background-color': '#E74C3C'})

        self.lbl_textinput_ChilT = gui.Label('T[C]', width=50, height=20, margin='5px',style={'font-size': '14px'})

        self.textinput_ChilT = gui.TextInput(width=50, height=20,margin='5px')
        self.textinput_ChilT.set_value('0.00')

        self.btChilTset = gui.Button('SET', width=50, height=20, margin='5px', style={'font-size': '16px', 'font-weight': 'bold','background-color': '#6495ED'})

        subContainerADV_Chiller.set_from_asciiart("""
            |Chil_label| Chil_label | Chil_on         | Chil_off |
            |          | Chil_T      | textinput_ChilT | set_ChilT |
            """, 10, 10)

        subContainerADV_Chiller.append({'Chil_label':self.lbl_Chiller, 'Chil_on':self.btChillerOn ,'Chil_off':self.btChillerOff,
                                    'Chil_T':self.lbl_textinput_ChilT,'textinput_ChilT': self.textinput_ChilT,'set_ChilT':self.btChilTset
        })

        self.btChillerOff.attributes["disabled"] = ""
        self.btChillerOn.onclick.do(self.on_btChillerOn_pressed)
        self.btChillerOff.onclick.do(self.on_btChillerOff_pressed)
        self.btChilTset.onclick.do(self.on_btChilTset_pressed)

        '''
        #------------Setting the values -----------
        self.btAdvSet = gui.Button('SET', width="20%", height=30, margin='15px', style={'font-size': '16px', 'font-weight': 'bold','background-color': '#6495ED'})
        self.btAdvSet.onclick.do(self.on_btAdvSet_pressed)
        '''

        subContainerADV = gui.HBox(width = "100%", hight = "100%", style={'align-items':'flex-start', 'justify-content':'space-around'})
        subContainerADV.append([subContainerADV_HV, subContainerADV_LV1, subContainerADV_LV2,subContainerADV_Chiller])
        #subContainerADV.append([subContainerADV_Chiller])

        #- Wrapping the subcontainers
        verticalContainer_tb3.append([horizontalContainer_logo, self.lbl_warning, subContainerADV ])
        verticalContainer_tb3.style['justify-content'] ='space-around'
        verticalContainer_tb3.style['align-items'] = 'center'



        #===================================== TAB 4 =================================================
        self.lbl_swName = gui.Label('ColdBox Controller V 0.5', width=200, height=30, margin='5px',style={'font-size': '15px', 'font-weight': 'bold'})
        self.lbl_coldbox_type = gui.Label('ColdBox type: '+coldbox_type , width=200, height=30, margin='5px')
        verticalContainer_tb4.append([horizontalContainer_logo, self.lbl_swName, self.lbl_coldbox_type])

        #===================================== Wrapping all tabs together =================================================
        tabBox = gui.TabBox(width='100%',style={'align-items':'flex-start', 'justify-content':'flex-start','font-size': '16px', 'font-weight': 'bold','background-color': '#3498DB'})

        tabBox.append(verticalContainer_tb1, 'Control Panel')
        tabBox.add_tab(verticalContainer_tb2, 'Monitoring', None)
        tabBox.add_tab(verticalContainer_tb3, 'Advanced', None)
        tabBox.add_tab(verticalContainer_tb4, 'About', None)

        #===================================== Grafana pannels and interlocks =====================================
        self.grafana_dash = gui.Widget( _type='iframe', width='100%', height=1000, margin='10px')
        self.grafana_dash.attributes['src'] = grf_dash
        self.grafana_dash.attributes['width'] = '100%'
        self.grafana_dash.attributes['height'] = '100%'
        self.grafana_dash.attributes['controls'] = 'true'
        self.grafana_dash.style['border'] = 'none'


        self.grafana_panel_list=[]
        for panel in grf_panel_list:
            self.grafana_panel= gui.Widget( _type='iframe', width=618, height=300, margin='10px')
            self.grafana_panel.attributes['src'] = panel
            self.grafana_panel.attributes['width'] = '100%'
            self.grafana_panel.attributes['height'] = '100%'
            self.grafana_panel.attributes['controls'] = 'true'
            self.grafana_panel.style['border'] = 'none'
            self.grafana_panel_list.append(self.grafana_panel)


        self.grafana_intrl_list=[]
        for intrl in grf_intrl_list:
            self.grafana_inter = gui.Widget( _type='iframe', width=140, height=70, margin='10px')
            self.grafana_inter.attributes['src'] = intrl
            self.grafana_inter.attributes['width'] = '100%'
            self.grafana_inter.attributes['height'] = '100%'
            self.grafana_inter.attributes['controls'] = 'true'
            self.grafana_inter.style['border'] = 'none'
            self.grafana_intrl_list.append(self.grafana_inter)

        horizontalContainer_grafana_intrl.append([self.grafana_intrl_list])
        horizontalContainer_grafana_panels.append([self.grafana_panel_list])

        horizontalContainer_grafana_dash.append(self.grafana_dash)


        #=========================== Appending TabBox and Grafana plots to a vertical main container ======================

        main_container = gui.VBox(width ='100%', hight='100%', style={'align-items':'flex-start', 'justify-content':'flex-start'})
        main_container.append([tabBox, horizontalContainer_grafana_dash, horizontalContainer_grafana_intrl, horizontalContainer_grafana_panels])
        #main_container.append([tabBox, horizontalContainer_grafana_dash])

        #================== Thread management =============================================================================
        self.thread_alive_flag = True
        table_kys1=['row1_col2','row2_col2','row3_col2','row4_col2','row5_col2','row1_col3','row2_col3','row3_col3','row4_col3','row5_col3']
        table_kys2=['row0_col2','row1_col2','row2_col2','row3_col2','row4_col2','row5_col2']
        self.readout_table_t= dict.fromkeys(table_kys1,'None')
        self.readout_table_plt = dict.fromkeys(table_kys1,'None')
        self.readout_table_amb= dict.fromkeys(table_kys2,'None')

        thread_table_t = threading.Thread(target=self.update_table_t)
        thread_table_plt = threading.Thread(target=self.update_table_plt)
        thread_table_amb = threading.Thread(target=self.update_table_amb)
        thread_table_t.start()
        thread_table_plt.start()
        thread_table_amb.start()

        # returning the root widget
        return main_container


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


    def on_btStart_pressed(self, widget):
        currentDT = datetime.datetime.now()
        current_text=self.read_user_options()
        coldjigcontroller.start_thermal_cycle([1,2,3,4,5]) # should get list of available modules. Full list is hardcoded for now.
        logging.info("Thermocycling started!")
        #current_text= self.statusBox.get_text()
        self.statusBox.set_text(current_text+"["+currentDT.strftime("%H:%M:%S")+"] -- Thermocycling started\n")
        self.btStart.attributes["disabled"] = ""
        #-- this is to prevent the user from changing the values when the TC is running
        '''
        for textinput in self.list_textinput_HV:
            textinput.attributes["disabled"] = ""
        for textinput in self.list_textinput_LV1:
            textinput.attributes["disabled"] = ""
        for textinput in self.list_textinput_LV2:
            textinput.attributes["disabled"] = ""
        self.textinput_ChilT.attributes["disabled"] = ""
        '''
        del self.btStop.attributes["disabled"]



    def on_btStop_pressed(self, widget):
        #self.dialog = gui.GenericDialog(title='attempt to stop Thermocycling', message='Are you sure you want to terminate the Thermocycling?', width='500px')
        #self.dialog.show(self)
        self.TC_term_popup_confirm.show()
        self.TC_term_popup_confirm.onconfirm.do(self.Terminate_thermocycling)
        #self.dialog.confirm_dialog.do(self.Terminate_thermocycling)
        #self.TC_term_popup_confirm.onconfirm()




    #--------- Advance buttons ----------
    ###---- HV buttons --------------
    def on_btHVon_pressed(self, widget):
        self.btHVon.attributes["disabled"] = ""
        del self.btHVoff.attributes["disabled"]
        for bt in self.list_btHVon:
            del bt.attributes["disabled"]
        for bt in self.list_btHVset:
            del bt.attributes["disabled"]
        self.data_dict['Caen.state'] = 'ON'
        logging.info("HV set to ON")

    def on_btHVon_0_pressed(self, widget):
        self.list_btHVon[0].attributes["disabled"] = ""
        del self.list_btHVoff[0].attributes["disabled"]
        self.data_dict['Caen.set_channel_0'] = 'ON'
        logging.info("HV ch0 set to ON")


    def on_btHVon_1_pressed(self, widget):
        self.list_btHVon[1].attributes["disabled"] = ""
        del self.list_btHVoff[1].attributes["disabled"]
        self.data_dict['Caen.set_channel_1'] = 'ON'
        logging.info("HV ch1 set to ON")

    def on_btHVon_2_pressed(self, widget):
        self.list_btHVon[2].attributes["disabled"] = ""
        del self.list_btHVoff[2].attributes["disabled"]
        self.data_dict['Caen.set_channel_2'] = 'ON'
        logging.info("HV ch2 set to ON")

    def on_btHVon_3_pressed(self, widget):
        self.list_btHVon[3].attributes["disabled"] = ""
        del self.list_btHVoff[3].attributes["disabled"]
        self.data_dict['Caen.set_channel_3'] = 'ON'
        logging.info("HV ch3 set to ON")

    def on_btHVoff_0_pressed(self, widget):
        self.list_btHVoff[0].attributes["disabled"] = ""
        del self.list_btHVon[0].attributes["disabled"]
        self.data_dict['Caen.set_channel_0'] = 'OFF'
        logging.info("HV ch0 set to OFF")

    def on_btHVoff_1_pressed(self, widget):
        self.list_btHVoff[1].attributes["disabled"] = ""
        del self.list_btHVon[1].attributes["disabled"]
        self.data_dict['Caen.set_channel_1'] = 'OFF'
        logging.info("HV ch1 set to OFF")

    def on_btHVoff_2_pressed(self, widget):
        self.list_btHVoff[2].attributes["disabled"] = ""
        del self.list_btHVon[2].attributes["disabled"]
        self.data_dict['Caen.set_channel_2'] = 'OFF'
        logging.info("HV ch2 set to OFF")

    def on_btHVoff_3_pressed(self, widget):
        self.list_btHVoff[3].attributes["disabled"] = ""
        del self.list_btHVon[3].attributes["disabled"]
        self.data_dict['Caen.set_channel_3'] = 'OFF'
        logging.info("HV ch3 set to OFF")

    def on_btHVoff_pressed(self, widget):
        self.btHVoff.attributes["disabled"] = ""
        del self.btHVon.attributes["disabled"]
        for bt in self.list_btHV:
            bt.attributes["disabled"]= ""
        for bt in self.list_btHVset:
            bt.attributes["disabled"]= ""
        self.data_dict['Caen.state'] = 'OFF'
        logging.info("HV set to OFF")

    def on_btHVset_0_pressed(self, widget):
        HV_val=self.textinput_HV0.get_text()
        self.data_dict['Caen.set_voltge_0'] = HV_val
        logging.info("HV ch0 set to "+HV_val+" V")

    def on_btHVset_1_pressed(self, widget):
        HV_val=self.textinput_HV1.get_text()
        self.data_dict['Caen.set_voltge_1'] = HV_val
        logging.info("HV ch1 set to "+HV_val+" V")

    def on_btHVset_2_pressed(self, widget):
        HV_val=self.textinput_HV2.get_text()
        self.data_dict['Caen.set_voltge_2'] = HV_val
        logging.info("HV ch2 set to "+HV_val+" V")

    def on_btHVset_3_pressed(self, widget):
        HV_val=self.textinput_HV3.get_text()
        self.data_dict['Caen.set_voltge_3'] = HV_val
        logging.info("HV ch3 set to "+HV_val+" V")

    ###---- LV buttons --------------
    def on_btLV1on_pressed(self, widget):
        self.btLV1on.attributes["disabled"] = ""
        del self.btLV1off.attributes["disabled"]
        self.data_dict['LV.State_1'] = 'ON'
        logging.info("LV1 set to ON")


    def on_btLV1off_pressed(self, widget):
        self.btLV1off.attributes["disabled"] = ""
        del self.btLV1on.attributes["disabled"]
        self.data_dict['LV.State_1'] = 'OFF'
        logging.info("LV1 set to OFF")

    def on_btLV1set_pressed(self, widget):
        LV1_0=self.textinput_LV1_0.get_text()
        LV1_1=self.textinput_LV1_1.get_text()

        self.data_dict['LV.set_voltge_1_0'] = LV1_0
        self.data_dict['LV.set_voltge_1_1'] = LV1_1
        logging.info("LV1_0 set to "+LV1_0+" V")
        logging.info("LV1_1 set to "+LV1_1+" V")

    def on_btLV2on_pressed(self, widget):
        self.btLV2on.attributes["disabled"] = ""
        del self.btLV2off.attributes["disabled"]
        self.data_dict['LV.State_2'] = 'ON'
        logging.info("LV2 set to ON")

    def on_btLV2off_pressed(self, widget):
        self.btLV2off.attributes["disabled"] = ""
        del self.btLV2on.attributes["disabled"]
        self.data_dict['LV.State_2'] = 'OFF'
        logging.info("LV2 set to OFF")

    def on_btLV2set_pressed(self, widget):
        LV2_0=self.textinput_LV2_0.get_text()
        LV2_1=self.textinput_LV2_1.get_text()

        self.data_dict['LV.set_voltge_2_0'] = LV2_0
        self.data_dict['LV.set_voltge_2_1'] = LV2_1
        logging.info("LV2_0 set to "+LV2_0+" V")
        logging.info("LV2_1 set to "+LV2_1+" V")

    ###---- Chiller buttons --------------
    def on_btChillerOn_pressed(self, widget):
        self.btChillerOn.attributes["disabled"] = ""
        del self.btChillerOff.attributes["disabled"]
        self.data_dict['chiller.set_state'] = 'ON'
        logging.info("Chiller set to ON")

    def on_btChillerOff_pressed(self, widget):
        self.btChillerOff.attributes["disabled"] = ""
        del self.btChillerOn.attributes["disabled"]
        self.data_dict['chiller.set_state'] = 'OFF'
        logging.info("Chiller set to OFF")

    def on_btChilTset_pressed(self, widget):
        ChillerT=self.textinput_ChilT.get_text()
        self.data_dict['chiller.set_temperature'] = ChillerT
        logging.info("Chiller temperature set to "+ChillerT+" C")

    '''
    def on_btAdvSet_pressed(self, widget):
        self.dialog = gui.GenericDialog(title='Setting HV/LV/Chiller T values', message='Are you sure you want to set new values for HV/LV/Chiller T?', width='500px')
        self.dialog.confirm_dialog.do(self.SetAdvValues)
        self.dialog.show(self)

    def SetAdvValues(self, widget):

        new_ChillerT_value=self.textinput_ChilT.get_text()
        logging.debug("Chiller set to "+new_ChillerT_value+"C")
        #self.list_textinput_HV
        #self.list_textinput_LV
        #----------------------

        data_dict['chiller.set_temperature'] = new_ChillerT_value

        logging.info("NEW HV/LV/Chiller T values are set!!")
        self.notification_message("NEW HV/LV/Chiller T values are set!", "")
        '''
    def Terminate_thermocycling(self, widget):
        currentDT = datetime.datetime.now()
        current_text= self.statusBox.get_text()
        coldjigcontroller.stop_thermal_cycle()
        logging.info("Thermocycling stopped!")
        self.statusBox.set_text(current_text+"["+currentDT.strftime("%H:%M:%S")+"] -- Thermocycling stopped!\n")
        self.btStop.attributes["disabled"] = ""
        del self.btStart.attributes["disabled"]
        #-- this is to let the user to change the values when the TC is stopped
        '''
        for textinput in self.list_textinput_HV:
            del textinput.attributes["disabled"]
        for textinput in self.list_textinput_LV1:
            del textinput.attributes["disabled"]
        for textinput in self.list_textinput_LV2:
            del textinput.attributes["disabled"]

        del self.textinput_ChilT.attributes["disabled"]
        '''
        #self.js_notification('Thermocycling terminated!')
        self.TC_term_popup_alert.show()





    def js_notification(self,txt):
        time.sleep(0.1)
        self.execute_javascript('alert("%s")'%txt)


    def read_user_options(self):
        ncycle = self.spin.get_value()
        availavle_chucks=[]

        for chuck in self.list_checkBox_ch:
            availavle_chucks.append(int(chuck.get_value()) )
        logging.debug('availavle_chucks: '+str(availavle_chucks))

        self.total_selected_chucks = np.sum(list(map(int,availavle_chucks)))
        logging.debug('total_selected_chucks: '+str(self.total_selected_chucks))

        if self.radioButton_stTest.get_value():
            selected_tests = ' standard'
        else:
            selected_tests_helper = [self.checkBox_t1.get_value(),self.checkBox_t2.get_value(),self.checkBox_t3.get_value(),self.checkBox_t4.get_value(),self.checkBox_t5.get_value(),self.checkBox_t6.get_value(),self.checkBox_t7.get_value()]
            selected_tests = str(list(map(int,selected_tests_helper)))
            self.total_selected_tests = np.sum(list(map(int,selected_tests_helper)))
            logging.debug('custom test is running: '+str(self.total_selected_tests)+' tests')

        user_options = 'User options set:\n'+'-Cycles:'+ str(ncycle) +'\n-Available_chucks:'+str(list(map(int,availavle_chucks)))+'\n-Selected_test(s):'+selected_tests+'\n------\n'
        return user_options

    def update_table_t(self):
        while self.thread_alive_flag:
            self.readout_table_t['row1_col2']= str(get_measurement(self.dbClient,INFLUXDB_DATABASE, config_device["ch_device_list"][0],INFLUXDB_MEASUREMENT,'T'))
            self.readout_table_t['row2_col2']= str(get_measurement(self.dbClient,INFLUXDB_DATABASE, config_device["ch_device_list"][1],INFLUXDB_MEASUREMENT,'T'))
            self.readout_table_t['row3_col2']= str(get_measurement(self.dbClient,INFLUXDB_DATABASE, config_device["ch_device_list"][2],INFLUXDB_MEASUREMENT,'T'))
            self.readout_table_t['row4_col2']= str(get_measurement(self.dbClient,INFLUXDB_DATABASE, config_device["ch_device_list"][3],INFLUXDB_MEASUREMENT,'T'))

            self.readout_table_t['row1_col3']= str(get_measurement(self.dbClient,INFLUXDB_DATABASE, config_device["mod_device_list"][0],INFLUXDB_MEASUREMENT,'rH'))
            self.readout_table_t['row2_col3']= str(get_measurement(self.dbClient,INFLUXDB_DATABASE, config_device["mod_device_list"][1],INFLUXDB_MEASUREMENT,'rH'))
            self.readout_table_t['row3_col3']= str(get_measurement(self.dbClient,INFLUXDB_DATABASE, config_device["mod_device_list"][2],INFLUXDB_MEASUREMENT,'rH'))
            self.readout_table_t['row4_col3']= str(get_measurement(self.dbClient,INFLUXDB_DATABASE, config_device["mod_device_list"][3],INFLUXDB_MEASUREMENT,'rH'))
            if n_chucks==5:
                self.readout_table_t['row5_col2']= str(get_measurement(self.dbClient,INFLUXDB_DATABASE, config_device["ch_device_list"][4],INFLUXDB_MEASUREMENT,'T'))
                self.readout_table_t['row5_col3']= str(get_measurement(self.dbClient,INFLUXDB_DATABASE, config_device["mod_device_list"][4],INFLUXDB_MEASUREMENT,'rH'))
            time.sleep(1)

    def update_table_plt(self):
        while self.thread_alive_flag:
            self.readout_table_plt['row1_col2']= str(get_measurement(self.dbClient,INFLUXDB_DATABASE, config_device["pltC_device_list"][0],INFLUXDB_MEASUREMENT,'T'))
            self.readout_table_plt['row2_col2']= str(get_measurement(self.dbClient,INFLUXDB_DATABASE, config_device["pltC_device_list"][1],INFLUXDB_MEASUREMENT,'T'))
            self.readout_table_plt['row3_col2']= str(get_measurement(self.dbClient,INFLUXDB_DATABASE, config_device["pltC_device_list"][2],INFLUXDB_MEASUREMENT,'T'))
            self.readout_table_plt['row4_col2']= str(get_measurement(self.dbClient,INFLUXDB_DATABASE, config_device["pltC_device_list"][3],INFLUXDB_MEASUREMENT,'T'))

            self.readout_table_plt['row1_col3']= str(get_measurement(self.dbClient,INFLUXDB_DATABASE, config_device["pltV_device_list"][0],INFLUXDB_MEASUREMENT,'rH'))
            self.readout_table_plt['row2_col3']= str(get_measurement(self.dbClient,INFLUXDB_DATABASE, config_device["pltV_device_list"][1],INFLUXDB_MEASUREMENT,'rH'))
            self.readout_table_plt['row3_col3']= str(get_measurement(self.dbClient,INFLUXDB_DATABASE, config_device["pltV_device_list"][2],INFLUXDB_MEASUREMENT,'rH'))
            self.readout_table_plt['row4_col3']= str(get_measurement(self.dbClient,INFLUXDB_DATABASE, config_device["pltV_device_list"][3],INFLUXDB_MEASUREMENT,'rH'))
            if n_chucks==5:
                self.readout_table_plt['row5_col2']= str(get_measurement(self.dbClient,INFLUXDB_DATABASE, config_device["pltC_device_list"][4],INFLUXDB_MEASUREMENT,'T'))
                self.readout_table_plt['row5_col3']= str(get_measurement(self.dbClient,INFLUXDB_DATABASE, config_device["pltV_device_list"][4],INFLUXDB_MEASUREMENT,'rH'))
            time.sleep(1)

    def update_table_amb(self):
        while self.thread_alive_flag:
            self.readout_table_amb['row0_col2']= str(get_measurement(self.dbClient, INFLUXDB_DATABASE,config_device["CB_device_rH"],INFLUXDB_MEASUREMENT,'rH'))
            self.readout_table_amb['row1_col2']= str(get_measurement(self.dbClient,INFLUXDB_DATABASE,config_device["CB_device_T"],INFLUXDB_MEASUREMENT,'T'))
            self.readout_table_amb['row2_col2']= str(get_dewpoint(get_measurement(self.dbClient,INFLUXDB_DATABASE,config_device["CB_device_T"],INFLUXDB_MEASUREMENT,'T'), get_measurement(self.dbClient,INFLUXDB_DATABASE,config_device["CB_device_rH"],INFLUXDB_MEASUREMENT,'rH') ))
            self.readout_table_amb['row3_col2']= str(get_measurement(self.dbClient,INFLUXDB_DATABASE,config_device["CB_device_N2flw"],INFLUXDB_MEASUREMENT,'T'))
            self.readout_table_amb['row4_col2']= str(get_measurement(self.dbClient,INFLUXDB_DATABASE,config_device["CB_device_Chiller_T"],INFLUXDB_MEASUREMENT,'T'))
            self.readout_table_amb['row5_col2']= str(get_measurement(self.dbClient,INFLUXDB_DATABASE,config_device["CB_device_Chiller_flw"],INFLUXDB_MEASUREMENT,'T'))
            time.sleep(1)

    def on_close(self):
        self.thread_alive_flag = False
        super(ColdBoxGUI, self).on_close()



if __name__ == "__main__":
    logging = GUIlogging.init_logger(__name__)
    #logging = GUIcoloredlogging.init_logger(__name__)

    logging.info("Starting ColdJig GUI")
    verbose = False # set to Fals if you dont want to print debugging info
    config = conf.ConfigParser()
    configfile = 'default'

    try:
        options, remainder = getopt.getopt(
        sys.argv[1:],
        'c:p:vh',
        ['config=',
         'port=',
         'verbose',
         'help'
         ])
    except getopt.GetoptError as err:
        logging.error('option requires argument.\n Usage: blah -c configFile \n Process terminated.')
        sys.exit(1)

    for opt, arg in options:
        if opt in ('-h', '--help'):
            CBChelp.CBC_help()
            sys.exit(1)
        if opt in ('-c', '--config'):
            configfile = arg
        elif opt in ('-v', '--verbose'):
            verbose = True

    if not any('-c' in sublist for sublist in options):
        #logging.error(bcolors.FAIL + "Attempt to start the GUI without user config.\n Process terminated." + bcolors.ENDC)
        logging.error("Attempt to start the GUI without user config.\n Process terminated.")
        sys.exit(1)

    else:
        if os.path.isfile(configfile):
            config.read(configfile)
        else:
            #logging.error(bcolors.FAIL +'Config file does not exist. Process terminated.' +bcolors.ENDC)
            logging.error('Config file does not exist. Process terminated.')
            sys.exit(1)

    #logging.info(bcolors.OKGREEN+'Reading config file: '+configfile+bcolors.ENDC)
    logging.info('Reading config file: '+configfile)
    config_gui, config_influx, config_device = configreader.read_conf(config)

    # reading config values directly
    #gui_server = config['SERVER']['gui_server']
    #gui_server_port = config['SERVER']['gui_server_port']

    gui_server = config_gui["gui_server"]
    gui_server_port = config_gui["gui_server_port"]
    coldbox_type = config_gui["coldbox_type"]
    n_chucks = config_gui["n_chucks"]
    plt_field = config_gui["plt_field"]
    grf_dash= config_gui["grf_dash"]
    grf_panel_list = config_gui["grf_panel_list"]
    grf_intrl_list = config_gui["grf_intrl_list"]
    gui_debug = config_gui["gui_debug"]
    gui_start_browser = config_gui["gui_start_browser"]
    #gui_logging_level = config_gui["gui_logging_level"]

    INFLUXDB_ADDRESS = config_influx["influx_server"]
    INFLUXDB_USER = config_influx["influx_user"]
    INFLUXDB_PASSWORD = config_influx["influx_pass"]
    INFLUXDB_PORT = config_influx["influx_port"]
    INFLUXDB_DATABASE = config_influx["influx_database"]
    INFLUXDB_MEASUREMENT = config_influx["influx_measurement"]


    gui_multiple_instance = config_gui["gui_multiple_instance"]
    gui_enable_file_cache = config_gui["gui_enable_file_cache"]
    gui_update_interval = config_gui["gui_update_interval"]

    ch_device_list = config_device["ch_device_list"]
    mod_device_list = config_device["mod_device_list"]
    pltC_device_list = config_device["pltC_device_list"]
    pltV_device_list = config_device["pltV_device_list"]
    CB_device_rH = config_device["CB_device_rH"]
    CB_device_T = config_device["CB_device_T"]
    CB_device_N2flw = config_device["CB_device_N2flw"]
    CB_device_Chiller_T = config_device["CB_device_Chiller_T"]
    CB_device_Chiller_flw = config_device["CB_device_Chiller_flw"]


    logging.debug('gui_server= '+gui_server)
    logging.debug('gui_port= '+str(gui_server_port))

    logging.debug('influx_server= '+INFLUXDB_ADDRESS)
    logging.debug('influx_user= '+INFLUXDB_USER)
    logging.debug('influx_port= '+INFLUXDB_PORT)
    logging.debug('influx_database= '+INFLUXDB_DATABASE)
    logging.debug('influx_measurement= '+INFLUXDB_MEASUREMENT)

    logging.debug('coldbox_type= '+coldbox_type)
    logging.debug('n_chucks= '+str(n_chucks))
    logging.debug('plt_fields= '+str(plt_field))
    logging.debug('controller= '+config['COLDBOX']['controller'])

    logging.debug('gui_debug= '+str(gui_debug))
    #logging.debug('gui_logging_level= '+str(gui_logging_level))
    logging.debug('gui_start_browser= '+str(gui_start_browser))
    logging.debug('gui_multiple_instance= '+str(gui_multiple_instance))
    logging.debug('gui_enable_file_cache= '+str(gui_enable_file_cache))
    logging.debug('gui_update_interval= '+str(gui_update_interval))

    logging.debug('CB_device_Chiller_flw= '+CB_device_Chiller_flw)

    logging.debug('ch_device_list='+ str(ch_device_list))
    logging.debug('mod_device_list='+ str(mod_device_list))
    logging.debug('pltC_device_list='+ str(pltC_device_list))
    logging.debug('pltV_device_list='+ str(pltV_device_list))
    logging.debug('grf_dash='+ str(grf_dash))
    #logging.debug('grf_panel_list='+ str(grf_panel_list))
    #logging.debug('grf_intrl_list='+ str(grf_intrl_list))

    #-- checking number of chucks--
    if not (n_chucks==5 or n_chucks==4):
        #logging.error(bcolors.FAIL +'Number of chucks is not supported. Set n_chucks in config file to 4 or 5.' +bcolors.ENDC)
        logging.error('Number of chucks is not supported. Set n_chucks in config file to 4 or 5.')
        sys.exit(1)
    #-----------
    coldjigcontroller = None
    try:
        coldjigcontroller = importlib.import_module(config['COLDBOX']['controller'])
    except ImportError:
        logging.critical('could not import controller library -- check COLDBOX.controller option of config file')
        sys.exit(1)

    if coldjigcontroller is None:
        logging.critical('failed to create an instance of the controller')
        sys.exit(1)

    #-- use this for debugging purpose. The app will exit after loading the configs
    #exit()
    #-----------

    if not verbose:
        stdout_string_io = StringIO()
        sys.stdout = sys.stderr = stdout_string_io

    #--- starts the coldjigcontroller
    if(coldjigcontroller.start()):
        logging.info("Coldbox Controller is up and running!")

    #--starts the webserver / optional parameters
    #start(ColdBoxGUI, update_interval=0.5, debug=gui_debug, address=gui_server, port=gui_server_port, start_browser=gui_start_browser, multiple_instance=gui_multiple_instance, enable_file_cache=gui_enable_file_cache)
    start(ColdBoxGUI, update_interval=gui_update_interval, debug=gui_debug, address=gui_server, port=gui_server_port, start_browser=gui_start_browser, multiple_instance=gui_multiple_instance, enable_file_cache=gui_enable_file_cache, username=None, password=None)
