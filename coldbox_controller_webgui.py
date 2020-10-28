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
from RadioButton import *
from threading import Timer
import configparser as conf
import modules.configreader as configreader
from modules.dewPoint import *
import modules.CBChelp as CBChelp
import numpy as np
import os, sys, getopt
try:
    from io import StringIO
except:
    from cStringIO import StringIO

import time,datetime

from modules.influx_query import *

#import user_manager
#from user_manager import *

#import modules.GUIlogger as GUIlogger
import modules.GUIcoloredlogs as GUIlogger
#from  modules.bcolors import bcolors

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
    #def main(self):
        # the margin 0px auto centers the main container
        verticalContainer_tb1 = gui.Container(width=1400, margin='0px auto', style={'display': 'block', 'overflow': 'hidden'})
        verticalContainer_tb2 = gui.Container(width=1500, margin='0px auto', style={'display': 'block', 'overflow': 'hidden'})
        verticalContainer_tb3 = gui.Container(width=1500, margin='0px auto', style={'display': 'block', 'overflow': 'hidden'})
        verticalContainer_tb4 = gui.Container(width=1500, margin='0px auto', style={'display': 'block', 'overflow': 'hidden'})

        horizontalContainer_logo = gui.Container(width='20%', layout_orientation=gui.Container.LAYOUT_HORIZONTAL, margin='10px', style={'display': 'block', 'overflow': 'auto'})
        horizontalContainer = gui.Container(width='100%', layout_orientation=gui.Container.LAYOUT_HORIZONTAL, margin='10px', style={'display': 'block', 'overflow': 'auto'})
        horizontalContainer_grafana_panels = gui.Container(width='100%', layout_orientation=gui.Container.LAYOUT_HORIZONTAL, margin='10px', style={'display': 'block', 'overflow': 'auto'})
        horizontalContainer_grafana_intrl = gui.Container(width='100%', layout_orientation=gui.Container.LAYOUT_HORIZONTAL, margin='10px', style={'display': 'block', 'overflow': 'auto'})


        #--------------------------InfluxDB -----------------
        self.dbClient = InfluxDBClient(INFLUXDB_ADDRESS, 8086, INFLUXDB_USER, INFLUXDB_PASSWORD, None)


        #--------logo Container ---------------
        self.img_logo = gui.Image('/my_res:ITKlogo.png', width=200, height=67)
        horizontalContainer_logo.append(self.img_logo)


        #-------------------------- Left V Container ---------------------
        subContainerLeft = gui.Container(width=420, layout_orientation=gui.Container.LAYOUT_HORIZONTAL, style={'display': 'block', 'overflow': 'auto', 'text-align': 'left'})
        subContainerLeft_1 = gui.Container(width=110, layout_orientation=gui.Container.LAYOUT_HORIZONTAL, style={'display': 'block', 'overflow': 'auto', 'text-align': 'left'})
        subContainerLeft_2 = gui.Container(width=110, layout_orientation=gui.Container.LAYOUT_HORIZONTAL, style={'display': 'block', 'overflow': 'auto', 'text-align': 'left'})
        subContainerLeft_3 = gui.Container(width=200, layout_orientation=gui.Container.LAYOUT_HORIZONTAL, style={'display': 'block', 'overflow': 'auto', 'text-align': 'left'})


        self.lbl_01 = gui.Label('Available chk.', width=250, height=20, margin='20px',style={'font-size': '13px', 'font-weight': 'bold'})
        self.checkBox_ch1 = gui.CheckBoxLabel('Chuck 1', False, width=80, height=20, margin='15px')
        self.checkBox_ch2 = gui.CheckBoxLabel('Chuck 2', False, width=80, height=20, margin='15px')
        self.checkBox_ch3 = gui.CheckBoxLabel('Chuck 3', False, width=80, height=20, margin='15px')
        self.checkBox_ch4 = gui.CheckBoxLabel('Chuck 4', False, width=80, height=20, margin='15px')
        self.list_checkBox_ch = [self.checkBox_ch1,self.checkBox_ch2,self.checkBox_ch3,self.checkBox_ch4]
        if n_chucks ==5:
            self.checkBox_ch5 = gui.CheckBoxLabel('Chuck 5', False, width=80, height=20, margin='15px')
            self.list_checkBox_ch.append(self.checkBox_ch5)

        for checkBox in self.list_checkBox_ch:
            checkBox.onchange.do(self.onchange_checkbox_ch)


        self.lbl_02 = gui.Label('Module Flv.', width=230, height=20, margin='20px',style={'font-size': '13px', 'font-weight': 'bold'})
        self.dropDown_ch1 = gui.DropDown.new_from_list(('LS','SS','R0','R1','R2','R3','R4','R5'), width=50, height=20, margin='15px')
        self.dropDown_ch2 = gui.DropDown.new_from_list(('LS','SS','R0','R1','R2','R3','R4','R5'), width=50, height=20, margin='15px')
        self.dropDown_ch3 = gui.DropDown.new_from_list(('LS','SS','R0','R1','R2','R3','R4','R5'), width=50, height=20, margin='15px')
        self.dropDown_ch4 = gui.DropDown.new_from_list(('LS','SS','R0','R1','R2','R3','R4','R5'), width=50, height=20, margin='15px')
        self.list_dropDown_ch = [self.dropDown_ch1,self.dropDown_ch2,self.dropDown_ch3,self.dropDown_ch4]
        if n_chucks ==5:
            self.dropDown_ch5 = gui.DropDown.new_from_list(('LS','SS','R0','R1','R2','R3','R4','R5'), width=50, height=20, margin='15px')
            self.list_dropDown_ch.append(self.dropDown_ch5)

        for dropDown in self.list_dropDown_ch:
            dropDown.select_by_value('LS')
            dropDown.attributes["disabled"] = ""
            dropDown.style['opacity'] = '0.4' #this is to give a disabled apparence


        self.lbl_03 = gui.Label('Serial #', width=200, height=20, margin='20px',style={'font-size': '13px', 'font-weight': 'bold'})
        self.textinput_ch1 = gui.TextInput(width=120, height=20,margin='15px')
        self.textinput_ch2 = gui.TextInput(width=120, height=20,margin='15px')
        self.textinput_ch3 = gui.TextInput(width=120, height=20,margin='15px')
        self.textinput_ch4 = gui.TextInput(width=120, height=20,margin='15px')
        self.list_textinput_ch = [self.textinput_ch1,self.textinput_ch2,self.textinput_ch3,self.textinput_ch4]
        if n_chucks ==5:
            self.textinput_ch5 = gui.TextInput(width=120, height=20,margin='15px')
            self.list_textinput_ch.append(self.textinput_ch5)

        for textinput in self.list_textinput_ch:
            textinput.set_value('20UXXYY#######')
            textinput.attributes["disabled"] = ""

        subContainerLeft_1.append([self.lbl_01, self.list_checkBox_ch])
        subContainerLeft_2.append([self.lbl_02, self.list_dropDown_ch])
        subContainerLeft_3.append([self.lbl_03, self.list_textinput_ch])

        subContainerLeft.append([subContainerLeft_1,subContainerLeft_2,subContainerLeft_3])

        #-------------------------- Middle V Container ---------------------
        subContainerMiddle = gui.Container(width=250, layout_orientation=gui.Container.LAYOUT_HORIZONTAL, style={'display': 'block', 'overflow': 'auto', 'text-align': 'left'})
        subContainerMiddle_1 = gui.Container(width=250, layout_orientation=gui.Container.LAYOUT_HORIZONTAL, style={'display': 'block', 'overflow': 'auto', 'text-align': 'left'})
        self.subContainerMiddle_2 = gui.Container(width=250, layout_orientation=gui.Container.LAYOUT_VERTICAL, style={'display': 'block', 'overflow': 'auto', 'text-align': 'left','border':'Sens solid black'})


        self.lbl_05 = gui.Label('Tests', width=200, height=20, margin='15px',style={'font-size': '15px', 'font-weight': 'bold'})
        self.radioButton_stTest = RadioButtonWithLabel('Standard tests',True, 'groupTests', width=250, height=20, margin='10px')
        self.radioButton_cuTest = RadioButtonWithLabel('Custom tests',False, 'groupTests', width=250, height=20, margin='10px')

        self.checkBox_t1 = gui.CheckBoxLabel('Strobe Delay', False, width=110, height=20, margin='10px',style={'font-size': '15px','display': 'block', 'overflow': 'auto', 'text-align': 'left'})
        self.checkBox_t2 = gui.CheckBoxLabel('Three Point Gain', False, width=140, height=20, margin='10px',style={'font-size': '15px','display': 'block', 'overflow': 'auto', 'text-align': 'left'})
        self.checkBox_t3 = gui.CheckBoxLabel('Trim Range', False, width=105, height=20, margin='10px',style={'font-size': '15px','display': 'block', 'overflow': 'auto', 'text-align': 'left'})
        self.checkBox_t4 = gui.CheckBoxLabel('Three Point Gain part 2', False, width=180, height=20, margin='10px',style={'font-size': '15px','display': 'block', 'overflow': 'auto', 'text-align': 'left'})
        self.checkBox_t5 = gui.CheckBoxLabel('Response Curve', False, width=135, height=20, margin='10px',style={'font-size': '15px','display': 'block', 'overflow': 'auto', 'text-align': 'left'})
        self.checkBox_t6 = gui.CheckBoxLabel('Three Point Gain High Stats', False, width=210, height=20, margin='10px',style={'font-size': '15px','display': 'block', 'overflow': 'auto', 'text-align': 'left'})
        self.checkBox_t7 = gui.CheckBoxLabel('Noise Occupancy', False, width=145, height=20, margin='10px',style={'font-size': '15px','display': 'block', 'overflow': 'auto', 'text-align': 'left'})

        #subContainerMiddle_1.append([self.lbl_05, self.dropDown_tests])
        subContainerMiddle_1.append([self.lbl_05, self.radioButton_stTest, self.radioButton_cuTest])
        self.subContainerMiddle_2.append([self.checkBox_t1,self.checkBox_t2,self.checkBox_t3,self.checkBox_t4,self.checkBox_t5,self.checkBox_t6,self.checkBox_t7])


        self.subContainerMiddle_2.style['pointer-events'] = 'none'
        self.subContainerMiddle_2.style['opacity'] = '0.4' #this is to give a disabled apparence

        self.radioButton_stTest.onchange.do(self.radio_changed)
        self.radioButton_cuTest.onchange.do(self.radio_changed)

        subContainerMiddle.append([subContainerMiddle_1,self.subContainerMiddle_2])

        #-------------------------- Right V Container ---------------------
        # the arguments are	width - height - layoutOrientationOrizontal
        subContainerRight = gui.Container(width=300, layout_orientation=gui.Container.LAYOUT_HORIZONTAL, style={'display': 'block', 'overflow': 'auto', 'text-align': 'left'})

        self.subContainerRight_1 = gui.Container(width=300, layout_orientation=gui.Container.LAYOUT_HORIZONTAL, style={'display': 'block', 'overflow': 'auto', 'text-align': 'left'})
        self.subContainerRight_2 = gui.Container(width=300, layout_orientation=gui.Container.LAYOUT_HORIZONTAL, style={'display': 'block', 'overflow': 'auto', 'text-align': 'left'})
        self.subContainerRight_3 = gui.Container(width=300, layout_orientation=gui.Container.LAYOUT_VERTICAL, style={'display': 'block', 'overflow': 'auto', 'text-align': 'left'})

        self.lbl_04 = gui.Label('Controles', width=200, height=30, margin='5px',style={'font-size': '15px', 'font-weight': 'bold'})


        self.btStart = gui.Button('START', width=100, height=30, margin='10px',style={'font-size': '16px', 'font-weight': 'bold','background-color': '#28B463'})
        self.btStart.onclick.do(self.on_btStart_pressed)

        self.btStop = gui.Button('STOP', width=100, height=30, margin='10px',style={'font-size': '16px', 'font-weight': 'bold','background-color': '#C0392B'})
        self.btStop.attributes["disabled"] = ""
        self.btStop.onclick.do(self.on_btStop_pressed)

        self.subContainerRight_1.append([self.btStart,self.btStop])


        self.lbl_spin = gui.Label('# of cycles', width=100, height=20, margin='5px')
        self.spin = gui.SpinBox(10, 1, 100, width=100, height=20, margin='10px')
        #self.spin.onchange.do(self.on_spin_change)

        self.subContainerRight_2.append([self.lbl_spin,self.spin])

        self.lbl_status = gui.Label('Status', width=200, height=30, margin='1px',style={'font-size': '15px', 'font-weight': 'bold'})
        self.statusBox = gui.TextInput(False,width=280, height=160, margin='1px')

        self.subContainerRight_3.append([self.lbl_status,self.statusBox])
        subContainerRight.append([self.lbl_04,self.subContainerRight_1 ,self.subContainerRight_2, self.subContainerRight_3])


        #-------------------------- Log Container ---------------------
        # the arguments are	width - height - layoutOrientationOrizontal
        subContainerLog = gui.Container(width=380, style={'display': 'block', 'overflow': 'auto', 'text-align': 'left'})
        self.subContainerLog_1 = gui.Container(width=380, layout_orientation=gui.Container.LAYOUT_VERTICAL, style={'display': 'block', 'overflow': 'auto', 'text-align': 'left'})

        self.lbl_LogBox = gui.Label('Log', width=200, height=30, margin='1px',style={'font-size': '15px', 'font-weight': 'bold'})
        self.stdout_LogBox = gui.TextInput(False,width=380, height=295, margin='1px')

        self.subContainerLog_1.append([self.lbl_LogBox, self.stdout_LogBox])
        subContainerLog.append(self.subContainerLog_1)


        #----------- Grafana pannels and interlocks -----------------------------------------
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


        #--------------------------- Wrapping the subcontainers -----------------------------------------
        horizontalContainer.append([subContainerLeft, subContainerMiddle, subContainerRight, subContainerLog])

        horizontalContainer_grafana_panels.append([self.grafana_panel_list])
        horizontalContainer_grafana_intrl.append([self.grafana_intrl_list])



        #--------------------------- TAB 1 -----------------------------------------
        verticalContainer_tb1.append([horizontalContainer_logo, horizontalContainer, horizontalContainer_grafana_intrl, horizontalContainer_grafana_panels])


        #===================================== TAB 2 =================================================
        horizontalContainer_tb2 = gui.Container(width='100%', layout_orientation=gui.Container.LAYOUT_HORIZONTAL, margin='10px', style={'display': 'block', 'overflow': 'auto'})

        self.lbl_placeHolder = gui.Label('Place holder content', width=200, height=30, margin='5px',style={'font-size': '15px', 'font-weight': 'bold','color': 'red'})

        #------ Left Container ---------
        subContainerLeft_tb2 = gui.Container(width=300, layout_orientation=gui.Container.LAYOUT_HORIZONTAL, style={'display': 'block', 'overflow': 'auto', 'text-align': 'left','border':'0px solid black'})
        self.lbl_temp = gui.Label('Temperature[C]', width=200, height=20, margin='5px',style={'font-size': '15px', 'font-weight': 'bold'})


        # Temperatues table
        self.table_t = gui.Table(children={
            'row0': gui.TableRow({'col1':'  #  ', 'col2':'Chuck', 'col3':'Module'}),
            'row1': gui.TableRow({'col1':'1','col2':'', 'col3':''}),
            'row2': gui.TableRow({'col1':'2','col2':'', 'col3':''}),
            'row3': gui.TableRow({'col1':'3','col2':'', 'col3':''}),
            'row4': gui.TableRow({'col1':'4','col2':'', 'col3':''})
            },
            width=250, height=200, margin='10px auto')
        if n_chucks==5:
            self.table_t.add_child('row5', gui.TableRow({'col1':'5','col2':'', 'col3':''}) )

        subContainerLeft_tb2.append([self.lbl_temp, self.table_t])

        #------ Middle Container ---------

        subContainerMiddle_tb2 = gui.Container(width=300, layout_orientation=gui.Container.LAYOUT_HORIZONTAL, style={'display': 'block', 'overflow': 'auto', 'text-align': 'left','border':'0px solid black'})

        if (plt_field):
            self.lbl_peltiers = gui.Label('Peltiers', width=200, height=20, margin='5px',style={'font-size': '15px', 'font-weight': 'bold'})
            # Peltiers I/V table
            self.table_Plt = gui.Table(children={
                'row0': gui.TableRow({'col1':'  #  ', 'col2':'Current[mA]', 'col3':'Voltage[V]'}),
                'row1': gui.TableRow({'col1':'1','col2':'', 'col3':''}),
                'row2': gui.TableRow({'col1':'2','col2':'', 'col3':''}),
                'row3': gui.TableRow({'col1':'3','col2':'', 'col3':''}),
                'row4': gui.TableRow({'col1':'4','col2':'', 'col3':''}),
                },
                width=250, height=200, margin='10px auto')
            if n_chucks==5:
                self.table_Plt.add_child('row5', gui.TableRow({'col1':'5','col2':'', 'col3':''}) )

            subContainerMiddle_tb2.append([self.lbl_peltiers,self.table_Plt])

        #------ Right Container ---------
        subContainerRight_tb2 = gui.Container(width=400, layout_orientation=gui.Container.LAYOUT_HORIZONTAL, style={'display': 'block', 'overflow': 'auto', 'text-align': 'left'})
        self.lbl_Box = gui.Label('ColdBox Ambient', width=200, height=20, margin='5px',style={'font-size': '15px', 'font-weight': 'bold'})


        # Ambient table
        self.table_amb = gui.Table(children={
            'row0': gui.TableRow({'col1':'Relative H[%]', 'col2':''}),
            'row1': gui.TableRow({'col1':'Temperature[C]','col2':''}),
            'row2': gui.TableRow({'col1':'DewPoint[C]','col2':''}),
            'row3': gui.TableRow({'col1':'Flow N2/DryAir[l/s]','col2':''}),
            'row4': gui.TableRow({'col1':'Coolant temperature[C]','col2':''}),
            'row5': gui.TableRow({'col1':'Flow Coolant[l/s]','col2':''})
            },
            width=250, height=200, margin='10px auto',style={'text-align': 'left'})

        subContainerRight_tb2.append([self.lbl_Box,self.table_amb])



        horizontalContainer_tb2.append([subContainerLeft_tb2, subContainerMiddle_tb2, subContainerRight_tb2])




        verticalContainer_tb2.append([horizontalContainer_logo, self.lbl_placeHolder, horizontalContainer_tb2])

        #this flag will be used to stop the display_counter Timer
        self.stop_flag = False


        #===================================== TAB 3 =================================================
        verticalContainer_tb3.append([horizontalContainer_logo, self.lbl_placeHolder])


        #===================================== TAB 4 =================================================
        self.lbl_swName = gui.Label('ColdBox Controller V 0.3', width=200, height=30, margin='5px',style={'font-size': '15px', 'font-weight': 'bold'})
        self.lbl_coldbox_type = gui.Label('ColdBox type: '+coldbox_type , width=200, height=30, margin='5px')
        verticalContainer_tb4.append([horizontalContainer_logo, self.lbl_swName, self.lbl_coldbox_type])



        #===================================== Wrapping all tabs together =================================================

        tabBox = gui.TabBox(width='40%',style={'font-size': '16px', 'font-weight': 'bold','background-color': '#3498DB'})
        tabBox.append(verticalContainer_tb1, 'Control Panel')
        tabBox.add_tab(verticalContainer_tb2, 'Monitoring', None)
        tabBox.add_tab(verticalContainer_tb3, 'Advanced', None)
        tabBox.add_tab(verticalContainer_tb4, 'About', None)

        # returning the root widget
        #return verticalContainer_tb1

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


    def on_btStart_pressed(self, widget):
        currentDT = datetime.datetime.now()
        current_text=self.read_user_options()
        logger.info("Thermocycling started!")
        #current_text= self.statusBox.get_text()
        self.statusBox.set_text(current_text+"["+currentDT.strftime("%H:%M:%S")+"] -- Thermocycling started\n")
        self.btStart.attributes["disabled"] = ""
        del self.btStop.attributes["disabled"]
        #--FIX ME
        #self.subContainerRight_1.style['pointer-events'] = 'none'
        #self.subContainerRight_1.style['opacity'] = '0.4' #this is to give a disabled apparence


    def on_btStop_pressed(self, widget):
        self.dialog = gui.GenericDialog(title='attempt to stop Thermocycling', message='Are you sure you want to terminate the Thermocycling?', width='500px')
        self.dialog.confirm_dialog.do(self.Terminate_thermocycling)
        self.dialog.show(self)

    def Terminate_thermocycling(self, widget):
        currentDT = datetime.datetime.now()
        current_text= self.statusBox.get_text()
        logger.info("Thermocycling stopped!")
        self.statusBox.set_text(current_text+"["+currentDT.strftime("%H:%M:%S")+"] -- Thermocycling stopped!\n")
        self.btStop.attributes["disabled"] = ""
        del self.btStart.attributes["disabled"]
        #--FIX ME
        #del self.subContainerRight_1.style['pointer-events']
        #del self.subContainerRight_1.style['opacity']
        self.notification_message("Thermocycling terminated!", "")


    def read_user_options(self):
        ncycle = self.spin.get_value()
        availavle_chucks=[]

        for chuck in self.list_checkBox_ch:
            availavle_chucks.append(int(chuck.get_value()) )
        logger.debug('availavle_chucks: '+str(availavle_chucks))

        self.total_selected_chucks = np.sum(list(map(int,availavle_chucks)))
        logger.debug('total_selected_chucks: '+str(self.total_selected_chucks))

        if self.radioButton_stTest.get_value():
            selected_tests = ' standard'
        else:
            selected_tests_helper = [self.checkBox_t1.get_value(),self.checkBox_t2.get_value(),self.checkBox_t3.get_value(),self.checkBox_t4.get_value(),self.checkBox_t5.get_value(),self.checkBox_t6.get_value(),self.checkBox_t7.get_value()]
            selected_tests = str(list(map(int,selected_tests_helper)))
            self.total_selected_tests = np.sum(list(map(int,selected_tests_helper)))
            logger.debug('custom test is running: '+str(self.total_selected_tests)+' tests')

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
            time.sleep(5)

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
            time.sleep(5)


    def update_table_amb(self):
        while self.thread_alive_flag:
            self.readout_table_amb['row0_col2']= str(get_measurement(self.dbClient, INFLUXDB_DATABASE,config_device["CB_device_rH"],INFLUXDB_MEASUREMENT,'rH'))
            self.readout_table_amb['row1_col2']= str(get_measurement(self.dbClient,INFLUXDB_DATABASE,config_device["CB_device_T"],INFLUXDB_MEASUREMENT,'T'))
            self.readout_table_amb['row2_col2']= str(get_dewpoint(get_measurement(self.dbClient,INFLUXDB_DATABASE,config_device["CB_device_T"],INFLUXDB_MEASUREMENT,'T'), get_measurement(self.dbClient,INFLUXDB_DATABASE,config_device["CB_device_rH"],INFLUXDB_MEASUREMENT,'rH') ))
            self.readout_table_amb['row3_col2']= str(get_measurement(self.dbClient,INFLUXDB_DATABASE,config_device["CB_device_N2flw"],INFLUXDB_MEASUREMENT,'T'))
            self.readout_table_amb['row4_col2']= str(get_measurement(self.dbClient,INFLUXDB_DATABASE,config_device["CB_device_Chiller_T"],INFLUXDB_MEASUREMENT,'T'))
            self.readout_table_amb['row5_col2']= str(get_measurement(self.dbClient,INFLUXDB_DATABASE,config_device["CB_device_Chiller_flw"],INFLUXDB_MEASUREMENT,'T'))
            time.sleep(5)

    def on_close(self):
        self.thread_alive_flag = False
        super(ColdBoxGUI, self).on_close()


