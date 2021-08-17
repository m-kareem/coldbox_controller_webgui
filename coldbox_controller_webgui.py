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
Configuration file must be specified with option -c filename.conf
Mohammad Kareem, 2021
https://gitlab.cern.ch/mkareem/coldbox_controller_webgui
'''

import remi.gui as gui
from remi import start, App
from GUImodules.RadioButton import *
import GUImodules.Popup as Popup
from threading import Timer
import configparser as conf
from GUImodules.dewPoint import *
import GUImodules.CBChelp as CBChelp
import numpy as np
import random
import os, sys, getopt
import importlib

from io import StringIO ## for Python 3
stdout_string_io = StringIO()
sys.stderr = sys.stdout= stdout_string_io

import time,datetime

#import user_manager
#from user_manager import *

import logging, logging.config

import threading

from pubsub import pub

#-- For pubsub testing only
#testPubSub = True
testPubSub = False
if testPubSub:
    import coldjig_pubsub

#--- HTML color codes:
col_blue  = '#2563C8'
col_lblue  = '#259CC8'
col_red   = '#C82525'
col_green = '#34B63B'
col_darkBlue = '#21618C'
#--------------------------------------------------------------
class ColdBoxGUI(App):
    def __init__(self, *args):

        res_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), './res/')
        super(ColdBoxGUI, self).__init__(*args, static_file_path={'my_res':res_path})

    def idle(self):
        #idle function called every update cycle (e.g. update_interval=0.1 argument in 'start' function)

        # -- updating the logBox
        if not verbose:
            stdout_string_io.seek(0)
            lines = stdout_string_io.readlines()
            lines.reverse()
            self.stdout_LogBox.set_text("".join(lines))
        else:
            self.stdout_LogBox.set_text(" Run without verbose option (-v) to redirect the terminal outputs here.")


    def main(self):
        return ColdBoxGUI.construct_ui(self)


    @staticmethod
    def construct_ui(self):
        # the margin 0px auto centers the main container
        verticalContainer_tb1 = gui.VBox(width = "100%", height=450)
        verticalContainer_tb2 = gui.VBox(width = "100%", height=450)
        verticalContainer_tb3 = gui.VBox(width = "100%", height=450)

        horizontalContainer_logo = gui.Container(width='40%', layout_orientation=gui.Container.LAYOUT_HORIZONTAL, margin='10px', style={'display': 'block', 'overflow': 'auto'})
        #horizontalContainer = gui.HBox(width = "95%",style={'align-items':'flex-start', 'justify-content':'space-around'})
        horizontalContainer = gui.HBox(width = "95%",style={'align-items':'stretch', 'justify-content':'center'})

        horizontalContainer_grafana_dash = gui.HBox(width = "100%")
        horizontalContainer_grafana_dash.style['justify-content'] ='flex-start'
        horizontalContainer_grafana_dash.style['align-items'] = 'flex-start'

        horizontalContainer_grafana_intrl = gui.HBox(width = "100%")
        horizontalContainer_grafana_intrl.style['justify-content'] ='flex-start'
        horizontalContainer_grafana_intrl.style['align-items'] = 'flex-start'

        horizontalContainer_grafana_panels = gui.HBox(width = "100%")
        horizontalContainer_grafana_panels.style['justify-content'] ='flex-start'
        horizontalContainer_grafana_panels.style['align-items'] = 'flex-start'

        #--------logo Container ---------------
        self.img_logo = gui.Image('/my_res:ITKlogo.png', width=200, height=67)
        self.lbl_ColdBoxType = gui.Label('ColdBox type: '+coldbox_type , width=200, height=20, margin='20px',style={'font-size': '14px', 'font-weight': 'bold','color': 'red'})
        #horizontalContainer_logo.append(self.img_logo)
        horizontalContainer_logo.append([self.img_logo,self.lbl_ColdBoxType])


        #============================================= Tab 1 =============================================
        #-------------------------- Left Container ---------------------
        subContainerLeft = gui.GridBox(width='30%', height='100%', style={'margin':'10px'})
        self.lbl_ava = gui.Label('Available chk.', width="100%", height=20, style={'font-size': '15px', 'font-weight': 'bold','color': col_darkBlue})
        self.lbl_mod = gui.Label('Module Flv..', width="100%", height=20, style={'font-size': '15px', 'font-weight': 'bold','color': col_darkBlue})
        self.lbl_ser = gui.Label('Serial #', width="100%", height=20, style={'font-size': '15px', 'font-weight': 'bold','color': col_darkBlue})

        self.checkBox_ch1 = gui.CheckBoxLabel('Chuck 1', False, width="100%", height=25)
        self.checkBox_ch2 = gui.CheckBoxLabel('Chuck 2', False, width="100%", height=25)
        self.checkBox_ch3 = gui.CheckBoxLabel('Chuck 3', False, width="100%", height=25)
        self.checkBox_ch4 = gui.CheckBoxLabel('Chuck 4', False, width="100%", height=25)
        self.list_checkBox_ch = [self.checkBox_ch1,self.checkBox_ch2,self.checkBox_ch3,self.checkBox_ch4]
        if n_chucks ==5:
            self.checkBox_ch5 = gui.CheckBoxLabel('Chuck 5', False, width="100%", height=25)
            self.list_checkBox_ch.append(self.checkBox_ch5)

        for checkBox in self.list_checkBox_ch:
            checkBox.onchange.do(self.onchange_checkbox_ch)

        self.dropDown_ch1 = gui.DropDown.new_from_list(('LS','SS','R0','R1','R2','R3','R4','R5'), width="100%", height=25)
        self.dropDown_ch2 = gui.DropDown.new_from_list(('LS','SS','R0','R1','R2','R3','R4','R5'), width="100%", height=25)
        self.dropDown_ch3 = gui.DropDown.new_from_list(('LS','SS','R0','R1','R2','R3','R4','R5'), width="100%", height=25)
        self.dropDown_ch4 = gui.DropDown.new_from_list(('LS','SS','R0','R1','R2','R3','R4','R5'), width="100%", height=25)
        self.list_dropDown_ch = [self.dropDown_ch1,self.dropDown_ch2,self.dropDown_ch3,self.dropDown_ch4]
        if n_chucks ==5:
            self.dropDown_ch5 = gui.DropDown.new_from_list(('LS','SS','R0','R1','R2','R3','R4','R5'), width="100%", height=25)
            self.list_dropDown_ch.append(self.dropDown_ch5)

        for dropDown in self.list_dropDown_ch:
            dropDown.select_by_value('LS')
            dropDown.attributes["disabled"] = ""
            dropDown.style['opacity'] = '0.4' #this is to give a disabled apparence

        self.textinput_ch1 = gui.TextInput(width="100%", height=25)
        self.textinput_ch2 = gui.TextInput(width="100%", height=25)
        self.textinput_ch3 = gui.TextInput(width="100%", height=25)
        self.textinput_ch4 = gui.TextInput(width="100%", height=25)
        self.list_textinput_ch = [self.textinput_ch1,self.textinput_ch2,self.textinput_ch3,self.textinput_ch4]
        if n_chucks ==5:
            self.textinput_ch5 = gui.TextInput(width="100%", height=25)
            self.list_textinput_ch.append(self.textinput_ch5)

        for textinput in self.list_textinput_ch:
            textinput.set_value('20UXXYY#######')
            textinput.attributes["disabled"] = ""

        if n_chucks ==5:
            subContainerLeft.set_from_asciiart("""
                |lbl_ava      |lbl_mod      | lbl_ser      |
                |checkBox_ch1 |dropDown_ch1 |textinput_ch1 |
                |checkBox_ch2 |dropDown_ch2 |textinput_ch2 |
                |checkBox_ch3 |dropDown_ch3 |textinput_ch3 |
                |checkBox_ch4 |dropDown_ch4 |textinput_ch4 |
                |checkBox_ch5 |dropDown_ch5 |textinput_ch5 |
                """, 2, 10)
        else:
            subContainerLeft.set_from_asciiart("""
                |lbl_ava      |lbl_mod      | lbl_ser      |
                |checkBox_ch1 |dropDown_ch1 |textinput_ch1 |
                |checkBox_ch2 |dropDown_ch2 |textinput_ch2 |
                |checkBox_ch3 |dropDown_ch3 |textinput_ch3 |
                |checkBox_ch4 |dropDown_ch4 |textinput_ch4 |
                """, 2, 10)

        subContainerLeft.append({'lbl_ava':self.lbl_ava, 'lbl_mod':self.lbl_mod,'lbl_ser':self.lbl_ser,
                                 'checkBox_ch1':self.checkBox_ch1, 'dropDown_ch1':self.dropDown_ch1 , 'textinput_ch1':self.textinput_ch1,
                                 'checkBox_ch2':self.checkBox_ch2, 'dropDown_ch2':self.dropDown_ch2 , 'textinput_ch2':self.textinput_ch2,
                                 'checkBox_ch3':self.checkBox_ch3, 'dropDown_ch3':self.dropDown_ch3 , 'textinput_ch3':self.textinput_ch3,
                                 'checkBox_ch4':self.checkBox_ch4, 'dropDown_ch4':self.dropDown_ch4 , 'textinput_ch4':self.textinput_ch4,
                                })
        if n_chucks ==5:
            subContainerLeft.append({'checkBox_ch5':self.checkBox_ch5, 'dropDown_ch5':self.dropDown_ch5 , 'textinput_ch5':self.textinput_ch5 })


        subContainerLeft.style.update({'grid-template-columns':'25% 25% 30%', 'grid-template-rows':'30% 30% 30% 30% 30% 30%'})

        #-------------------------- Middle V Container ---------------------
        subContainerMiddle = gui.GridBox(width='25%', height='100%', style={'margin':'0px auto'})
        self.lbl_tests = gui.Label('Tests', width="100%", height=20, style={'font-size': '15px', 'font-weight': 'bold','color': col_darkBlue})

        self.radioButton_stTest = RadioButtonWithLabel('Standard tests',True, 'groupTests', width="100%", height=20 )
        self.radioButton_cuTest = RadioButtonWithLabel('Custom tests',False, 'groupTests', width="100%", height=20 )

        self.subContainerMiddle_2 = gui.VBox(width = "100%", style={'align-items':'flex-start', 'justify-content':'flex-start'})
        self.checkBox_t1 = gui.CheckBoxLabel('Strobe Delay', False,  height=22, margin='5px', style={'font-size': '15px','display': 'block'})
        self.checkBox_t2 = gui.CheckBoxLabel('Three Point Gain', False,  height=22, margin='5px', style={'font-size': '15px','display': 'block'})
        self.checkBox_t3 = gui.CheckBoxLabel('Trim Range', False,  height=22, margin='5px', style={'font-size': '15px','display': 'block'})
        self.checkBox_t4 = gui.CheckBoxLabel('Three Point Gain part 2', False,  height=22, margin='5px', style={'font-size': '15px','display': 'block'})
        self.checkBox_t5 = gui.CheckBoxLabel('Response Curve', False,  height=22, margin='5px', style={'font-size': '15px','display': 'block'})
        self.checkBox_t6 = gui.CheckBoxLabel('Three Point Gain High Stats', False,  height=22, margin='5px', style={'font-size': '15px','display': 'block'})
        self.checkBox_t7 = gui.CheckBoxLabel('Noise Occupancy', False,  height=22, margin='5px', style={'font-size': '15px','display': 'block'})
        self.list_checkBox_t = [self.checkBox_t1,self.checkBox_t2,self.checkBox_t3,self.checkBox_t4,self.checkBox_t5,self.checkBox_t6,self.checkBox_t7]

        self.subContainerMiddle_2.append([self.checkBox_t1,self.checkBox_t2,self.checkBox_t3,self.checkBox_t4,self.checkBox_t5,self.checkBox_t6,self.checkBox_t7])
        self.subContainerMiddle_2.style['pointer-events'] = 'none'
        self.subContainerMiddle_2.style['opacity'] = '0.4' #this is to give a disabled apparence

        self.radioButton_stTest.onchange.do(self.radio_changed)
        self.radioButton_cuTest.onchange.do(self.radio_changed)

        subContainerMiddle.set_from_asciiart("""
            |lbl_tests          |                      |
            |radioButton_stTest |radioButton_cuTest    |
            |                   |subContainerMiddle_2  |
            """, 2, 10)

        subContainerMiddle.append({'lbl_tests':self.lbl_tests,
                                  'radioButton_stTest':self.radioButton_stTest, 'radioButton_cuTest':self.radioButton_cuTest ,
                                  'subContainerMiddle_2':self.subContainerMiddle_2
        })
        subContainerMiddle.style.update({'grid-template-columns':'30% 50%', 'grid-template-rows':'5% 10% 50%'})

        #-------------------------- Right V Container ---------------------
        subContainerRight = gui.GridBox(width='40%', height='100%', style={'margin':'0px auto'})

        self.lbl_control = gui.Label('Controls', width="100%", height=20, style={'font-size': '15px', 'font-weight': 'bold','color': col_darkBlue})

        self.btStartLib = gui.Button('Start', width="100%", height=30, style={'font-size': '16px', 'font-weight': 'bold','background-color': col_green})
        self.btStartLib.onclick.do(self.on_btStartLib_pressed)
        self.btStartLib.attributes['title']='-Connects and initialises hardware\n-Starts core loop'

        self.btStopLib = gui.Button('Shutdown', width="100%", height=30, style={'font-size': '16px', 'font-weight': 'bold','background-color': col_red})
        self.btStopLib.onclick.do(self.on_btStopLib_pressed)
        self.btStopLib.attributes['title']='-Shutting down all tasks and core loop\n-Gracefully disengage hardware'
        self.btStopLib.attributes["disabled"] = ""
        self.Lib_term_popup_confirm = Popup.PopupConfirm("ColdBoxGUI", "Are you sure you want to shutdown the ColdJigLib?\nThis will close the current browser tab as well!")

        self.btStartTC = gui.Button('Start TC', width="100%", height=30, style={'font-size': '16px', 'font-weight': 'bold','background-color': col_green})
        self.btStartTC.onclick.do(self.on_btStartTC_pressed)
        self.btStartTC.attributes['title']='Start Thermocycling'
        self.btStartTC.attributes["disabled"] = ""

        self.btStopTC = gui.Button('Stop TC', width="100%", height=30, style={'font-size': '16px', 'font-weight': 'bold','background-color': col_red})
        self.btStopTC.attributes["disabled"] = ""
        self.btStopTC.onclick.do(self.on_btStopTC_pressed)
        self.btStopTC.attributes['title']='Stop Thermocycling'
        self.TC_term_popup_confirm = Popup.PopupConfirm("ColdBoxGUI", "Are you sure you want to terminate the Thermocycling?")
        self.TC_term_popup_alert = Popup.PopupAlert("ColdBoxGUI", "Thermocycling terminated!")
        self.TC_NoCh_popup_alert = Popup.PopupAlert("ERROR", 'No chuck selected!', '#BF33AD')
        self.TC_NoCusTest_popup_alert = Popup.PopupAlert("ERROR", 'No custom test selected!', '#BF33AD')

        self.lbl_spin = gui.Label('# of cycles', width="100%", height=30)
        self.spin = gui.SpinBox(10, 1, 100, width="100%", height=30, style={'font-size': '15px', 'font-weight': 'bold'})

        self.lbl_status = gui.Label('TC Status', width="100%", height=30, style={'font-size': '15px', 'font-weight': 'bold'})
        self.statusBox = gui.TextInput(False, width="100%",hight=550)
        self.statusBox.set_text('--- Welcome to ColdBoxGUI ---\n press Start to begin\n================\n')

        self.lbl_LogBox = gui.Label('Log', width="100%", height=20, style={'font-size': '15px', 'font-weight': 'bold','color': col_darkBlue})
        self.stdout_LogBox = gui.TextInput(False, width = "100%")

        subContainerRight.set_from_asciiart("""
            |lb_controls  |            |lbl_LogBox    |
            |bt_lib_start |bt_lib_stop |stdout_LogBox |
            |bt_TC_start  |bt_TC_stop  |stdout_LogBox |
            |lb_spin      |spin        |stdout_LogBox |
            |lb_status    |            |stdout_LogBox |
            |status_Box   |status_Box  |stdout_LogBox |
            """, 2, 10)

        subContainerRight.append({'lb_controls':self.lbl_control, 'lbl_LogBox':self.lbl_LogBox,
                                  'bt_lib_start':self.btStartLib, 'bt_lib_stop':self.btStopLib ,
                                  'bt_TC_start':self.btStartTC, 'bt_TC_stop':self.btStopTC ,
                                  'lb_spin':self.lbl_spin, 'spin':self.spin ,
                                  'lb_status':self.lbl_status,
                                  'status_Box':self.statusBox,
                                  'stdout_LogBox':self.stdout_LogBox,
        })
        subContainerRight.style.update({'grid-template-columns':'25% 25% 60%', 'grid-template-rows':'10% 10% 10% 10% 10% 100%'})

        #- Wrapping the subcontainers
        horizontalContainer.append([subContainerLeft, subContainerMiddle, subContainerRight,
                                    self.TC_term_popup_alert, self.TC_NoCh_popup_alert, self.TC_NoCusTest_popup_alert,
                                    self.TC_term_popup_confirm, self.Lib_term_popup_confirm])

        verticalContainer_tb1.append([horizontalContainer_logo, horizontalContainer])
        verticalContainer_tb1.style['justify-content'] ='flex-start'
        verticalContainer_tb1.style['align-items'] = 'flex-start'


        #===================================== TAB 2 =================================================
        '''
        Monitoring Tab removed
        '''

        #===================================== TAB 2 =================================================
        self.data_dict = coldjigcontroller.data_dict
        subContainerADV = gui.GridBox(width = "100%",hight = "100%", style={'margin':'20px auto','align-items':'flex-start', 'justify-content':'flex-start'})

        #------------TC controls-----------
        subContainerADV_TC = gui.GridBox(width = "100%",hight = "100%", style={'margin':'20px','align-items':'flex-start', 'justify-content':'flex-start'})
        subContainerADV_TC.style['border-left'] = '3px solid rgba(0,0,0,.12)'

        self.lbl_TC = gui.Label('Thermocycling settings', width=200, height=20, margin='5px',style={'font-size': '14px', 'font-weight': 'bold'})

        self.lbl_textinput_TCHot = gui.Label('Hot temperature [C]', width=200, height=20, margin='5px',style={'font-size': '14px'})
        self.textinput_TCHot = gui.TextInput(width=50, height=20,margin='5px')
        self.textinput_TCHot.set_value('40')
        #self.btTCHotset = gui.Button('SET', width=50, height=20, margin='5px', style={'font-size': '16px', 'font-weight': 'bold','background-color': col_lblue})

        self.lbl_textinput_TCCold = gui.Label('Cold temperature [C]', width=200, height=20, margin='5px',style={'font-size': '14px'})
        self.textinput_TCCold = gui.TextInput(width=50, height=20,margin='5px')
        self.textinput_TCCold.set_value('-35')
        #self.btTCColdset = gui.Button('SET', width=50, height=20, margin='5px', style={'font-size': '16px', 'font-weight': 'bold','background-color': col_lblue})

        self.lbl_textinput_TCWarmup = gui.Label('Warm-up temperature [C]', width=200, height=20, margin='5px',style={'font-size': '14px'})
        self.textinput_TCWarmup = gui.TextInput(width=50, height=20,margin='5px')
        self.textinput_TCWarmup.set_value('20')
        #self.btTCWarmupset = gui.Button('SET', width=50, height=20, margin='5px', style={'font-size': '16px', 'font-weight': 'bold','background-color': col_lblue})

        subContainerADV_TC.set_from_asciiart("""
            |TC_label    |TC_label    |                    |
            |TCCold      |TCCold      | textinput_TCCold   |
            |TCHot       |TCHot       | textinput_TCHot    |
            |TCWarmup    |TCWarmup    | textinput_TCWarmup |

            """, 10, 10)

        subContainerADV_TC.append({'TC_label':self.lbl_TC,
                                    'TCHot':self.lbl_textinput_TCHot,'textinput_TCHot': self.textinput_TCHot,
                                    'TCCold':self.lbl_textinput_TCCold,'textinput_TCCold': self.textinput_TCCold,
                                    'TCWarmup':self.lbl_textinput_TCWarmup,'textinput_TCWarmup': self.textinput_TCWarmup,
                                    })

        if coldbox_type == 'BNL':
            #------------HV controls-----------
            subContainerADV_HV = gui.GridBox(width = "40%", hight = "100%", style={'margin':'20px','align-items':'flex-start', 'justify-content':'flex-start'})
            subContainerADV_HV.style['border-left'] = '3px solid rgba(0,0,0,.12)'

            self.lbl_HV = gui.Label('High-Voltage', width=110, height=20, margin='5px',style={'font-size': '14px', 'font-weight': 'bold'})

            self.btHVon = gui.Button('ON', width=75, height=20, margin='5px', style={'font-size': '16px', 'font-weight': 'bold','background-color': col_green})
            self.btHVoff = gui.Button('OFF', width=75, height=20, margin='5px', style={'font-size': '16px', 'font-weight': 'bold','background-color': col_red})

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

            self.btHVon_0 = gui.Button('ON', width=50, height=20, margin='5px', style={'font-size': '16px', 'font-weight': 'bold','background-color': col_green})
            self.btHVon_1 = gui.Button('ON', width=50, height=20, margin='5px', style={'font-size': '16px', 'font-weight': 'bold','background-color': col_green})
            self.btHVon_2 = gui.Button('ON', width=50, height=20, margin='5px', style={'font-size': '16px', 'font-weight': 'bold','background-color': col_green})
            self.btHVon_3 = gui.Button('ON', width=50, height=20, margin='5px', style={'font-size': '16px', 'font-weight': 'bold','background-color': col_green})

            self.btHVoff_0 = gui.Button('OFF', width=50, height=20, margin='5px', style={'font-size': '16px', 'font-weight': 'bold','background-color': col_red})
            self.btHVoff_1 = gui.Button('OFF', width=50, height=20, margin='5px', style={'font-size': '16px', 'font-weight': 'bold','background-color': col_red})
            self.btHVoff_2 = gui.Button('OFF', width=50, height=20, margin='5px', style={'font-size': '16px', 'font-weight': 'bold','background-color': col_red})
            self.btHVoff_3 = gui.Button('OFF', width=50, height=20, margin='5px', style={'font-size': '16px', 'font-weight': 'bold','background-color': col_red})

            self.btHVset_0 = gui.Button('SET', width=50, height=20, margin='5px', style={'font-size': '16px', 'font-weight': 'bold','background-color': col_lblue})
            self.btHVset_1 = gui.Button('SET', width=50, height=20, margin='5px', style={'font-size': '16px', 'font-weight': 'bold','background-color': col_lblue})
            self.btHVset_2 = gui.Button('SET', width=50, height=20, margin='5px', style={'font-size': '16px', 'font-weight': 'bold','background-color': col_lblue})
            self.btHVset_3 = gui.Button('SET', width=50, height=20, margin='5px', style={'font-size': '16px', 'font-weight': 'bold','background-color': col_lblue})



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

            self.btHVon.onclick.do(self.on_btHV_sw_pressed,-1,'on')
            self.btHVoff.onclick.do(self.on_btHV_sw_pressed,-1,'off')

            for i in range(4):
                self.list_btHVon[i].onclick.do(self.on_btHV_sw_pressed,i,'on')
                self.list_btHVoff[i].onclick.do(self.on_btHV_sw_pressed,i,'off')
                self.list_btHVset[i].onclick.do(self.on_btHVset_pressed,i)

            #------------LV controls-----------
            subContainerADV_LV1 = gui.GridBox(width = "100%",hight = "100%", style={'margin':'20px auto','align-items':'flex-start', 'justify-content':'flex-start'})
            subContainerADV_LV1.style['border-left'] = '3px solid rgba(0,0,0,.12)'

            self.lbl_LV1 = gui.Label('Low-Voltage 1', width=110, height=20, margin='5px',style={'font-size': '14px', 'font-weight': 'bold'})

            self.btLV1on = gui.Button('ON', width=50, height=20, margin='5px', style={'font-size': '16px', 'font-weight': 'bold','background-color': col_green})
            self.btLV1off = gui.Button('OFF', width=50, height=20, margin='5px', style={'font-size': '16px', 'font-weight': 'bold','background-color': col_red})

            self.lbl_textinput_LV1_0 = gui.Label('CH0', width=50, height=20, margin='5px',style={'font-size': '14px'})
            self.lbl_textinput_LV1_1 = gui.Label('CH1', width=50, height=20, margin='5px',style={'font-size': '14px'})

            self.textinput_LV1_0 = gui.TextInput(width=50, height=20,margin='5px')
            self.textinput_LV1_1 = gui.TextInput(width=50, height=20,margin='5px')

            self.list_textinput_LV1 = [self.textinput_LV1_0,self.textinput_LV1_1]
            for textinput in self.list_textinput_LV1:
                textinput.set_value('0.00')

            self.btLV1set = gui.Button('SET', width=50, height=50, margin='5px', style={'font-size': '16px', 'font-weight': 'bold','background-color': col_lblue})


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
            self.btLV1on.onclick.do(self.on_btLV_sw_pressed,1,'on')
            self.btLV1off.onclick.do(self.on_btLV_sw_pressed,1,'off')
            self.btLV1set.onclick.do(self.on_btLVset_pressed,1)


            subContainerADV_LV2 = gui.GridBox(width = "100%",hight = "100%", style={'margin':'20px auto','align-items':'flex-start', 'justify-content':'flex-start'})
            subContainerADV_LV2.style['border-left'] = '3px solid rgba(0,0,0,.12)'

            self.lbl_LV2 = gui.Label('Low-Voltage 2', width=110, height=20, margin='5px',style={'font-size': '14px', 'font-weight': 'bold'})

            self.btLV2on = gui.Button('ON', width=50, height=20, margin='5px', style={'font-size': '16px', 'font-weight': 'bold','background-color': col_green})
            self.btLV2off = gui.Button('OFF', width=50, height=20, margin='5px', style={'font-size': '16px', 'font-weight': 'bold','background-color': col_red})

            self.lbl_textinput_LV2_0 = gui.Label('CH0', width=50, height=20, margin='5px',style={'font-size': '14px'})
            self.lbl_textinput_LV2_1 = gui.Label('CH1', width=50, height=20, margin='5px',style={'font-size': '14px'})

            self.textinput_LV2_0 = gui.TextInput(width=50, height=20,margin='5px')
            self.textinput_LV2_1 = gui.TextInput(width=50, height=20,margin='5px')

            self.list_textinput_LV2 = [self.textinput_LV2_0,self.textinput_LV2_1]

            for textinput in self.list_textinput_LV2:
                textinput.set_value('0.00')

            self.btLV2set = gui.Button('SET', width=50, height=50, margin='5px', style={'font-size': '16px', 'font-weight': 'bold','background-color': col_lblue})

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
            self.btLV2on.onclick.do(self.on_btLV_sw_pressed,2,'on')
            self.btLV2off.onclick.do(self.on_btLV_sw_pressed,2,'off')
            self.btLV2set.onclick.do(self.on_btLVset_pressed,2)

            #------------Chiller controls-----------
            subContainerADV_Chiller_BNL = gui.GridBox(width = "75%",hight = "100%", style={'margin':'20px','align-items':'flex-start', 'justify-content':'flex-start'})
            subContainerADV_Chiller_BNL.style['border-left'] = '3px solid rgba(0,0,0,.12)'

            self.lbl_Chiller = gui.Label('Chiller', width=110, height=20, margin='5px',style={'font-size': '14px', 'font-weight': 'bold'})

            self.btChillerOn = gui.Button('ON', width=50, height=20, margin='5px', style={'font-size': '16px', 'font-weight': 'bold','background-color': col_green})
            self.btChillerOff = gui.Button('OFF', width=50, height=20, margin='5px', style={'font-size': '16px', 'font-weight': 'bold','background-color': col_red})

            self.lbl_textinput_ChilT = gui.Label('Temperature[C]', width=50, height=20, margin='5px',style={'font-size': '14px'})

            self.textinput_ChilT = gui.TextInput(width=50, height=20,margin='5px')
            self.textinput_ChilT.set_value('0.00')

            self.btChilTset = gui.Button('SET', width=50, height=20, margin='5px', style={'font-size': '16px', 'font-weight': 'bold','background-color': col_lblue})

            subContainerADV_Chiller_BNL.set_from_asciiart("""
                |Chil_label| Chil_label  | Chil_on         | Chil_off  |
                |Chil_T    | Chil_T      | textinput_ChilT | set_ChilT |
                """, 10, 10)

            subContainerADV_Chiller_BNL.append({'Chil_label':self.lbl_Chiller, 'Chil_on':self.btChillerOn ,'Chil_off':self.btChillerOff,
                                        'Chil_T':self.lbl_textinput_ChilT,'textinput_ChilT': self.textinput_ChilT,'set_ChilT':self.btChilTset
                                        })

            self.btChillerOff.attributes["disabled"] = ""
            self.btChillerOn.onclick.do(self.on_btChiller_sw_pressed, 'on')
            self.btChillerOff.onclick.do(self.on_btChiller_sw_pressed, 'off')
            self.btChilTset.onclick.do(self.on_btChil_T_set_pressed)

            '''
            #------------Setting the values -----------
            self.btAdvSet = gui.Button('SET', width="20%", height=30, margin='15px', style={'font-size': '16px', 'font-weight': 'bold','background-color': col_blue})
            self.btAdvSet.onclick.do(self.on_btAdvSet_pressed)
            '''
            #- Wrapping the subcontainers
            subContainerADV.set_from_asciiart("""
                |TC      |HV |HV  | LV1  |  |
                |Chiller |HV |HV  | LV2  |  |

                """, 10, 10)

            subContainerADV.append({'TC':subContainerADV_TC, 'Chiller':subContainerADV_Chiller_BNL,
                                        'HV': subContainerADV_HV, 'LV1': subContainerADV_LV1, 'LV2': subContainerADV_LV2,
                                        })

            #------------------------------------------
        elif coldbox_type=='UK':
            #------------Peltiers controls-----------
            subContainerADV_plt = gui.GridBox(width = "55%", hight = "100%", style={'margin':'20px','align-items':'flex-start', 'justify-content':'flex-start'})
            subContainerADV_plt.style['border-left'] = '3px solid rgba(0,0,0,.12)'
            self.lbl_plt = gui.Label('Peltier mode', width=110, height=20, margin='5px',style={'font-size': '14px', 'font-weight': 'bold'})
            self.lbl_plt_curr = gui.Label('Current[A]', width=110, height=20, margin='5px',style={'font-size': '14px', 'font-weight': 'bold'})
            self.lbl_plt_vol = gui.Label('Voltage[V]', width=110, height=20, margin='5px',style={'font-size': '14px', 'font-weight': 'bold'})

            self.btPLT_heat = gui.Button('HEAT', width=75, height=20, margin='5px', style={'font-size': '16px', 'font-weight': 'bold','background-color': col_red})
            self.btPLT_cool = gui.Button('COOL', width=75, height=20, margin='5px', style={'font-size': '16px', 'font-weight': 'bold','background-color': col_blue})

            self.lbl_textinput_plt0 = gui.Label('Plt_1', width=50, height=20, margin='5px',style={'font-size': '14px'})
            self.lbl_textinput_plt1 = gui.Label('Plt_2', width=50, height=20, margin='5px',style={'font-size': '14px'})
            self.lbl_textinput_plt2 = gui.Label('Plt_3', width=50, height=20, margin='5px',style={'font-size': '14px'})
            self.lbl_textinput_plt3 = gui.Label('Plt_4', width=50, height=20, margin='5px',style={'font-size': '14px'})
            self.lbl_textinput_plt4 = gui.Label('Plt_5', width=50, height=20, margin='5px',style={'font-size': '14px'})

            self.textinput_curr_plt0 = gui.TextInput(width=50, height=20,margin='5px')
            self.textinput_curr_plt1 = gui.TextInput(width=50, height=20,margin='5px')
            self.textinput_curr_plt2 = gui.TextInput(width=50, height=20,margin='5px')
            self.textinput_curr_plt3 = gui.TextInput(width=50, height=20,margin='5px')
            self.textinput_curr_plt4 = gui.TextInput(width=50, height=20,margin='5px')
            self.list_textinput_curr= [self.textinput_curr_plt0,self.textinput_curr_plt1,self.textinput_curr_plt2,self.textinput_curr_plt3,self.textinput_curr_plt4]


            self.textinput_vol_plt0 = gui.TextInput(width=50, height=20,margin='5px')
            self.textinput_vol_plt1 = gui.TextInput(width=50, height=20,margin='5px')
            self.textinput_vol_plt2 = gui.TextInput(width=50, height=20,margin='5px')
            self.textinput_vol_plt3 = gui.TextInput(width=50, height=20,margin='5px')
            self.textinput_vol_plt4 = gui.TextInput(width=50, height=20,margin='5px')
            self.list_textinput_vol= [self.textinput_vol_plt0,self.textinput_vol_plt1,self.textinput_vol_plt2,self.textinput_vol_plt3,self.textinput_vol_plt4]

            self.list_textinput_plt = [self.textinput_curr_plt0, self.textinput_curr_plt1,self.textinput_curr_plt2,self.textinput_curr_plt3,self.textinput_curr_plt4,
                                       self.textinput_vol_plt0, self.textinput_vol_plt1,self.textinput_vol_plt2,self.textinput_vol_plt3,self.textinput_vol_plt4]
            for textinput in self.list_textinput_plt:
                textinput.set_value('0.00')

            self.bt_PLTset_0 = gui.Button('SET', width=50, height=20, margin='5px', style={'font-size': '16px', 'font-weight': 'bold','background-color': col_lblue})
            self.bt_PLTset_1 = gui.Button('SET', width=50, height=20, margin='5px', style={'font-size': '16px', 'font-weight': 'bold','background-color': col_lblue})
            self.bt_PLTset_2 = gui.Button('SET', width=50, height=20, margin='5px', style={'font-size': '16px', 'font-weight': 'bold','background-color': col_lblue})
            self.bt_PLTset_3 = gui.Button('SET', width=50, height=20, margin='5px', style={'font-size': '16px', 'font-weight': 'bold','background-color': col_lblue})
            self.bt_PLTset_4 = gui.Button('SET', width=50, height=20, margin='5px', style={'font-size': '16px', 'font-weight': 'bold','background-color': col_lblue})
            self.list_bt_PLTset = [self.bt_PLTset_0,self.bt_PLTset_1,self.bt_PLTset_2,self.bt_PLTset_3,self.bt_PLTset_4]

            subContainerADV_plt.set_from_asciiart("""
                |PLT_label | PLT_bt_HEAT  | PLT_bt_COOL |             |
                |          | PLT_current  | PTL_vol     |             |
                | plt0     | plt_curr0    | plt_vol0    | plt_set0    |
                | plt1     | plt_curr1    | plt_vol1    | plt_set1    |
                | plt2     | plt_curr2    | plt_vol2    | plt_set2    |
                | plt3     | plt_curr3    | plt_vol3    | plt_set3    |
                | plt4     | plt_curr4    | plt_vol4    | plt_set4    |
                """, 10, 10)

            subContainerADV_plt.append({'PLT_label':self.lbl_plt, 'PLT_bt_HEAT':self.btPLT_heat,'PLT_bt_COOL':self.btPLT_cool,
                                        'PLT_current':self.lbl_plt_curr ,'PTL_vol':self.lbl_plt_vol,
                                        'plt0':self.lbl_textinput_plt0, 'plt_curr0':self.list_textinput_curr[0] , 'plt_vol0':self.list_textinput_vol[0], 'plt_set0':self.bt_PLTset_0 ,
                                        'plt1':self.lbl_textinput_plt1, 'plt_curr1':self.list_textinput_curr[1] , 'plt_vol1':self.list_textinput_vol[1], 'plt_set1':self.bt_PLTset_1 ,
                                        'plt2':self.lbl_textinput_plt2, 'plt_curr2':self.list_textinput_curr[2] , 'plt_vol2':self.list_textinput_vol[2], 'plt_set2':self.bt_PLTset_2 ,
                                        'plt3':self.lbl_textinput_plt3, 'plt_curr3':self.list_textinput_curr[3] , 'plt_vol3':self.list_textinput_vol[3], 'plt_set3':self.bt_PLTset_3 ,
                                        'plt4':self.lbl_textinput_plt4, 'plt_curr4':self.list_textinput_curr[4] , 'plt_vol4':self.list_textinput_vol[4], 'plt_set4':self.bt_PLTset_4
            })


            self.btPLT_heat.onclick.do(self.on_btPLT_sw_pressed,'heat')
            self.btPLT_cool.onclick.do(self.on_btPLT_sw_pressed,'cool')

            for i in range(len(self.list_bt_PLTset)):
                self.list_bt_PLTset[i].onclick.do(self.on_bt_PLTset_pressed,i)

            #------------Chiller controls-----------
            subContainerADV_Chiller_UK = gui.GridBox(width = "91%",hight = "100%", style={'margin':'20px','align-items':'flex-start', 'justify-content':'flex-start'})
            subContainerADV_Chiller_UK.style['border-left'] = '3px solid rgba(0,0,0,.12)'

            self.lbl_Chiller = gui.Label('Chiller', width=50, height=20, margin='5px',style={'font-size': '14px', 'font-weight': 'bold'})

            self.lbl_textinput_ChilT = gui.Label('Temperature [C]', width=200, height=20, margin='5px',style={'font-size': '14px'})
            self.textinput_ChilT = gui.TextInput(width=50, height=20,margin='5px')
            self.textinput_ChilT.set_value('0.00')
            self.btChilTset = gui.Button('SET', width=50, height=20, margin='5px', style={'font-size': '16px', 'font-weight': 'bold','background-color': col_lblue})

            self.lbl_textinput_Chil_pumpS = gui.Label('Pump speed', width=200, height=20, margin='5px',style={'font-size': '14px'})
            self.textinput_Chil_pumpS = gui.TextInput(width=50, height=20,margin='5px')
            self.textinput_Chil_pumpS.set_value('0.00')
            self.btChil_pumpS_set = gui.Button('SET', width=50, height=20, margin='5px', style={'font-size': '16px', 'font-weight': 'bold','background-color': col_lblue})

            subContainerADV_Chiller_UK.set_from_asciiart("""
                |Chil_label | Chil_label  |                |                   |
                |Chil_T     |Chil_T       | textinput_ChilT      | set_ChilT      |
                |Chil_pumpS |Chil_pumpS   | textinput_Chil_pumpS | set_Chil_pumpS |
                """, 10, 10)

            subContainerADV_Chiller_UK.append({'Chil_label':self.lbl_Chiller,
                                        'Chil_T':self.lbl_textinput_ChilT,'textinput_ChilT': self.textinput_ChilT,'set_ChilT':self.btChilTset,
                                        'Chil_pumpS':self.lbl_textinput_Chil_pumpS,'textinput_Chil_pumpS': self.textinput_Chil_pumpS,'set_Chil_pumpS':self.btChil_pumpS_set,
                                        })
            self.btChilTset.onclick.do(self.on_btChil_T_set_pressed)
            self.btChil_pumpS_set.onclick.do(self.on_btChil_pumpS_set_pressed)


            #- Wrapping the subcontainers
            subContainerADV.set_from_asciiart("""
                |TC      |plt |plt  |  |
                |Chiller |plt |plt  |  |

                """, 10, 10)

            subContainerADV.append({'TC':subContainerADV_TC, 'Chiller':subContainerADV_Chiller_UK,
                                        'plt': subContainerADV_plt,
                                        })


        verticalContainer_tb2.append([horizontalContainer_logo, subContainerADV ])
        verticalContainer_tb2.style['justify-content'] ='space-around'
        verticalContainer_tb2.style['align-items'] = 'center'
        verticalContainer_tb2.style['margin'] = '2px'



        #===================================== TAB 3 =================================================
        self.lbl_swName = gui.Label('ColdBox Controller V 0.8', width=200, height=30, margin='5px',style={'font-size': '15px', 'font-weight': 'bold'})
        #self.lbl_coldbox_type = gui.Label('ColdBox type: '+coldbox_type , width=200, height=30, margin='5px')
        verticalContainer_tb3.append([horizontalContainer_logo, self.lbl_swName, self.lbl_ColdBoxType])

        #===================================== Wrapping all tabs together =================================================
        tabBox = gui.TabBox(width='100%',style={'align-items':'flex-start', 'justify-content':'flex-start','font-size': '16px', 'font-weight': 'bold','background-color': col_darkBlue})

        tabBox.append(verticalContainer_tb1, 'Control Panel')
        tabBox.add_tab(verticalContainer_tb2, 'Advanced', None)
        tabBox.add_tab(verticalContainer_tb3, 'About', None)

        #===================================== Grafana pannels and interlocks =====================================
        self.grafana_dash = gui.Widget( _type='iframe', width='100%', height=1000, margin='10px')
        self.grafana_dash.attributes['src'] = grf_dash
        self.grafana_dash.attributes['width'] = '100%'
        self.grafana_dash.attributes['height'] = '100%'
        self.grafana_dash.attributes['controls'] = 'true'
        self.grafana_dash.style['border'] = 'none'

        horizontalContainer_grafana_dash.append(self.grafana_dash)


        #=========================== Appending TabBox and Grafana plots to a vertical main container ======================

        self.main_container = gui.VBox(width ='100%', hight='100%', style={'align-items':'flex-start', 'justify-content':'flex-start'})

        #-- other popup boxes will be appended here once the corresponding pubsub message is received
        self.main_container.append([tabBox])

        self.ultimate_container = gui.VBox(width ='100%', hight='100%', style={'align-items':'flex-start', 'justify-content':'flex-start'})
        self.ultimate_container.append([self.main_container, horizontalContainer_grafana_dash])

        #-------------------------------------
        #-- Subscribe to messages
        pub.subscribe(self.gui_warning,'warning')
        pub.subscribe(self.gui_error,'error')
        pub.subscribe(self.gui_alert,'alert')
        pub.subscribe(self.gui_danger,'danger')


        #=== for testing pubsub only
        if testPubSub:
            def start_pubsub():
                coldjig_pubsub.start()

            #start a separate thread to listen to the subscribed messages
            th_pubsub = threading.Thread(target=start_pubsub).start()

        #-------------------------Global GUI variables
        self.availavle_chucks=[]
        self.test_type=''
        self.selected_tests=[]


        # returning the root widget
        return self.ultimate_container


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


    def on_btStartLib_pressed(self, widget):
        logger.debug("user pressed Start button")
        self.btStartLib.attributes["disabled"] = ""
        currentDT = datetime.datetime.now()
        current_text= self.statusBox.get_text()

        if(coldjigcontroller.start()):
            del self.btStopLib.attributes["disabled"]
            del self.btStartTC.attributes["disabled"]
            logger.info("Coldbox Controller is up!")
            self.statusBox.set_text(current_text+"["+currentDT.strftime("%H:%M:%S")+"] -- Coldbox Controller is up!\n")

        else:
            logger.error("Starting the coldjiglib failed!")

    def on_btStopLib_pressed(self, widget):
        logger.debug("user pressed shutdown button")
        self.Lib_term_popup_confirm.show()
        self.Lib_term_popup_confirm.onconfirm.do(self.prep_Shutdown_Lib)

    def on_btStartTC_pressed(self, widget):
        logger.debug("user pressed Start TC button")
        #total_selected_chucks, total_selected_tests, userOpt_text=self.read_user_options()
        userOpt_text = self.read_user_options()

        if len(self.availavle_chucks) <1:
            logger.error("No chuck selected!")
            self.TC_NoCh_popup_alert.show()

        elif self.test_type == 'custom' and len(self.selected_tests)<1:
                logger.error("No custom test selected!")
                self.TC_NoCusTest_popup_alert.show()
        else:
            self.btStartTC.attributes["disabled"] = ""
            self.btStopLib.attributes["disabled"] = ""
            #-- user should not be able to change TC settings while TC is running
            self.textinput_TCHot.attributes["disabled"] = ""
            self.textinput_TCCold.attributes["disabled"] = ""
            self.textinput_TCWarmup.attributes["disabled"] = ""

            currentDT = datetime.datetime.now()
            current_text= self.statusBox.get_text()

            #if(coldjigcontroller.start_thermal_cycle(self.availavle_chucks,40.0,-35.0,20.0,self.ncycle)):
            if(coldjigcontroller.start_thermal_cycle(self.availavle_chucks,
                                                    float(self.textinput_TCHot.get_text()),
                                                    float(self.textinput_TCCold.get_text()),
                                                    float(self.textinput_TCWarmup.get_text()),
                                                    self.ncycle)):
                logger.info("Thermocycling started!")
                self.statusBox.set_text(userOpt_text+"["+currentDT.strftime("%H:%M:%S")+"] -- Thermocycling started\n")

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
                del self.btStopTC.attributes["disabled"]
            else:
                logger.error("Starting thermocycling failed!")

    def on_btStopTC_pressed(self, widget):
        logger.debug("user pressed Stop TC button")
        self.TC_term_popup_confirm.show()
        self.TC_term_popup_confirm.onconfirm.do(self.Terminate_thermocycling)


    #--------- Advance buttons ----------
    ###---- HV buttons --------------
    def on_btHV_sw_pressed(self, widget, n, switch):
        if switch=='on' or switch=='On' or switch=='ON':
            if n == -1:
                self.btHVon.attributes["disabled"] = ""
                del self.btHVoff.attributes["disabled"]
                for bt in self.list_btHVon:
                    del bt.attributes["disabled"]
                for bt in self.list_btHVset:
                    del bt.attributes["disabled"]
                self.data_dict['Caen.state'] = 'ON'
                logger.info("HV switched ON")
            elif n>=0 and n<4:
                self.list_btHVon[n].attributes["disabled"] = ""
                del self.list_btHVoff[n].attributes["disabled"]
                self.data_dict['Caen.set_channel_%i'%n] = 'ON'
                logger.info("HV ch%i switched ON"%n)
                #logger.debug('data_dict: '+'Caen.set_channel_%i'%n)
            else:
                logger.info("Attempt to access invalid HV channel")

        elif switch=='off' or switch=='Off' or switch=='OFF':
            if n == -1:
                self.btHVoff.attributes["disabled"] = ""
                del self.btHVon.attributes["disabled"]
                for bt in self.list_btHV:
                    bt.attributes["disabled"]= ""
                for bt in self.list_btHVset:
                    bt.attributes["disabled"]= ""
                self.data_dict['Caen.state'] = 'OFF'
                logger.info("HV switched OFF")
            elif n>=0 and n<4:
                self.list_btHVoff[n].attributes["disabled"] = ""
                del self.list_btHVon[n].attributes["disabled"]
                self.data_dict['Caen.set_channel_%i'%n] = 'OFF'
                logger.info("HV ch%i switched OFF"%n)
                #logger.debug('data_dict: '+'Caen.set_channel_%i'%n)
            else:
                logger.info("Attempt to access invalid HV channel")
        else:
            logger.info("Invalid HV switch. Use ON or OFF.")


    def on_btHVset_pressed(self, widget, n):
        HV_val=self.list_textinput_HV[n].get_text()
        self.data_dict['Caen.set_voltge_%i'%n] = float(HV_val)
        logger.info("HV ch%i set to %s V"%(n,HV_val) )

    #---- LV buttons --------------
    def on_btLV_sw_pressed(self, widget, LVstate, switch):
        if switch=='on' or switch=='On' or switch=='ON':
            if LVstate==1:
                self.btLV1on.attributes["disabled"] = ""
                del self.btLV1off.attributes["disabled"]
                self.data_dict['LV.State_1'] = 'ON'
                logger.info("LV1 switched ON")
            elif LVstate ==2:
                self.btLV2on.attributes["disabled"] = ""
                del self.btLV2off.attributes["disabled"]
                self.data_dict['LV.State_2'] = 'ON'
                logger.info("LV2 switched ON")

        elif switch=='off' or switch=='Off' or switch=='OFF':
            if LVstate==1:
                self.btLV1off.attributes["disabled"] = ""
                del self.btLV1on.attributes["disabled"]
                self.data_dict['LV.State_1'] = 'OFF'
                logger.info("LV1 switched OFF")
            elif LVstate ==2:
                self.btLV2off.attributes["disabled"] = ""
                del self.btLV2on.attributes["disabled"]
                self.data_dict['LV.State_2'] = 'OFF'
                logger.info("LV2 switched OFF")

    def on_btLVset_pressed(self, widget,LVstate):
        if LVstate==1:
            LV1_0=self.textinput_LV1_0.get_text()
            LV1_1=self.textinput_LV1_1.get_text()
            self.data_dict['LV.set_voltge_1_0'] = float(LV1_0)
            self.data_dict['LV.set_voltge_1_1'] = float(LV1_1)
            logger.info("LV1_0 set to "+LV1_0+" V")
            logger.info("LV1_1 set to "+LV1_1+" V")

        elif LVstate==2:
            LV2_0=self.textinput_LV2_0.get_text()
            LV2_1=self.textinput_LV2_1.get_text()
            self.data_dict['LV.set_voltge_2_0'] = float(LV2_0)
            self.data_dict['LV.set_voltge_2_1'] = float(LV2_1)
            logger.info("LV2_0 set to "+LV2_0+" V")
            logger.info("LV2_1 set to "+LV2_1+" V")

    #---- Chiller buttons --------------
    def on_btChiller_sw_pressed(self, widget,switch):
        if switch=='on' or switch=='On' or switch=='ON':
            self.btChillerOn.attributes["disabled"] = ""
            del self.btChillerOff.attributes["disabled"]
            self.data_dict['chiller.set_state'] = 'ON'
            logger.info("Chiller switched ON")
        elif switch=='off' or switch=='Off' or switch=='OFF':
            self.btChillerOff.attributes["disabled"] = ""
            del self.btChillerOn.attributes["disabled"]
            self.data_dict['chiller.set_state'] = 'OFF'
            logger.info("Chiller switched OFF")

    def on_btChil_T_set_pressed(self, widget):
        ChillerT=self.textinput_ChilT.get_text()
        self.data_dict['chiller.set_temperature'] = float(ChillerT)
        logger.info("Chiller temperature set to "+ChillerT+" C")

    #------ UK Advanced slots ----------
    def on_btPLT_sw_pressed(self, widget, swith):
        if swith=="HEAT" or swith=="Heat" or swith=="heat":
            self.btPLT_heat.attributes["disabled"] = ""
            del self.btPLT_cool.attributes["disabled"]
            self.data_dict['peltier.set_mode'] = 'HEAT'
            logger.info("Peltier mode set to HEAT")

        elif swith=="COOL" or swith=="Cool" or swith=="cool":
            self.btPLT_cool.attributes["disabled"] = ""
            del self.btPLT_heat.attributes["disabled"]
            self.data_dict['peltier.set_mode'] = 'COOL'
            logger.info("Peltier mode set to COOL")
        else:
            logger.error('Attempt to set invalid Peltier mode. Use HEAT or COOL.')

    def on_bt_PLTset_pressed(self, widget, n):
        plt_curr=self.list_textinput_curr[n].get_text()
        plt_vol=self.list_textinput_vol[n].get_text()
        self.data_dict['peltier.set_current.%i'%(n+1)] = float(plt_curr)
        self.data_dict['peltier.set_volt.%i'%(n+1)] = float(plt_vol)

        logger.info("Plt %i current set to %s A"%(n+1, plt_curr))
        logger.info("Plt %i voltage set to %s V"%(n+1, plt_vol))

    def on_btChil_pumpS_set_pressed(self, widget):
        ChillerPS=self.textinput_Chil_pumpS.get_text()
        self.data_dict['chiller.set_pump'] = int(ChillerPS)
        logger.info("Chiller pump speed set to "+ChillerPS)
    #=====================WIP=================

    def on_close(self):
        """ Overloading App.on_close event allows to perform some
             activities before app termination.
        """
        print("I'm going to be closed.")
        super(ColdBoxGUI, self).on_close()

    #=========================================

    def prep_Shutdown_Lib(self, widget):
        self.btStopLib.attributes["disabled"] = ""
        self.btStartTC.attributes["disabled"] = ""
        currentDT = datetime.datetime.now()
        current_text= self.statusBox.get_text()
        self.statusBox.set_text(current_text+"["+currentDT.strftime("%H:%M:%S")+"] -- Shutting down all tasks and core_loop\n")

        self.thread_Shutdown_Lib = threading.Thread(target=self.Shutdown_Lib)
        self.thread_Shutdown_Lib.start()

    def Shutdown_Lib(self):
        if(coldjigcontroller.shutdown()):
            time.sleep(2)
            logger.info("Coldbox Controller is down!")
            del self.btStartLib.attributes["disabled"]
            currentDT = datetime.datetime.now()
            current_text= self.statusBox.get_text()
            self.statusBox.set_text(current_text+"["+currentDT.strftime("%H:%M:%S")+"] -- Coldbox Controller is down!\n")

            #-- Close the browser and terminate the webserver
            self.execute_javascript("window.close();")
            self.close()
        else:
            logger.error("Shuting down the coldjiglib failed!")
            del self.btStopLib.attributes["disabled"]

    #=====================

    def Terminate_thermocycling(self, widget):
        self.btStopTC.attributes["disabled"] = ""
        currentDT = datetime.datetime.now()
        current_text= self.statusBox.get_text()
        if(coldjigcontroller.stop_thermal_cycle()):
            logger.info("Thermocycling terminated!")
            self.statusBox.set_text(current_text+"["+currentDT.strftime("%H:%M:%S")+"] -- Thermocycling terminated!\n")
            del self.btStartTC.attributes["disabled"]
            del self.btStopLib.attributes["disabled"]
            #-- allow the user to set TC settings
            del self.textinput_TCHot.attributes["disabled"]
            del self.textinput_TCCold.attributes["disabled"]
            del self.textinput_TCWarmup.attributes["disabled"]

        #-- this is to let the user to change the values when the TC is terminated
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
        else:
            logger.error("Terminating thermocycling failed!")
            del self.btStopTC.attributes["disabled"]


    def js_notification(self,txt):
        time.sleep(0.1)
        self.execute_javascript('alert("%s")'%txt)

    def read_user_options(self):
        self.ncycle = self.spin.get_value()
        self.availavle_chucks=[]
        self.selected_tests=[]
        availavle_chucks_tmp=[]
        selected_tests_tmp=[]

        for chuck in self.list_checkBox_ch:
            availavle_chucks_tmp.append(int(chuck.get_value()) )

        for idx, val in enumerate(availavle_chucks_tmp):
            if val ==1:
                self.availavle_chucks.append(idx+1)

        logger.debug('availavle_chucks: '+str(self.availavle_chucks))
        logger.debug('total_selected_chucks: '+str(len(self.availavle_chucks)))

        if self.radioButton_stTest.get_value():
            self.test_type = 'standard'
        else:
            self.test_type = 'custom'
            for test in self.list_checkBox_t:
                selected_tests_tmp.append(int(test.get_value()) )
            for idx, val in enumerate(selected_tests_tmp):
                if val ==1:
                    self.selected_tests.append(idx+1)

            logger.debug('custom test is running: '+str(len(self.selected_tests))+' tests')

        if self.test_type == 'custom':
            #user_options = 'User options set:\n'+'-Cycles:'+ str(self.ncycle) +'\n-Available_chucks:'+str(list(map(int,self.availavle_chucks)))+'\n-Selected_test(s):'+self.selected_tests+'\n------\n'
            user_options = 'User options set:\n'+'-Cycles:'+ str(self.ncycle) +'\n-Available_chucks:'+str(self.availavle_chucks)+'\n-Selected_test(s):'+str(self.selected_tests)+'\n------\n'
        else:
            #user_options = 'User options set:\n'+'-Cycles:'+ str(self.ncycle) +'\n-Available_chucks:'+str(list(map(int,self.availavle_chucks)))+'\n-Selected_test(s): standard\n------\n'
            user_options = 'User options set:\n'+'-Cycles:'+ str(self.ncycle) +'\n-Available_chucks:'+str(self.availavle_chucks)+'\n-Selected_test(s): standard\n------\n'
        return user_options

    #------ Listener functions
    def randomMargin(self, obj, lmarg, tmarg, randInterval):
        n1 = random.randint(-1*randInterval,randInterval)
        n2 = random.randint(-1*randInterval,randInterval)
        lMarg = str(n1+lmarg)+'px'
        tMarg = str(n1+tmarg)+'px'
        obj.style['margin-left'] = lMarg
        obj.style['margin-top'] = tMarg

    def gui_warning(self, message="NOT DEFINED") :
        logger.debug(">>> Received warning message")
        logger.warning(message)
        self.popup_warning = Popup.PopupAlert("WARNING", message, '#F7AB3B')
        self.randomMargin(self.popup_warning, 600, 250, 20)
        self.main_container.append(self.popup_warning)
        self.popup_warning.show()

    def gui_error(self,message="NOT DEFINED") :
        logger.debug(">>> Received error message")
        logger.error(message)
        self.popup_error = Popup.PopupAlert("ERROR", message, '#BF33AD')
        self.randomMargin(self.popup_error, 600, 250, 20)
        self.main_container.append(self.popup_error)
        self.popup_error.show()

    def gui_alert(self,message="NOT DEFINED") :
        logger.debug(">>> Received alert message")
        logger.warning("ALERT: "+message)
        self.popup_alert = Popup.PopupAlert("ALERT", message)
        self.randomMargin(self.popup_alert, 600, 250, 20)
        self.main_container.append(self.popup_alert)
        self.popup_alert.show()

    def gui_danger(self,message="NOT DEFINED") :
        logger.debug(">>> Received danger message")
        logger.warning("DANGER: "+message)
        self.popup_danger = Popup.PopupAlert("DANGER", message, '#B10D03')
        self.randomMargin(self.popup_danger, 600, 250, 20)
        self.main_container.append(self.popup_danger)
        self.popup_danger.show()

#===========================================================================
if __name__ == "__main__":

    config = conf.ConfigParser()
    configfile = 'default'
    verbose = False # set to Fals if you dont want to print debugging info

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
        #logger.error('option requires argument.\n Usage: blah -c configFile \n Process terminated.')
        print('option requires argument.\n Usage: blah -c configFile \n Process terminated.')
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
        #logger.error("Attempt to start the GUI without user config.\n Process terminated.")
        print("Attempt to start the GUI without user config.\n Process terminated.")
        sys.exit(1)

    else:
        if os.path.isfile(configfile):
            config.read(configfile)
        else:
            #logger.error('Config file does not exist.\n Process terminated.')
            print('Config file does not exist.\n Process terminated.')
            sys.exit(1)


    # set up logging from logging ini file
    timestr = time.strftime("%Y%m%d-%H%M%S")
    logFile_name = 'log/'+timestr+'_ColdJigGUI.log'

    LOG_INI_FILE = config['COLDBOX']['LOG_INI_FILE']
    #logging.config.fileConfig(LOG_INI_FILE)
    logging.config.fileConfig(LOG_INI_FILE, defaults={'logfilename': logFile_name})

    logger = logging.getLogger('GUIlogger')

    logger.info("Starting ColdJig GUI")
    logger.info('Reading config file: '+configfile)

    #--- reading config values
    gui_server = config['SERVER']['gui_server']
    gui_server_port = int(config['SERVER']['gui_server_port'])

    coldbox_type = config['COLDBOX']['coldbox_type']
    n_chucks = int(config['COLDBOX']['n_chucks'])
    coldBox_controller = config['COLDBOX']['controller']
    HW_INI_FILE        = config['COLDBOX']['HW_INI_FILE']
    INFLUX_INI_FILE    = config['COLDBOX']['INFLUX_INI_FILE']
    INTERLOCK_ACTION   = config['COLDBOX']['INTERLOCK_ACTION']
    THERMAL_CYCLE_MODULE = config['COLDBOX']['THERMAL_CYCLE_MODULE']
    controller_RATE    = float(config['COLDBOX']['controller_RATE'])

    gui_debug = config['GUI']['gui_debugging_mode']
    gui_start_browser = config['GUI']['gui_start_browser']
    gui_multiple_instance = config['GUI']['gui_multiple_instance']
    gui_enable_file_cache = config['GUI']['gui_enable_file_cache']
    gui_update_interval = float(config['GUI']['gui_update_interval'])

    grf_dash= config['GRAFANA']['dash']

    logger.debug('gui_server= '+gui_server)
    logger.debug('gui_port= '+str(gui_server_port))

    logger.debug('coldbox_type= '+coldbox_type)
    logger.debug('n_chucks= '+str(n_chucks))
    logger.debug('controller= '+str(coldBox_controller))
    logger.debug('HW_INI_FILE= '+HW_INI_FILE)
    logger.debug('INFLUX_INI_FILE= '+INFLUX_INI_FILE)
    logger.debug('INTERLOCK_ACTION= '+INTERLOCK_ACTION)
    logger.debug('controller_RATE= '+str(controller_RATE))

    logger.debug('gui_debug= '+str(gui_debug))
    logger.debug('gui_start_browser= '+str(gui_start_browser))
    logger.debug('gui_multiple_instance= '+str(gui_multiple_instance))
    logger.debug('gui_enable_file_cache= '+str(gui_enable_file_cache))
    logger.debug('gui_update_interval= '+str(gui_update_interval))

    logger.debug('grf_dash='+ str(grf_dash))

    #-- checking number of chucks--
    if not (n_chucks==5 or n_chucks==4):
        logger.error('Number of chucks is not supported. Set n_chucks in config file to 4 or 5.')
        sys.exit(1)

    #--- initializing the coldjigcontroller
    coldjigcontroller = None
    try:
        coldjigcontroller = importlib.import_module(coldBox_controller)
    except ImportError:
        logger.critical('could not import controller library -- check COLDBOX.controller option of config file')
        sys.exit(1)

    if coldjigcontroller is None:
        logger.critical('failed to create an instance of the controller')
        sys.exit(1)

    coldjigcontroller.hardware_ini_file = HW_INI_FILE
    coldjigcontroller.influx_ini_file = INFLUX_INI_FILE
    coldjigcontroller.interlock_action_module = INTERLOCK_ACTION
    coldjigcontroller.thermal_cycle_module = THERMAL_CYCLE_MODULE
    coldjigcontroller.RATE = controller_RATE
    #-----------

    #-- use this for debugging purpose. The app will exit after loading the configs
    #exit()


    #--starts the webserver / optional parameters
    #start(ColdBoxGUI, update_interval=0.5, debug=gui_debug, address=gui_server, port=gui_server_port, start_browser=gui_start_browser, multiple_instance=gui_multiple_instance, enable_file_cache=gui_enable_file_cache)
    start(ColdBoxGUI, update_interval=gui_update_interval, debug=gui_debug, address=gui_server, port=gui_server_port, start_browser=gui_start_browser, multiple_instance=gui_multiple_instance, enable_file_cache=gui_enable_file_cache, username=None, password=None)