if __name__ == "__main__":
    logger = GUIlogger.init_logger(__name__)
    #logger.info(bcolors.OKGREEN+"Starting ColdJig GUI"+bcolors.ENDC)
    logger.info("Starting ColdJig GUI")
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
        logger.error('option requires argument.\n Usage: blah -c configFile \n Process terminated.')
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
        #logger.error(bcolors.FAIL + "Attempt to start the GUI without user config.\n Process terminated." + bcolors.ENDC)
        logger.error("Attempt to start the GUI without user config.\n Process terminated.")
        sys.exit(1)

    else:
        if os.path.isfile(configfile):
            config.read(configfile)
        else:
            #logger.error(bcolors.FAIL +'Config file does not exist. Process terminated.' +bcolors.ENDC)
            logger.error('Config file does not exist. Process terminated.')
            sys.exit(1)

    #logger.info(bcolors.OKGREEN+'Reading config file: '+configfile+bcolors.ENDC)
    logger.info('Reading config file: '+configfile)
    config_gui, config_influx, config_device = configreader.read_conf(config)


    gui_server = config_gui["gui_server"]
    gui_server_port = config_gui["gui_server_port"]
    coldbox_type = config_gui["coldbox_type"]
    n_chucks = config_gui["n_chucks"]
    plt_field = config_gui["plt_field"]
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

    ch_device_list = config_device["ch_device_list"]
    mod_device_list = config_device["mod_device_list"]
    pltC_device_list = config_device["pltC_device_list"]
    pltV_device_list = config_device["pltV_device_list"]
    CB_device_rH = config_device["CB_device_rH"]
    CB_device_T = config_device["CB_device_T"]
    CB_device_N2flw = config_device["CB_device_N2flw"]
    CB_device_Chiller_T = config_device["CB_device_Chiller_T"]
    CB_device_Chiller_flw = config_device["CB_device_Chiller_flw"]


    logger.debug('gui_server= '+gui_server)
    logger.debug('gui_port= '+str(gui_server_port))

    logger.debug('influx_server= '+INFLUXDB_ADDRESS)
    logger.debug('influx_user= '+INFLUXDB_USER)
    logger.debug('influx_port= '+INFLUXDB_PORT)
    logger.debug('influx_database= '+INFLUXDB_DATABASE)
    logger.debug('influx_measurement= '+INFLUXDB_MEASUREMENT)

    logger.debug('coldbox_type= '+coldbox_type)
    logger.debug('n_chucks= '+str(n_chucks))
    logger.debug('plt_fields= '+str(plt_field))

    logger.debug('gui_debug= '+str(gui_debug))
    #logger.debug('gui_logging_level= '+str(gui_logging_level))
    logger.debug('gui_start_browser= '+str(gui_start_browser))
    logger.debug('gui_multiple_instance= '+str(gui_multiple_instance))
    logger.debug('gui_enable_file_cache= '+str(gui_enable_file_cache))

    logger.debug('CB_device_Chiller_flw= '+CB_device_Chiller_flw)

    logger.debug('ch_device_list='+ str(ch_device_list))
    logger.debug('mod_device_list='+ str(mod_device_list))
    logger.debug('pltC_device_list='+ str(pltC_device_list))
    logger.debug('pltV_device_list='+ str(pltV_device_list))
    #logger.debug('grf_panel_list='+ str(grf_panel_list))
    #logger.debug('grf_intrl_list='+ str(grf_intrl_list))

    #-- checking number of chucks--
    if not (n_chucks==5 or n_chucks==4):
        #logger.error(bcolors.FAIL +'Number of chucks is not supported. Set n_chucks in config file to 4 or 5.' +bcolors.ENDC)
        logger.error('Number of chucks is not supported. Set n_chucks in config file to 4 or 5.')
        sys.exit(1)

    #exit()

    if not verbose:
        stdout_string_io = StringIO()
        sys.stdout = sys.stderr = stdout_string_io

    #--starts the webserver / optional parameters
    #start(ColdBoxGUI, update_interval=0.5, debug=gui_debug, address=gui_server, port=gui_server_port, start_browser=gui_start_browser, multiple_instance=gui_multiple_instance, enable_file_cache=gui_enable_file_cache)
    start(ColdBoxGUI, debug=gui_debug, address=gui_server, port=gui_server_port, start_browser=gui_start_browser, multiple_instance=gui_multiple_instance, enable_file_cache=gui_enable_file_cache)
