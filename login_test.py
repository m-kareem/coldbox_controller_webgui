import remi.gui as gui
from remi.gui import *
from remi import start, App
import random
import threading
import user_manager
from user_manager import *

class CookieInterface(gui.Tag, gui.EventSource):
    def __init__(self, remi_app_instance, **kwargs):
        super(CookieInterface, self).__init__(**kwargs)
        gui.EventSource.__init__(self)
        self.app_instance = remi_app_instance
        self.EVENT_ONCOOKIES = "on_cookies"
        self.cookies = {}

    def request_cookies(self):
        self.app_instance.execute_javascript("""
            var aKeys = document.cookie.replace(/((?:^|\s*;)[^\=]+)(?=;|$)|^\s*|\s*(?:\=[^;]*)?(?:\1|$)/g, "").split(/\s*(?:\=[^;]*)?;\s*/);
            var result = {};
            for (var nLen = aKeys.length, nIdx = 0; nIdx < nLen; nIdx++) {
                var key = decodeURIComponent(aKeys[nIdx]);
                result[key] = decodeURIComponent(document.cookie.replace(new RegExp("(?:(?:^|.*;)\\s*" + encodeURIComponent(key).replace(/[\-\.\+\*]/g, "\\$&") + "\\s*\\=\\s*([^;]*).*$)|^.*$"), "$1")) || null;
            }
            sendCallbackParam('%s','%s', result);
            """%(self.identifier, self.EVENT_ONCOOKIES))

    @gui.decorate_event
    def on_cookies(self, **value):
        self.cookies = value
        return (value,)

    def remove_cookie(self, key, path='/', domain=''):
        if not key in self.cookies.keys():
            return
        self.app_instance.execute_javascript( """
            var sKey = "%(sKey)s";
            var sPath = "%(sPath)s";
            var sDomain = "%(sDomain)s";
            document.cookie = encodeURIComponent(sKey) + "=; expires=Thu, 01 Jan 1970 00:00:00 GMT" + (sDomain ? "; domain=" + sDomain : "") + (sPath ? "; path=" + sPath : "");
            """%{'sKey': key, 'sPath': path, 'sDomain': domain} )

    def set_cookie(self, key, value, expiration='Infinity', path='/', domain='', secure=False):
        """
        expiration (int): seconds after with the cookie automatically gets deleted
        """

        secure = 'true' if secure else 'false'
        self.app_instance.execute_javascript("""
            var sKey = "%(sKey)s";
            var sValue = "%(sValue)s";
            var vEnd = eval("%(vEnd)s");
            var sPath = "%(sPath)s";
            var sDomain = "%(sDomain)s";
            var bSecure = %(bSecure)s;
            if( (!sKey || /^(?:expires|max\-age|path|domain|secure)$/i.test(sKey)) == false ){
                var sExpires = "";
                if (vEnd) {
                    switch (vEnd.constructor) {
                        case Number:
                            sExpires = vEnd === Infinity ? "; expires=Fri, 31 Dec 9999 23:59:59 GMT" : "; max-age=" + vEnd;
                        break;
                        case String:
                            sExpires = "; expires=" + vEnd;
                        break;
                        case Date:
                            sExpires = "; expires=" + vEnd.toUTCString();
                        break;
                    }
                }
                document.cookie = encodeURIComponent(sKey) + "=" + encodeURIComponent(sValue) + sExpires + (sDomain ? "; domain=" + sDomain : "") + (sPath ? "; path=" + sPath : "") + (bSecure ? "; secure" : "");
            }
            """%{'sKey': key, 'sValue': value, 'vEnd': expiration, 'sPath': path, 'sDomain': domain, 'bSecure': secure})

'''
class User(object):
    USER_LEVEL_NOT_AUTHENTICATED = 0
    USER_LEVEL_USER = 1
    USER_LEVEL_ADMIN = 2

    def __init__(self, username, pwd, user_level=0):
        self.username = username
        self.pwd = pwd
        self.user_level = user_level
'''

class LoginManager(gui.Tag, gui.EventSource):
    """
    Login manager class allows to simply manage user access safety by session cookies
    It requires a cookieInterface instance to query and set user session id
    When the user login to the system you have to call
        login_manager.renew_session() #in order to force new session uid setup

    The session have to be refreshed each user action (like button click or DB access)
    in order to avoid expiration. BUT before renew, check if expired in order to ask user login

        if not login_manager.expired:
            login_manager.renew_session()
            #RENEW OK
        else:
            #UNABLE TO RENEW
            #HAVE TO ASK FOR LOGIN

    In order to know session expiration, you should register to on_session_expired event
        on_session_expired.do(mylistener.on_user_logout)
    When this event happens, ask for user login
    """
    def __init__(self, user_dictionary, cookieInterface, session_timeout_seconds = 60, **kwargs):
        #user_dictionary is a  dictionary (the key is the username,
        # the value is a User instance) have to be a list of users, can be loaded or other data sources
        super(LoginManager, self).__init__(**kwargs)
        gui.EventSource.__init__(self)
        self.user_dictionary = user_dictionary
        self.user_logged_instance = None
        self.session_uid = str(random.randint(1,999999999))
        self.cookieInterface = cookieInterface
        self.session_timeout_seconds = session_timeout_seconds
        self.timer_request_cookies() #starts the cookie refresh
        self.timeout_timer = None #checks the internal timeout

    def timer_request_cookies(self):
        self.cookieInterface.request_cookies()
        threading.Timer(self.session_timeout_seconds/10.0, self.timer_request_cookies).start()

    @gui.decorate_event
    def on_session_expired(self):
        self.user_logged_instance = None
        return ()

    def renew_session(self):
        """Have to be called on user actions to check and renew session
        """
        if ((not 'user_uid' in self.cookieInterface.cookies) or self.cookieInterface.cookies['user_uid']!=self.session_uid) and (not (self.user_logged_instance==None)):
            self.on_session_expired()

        if self.user_logged_instance == None:
            self.session_uid = str(random.randint(1,999999999))

        self.cookieInterface.set_cookie('user_uid', self.session_uid, str(self.session_timeout_seconds))

        #here we renew the internal timeout timer
        if self.timeout_timer:
            self.timeout_timer.cancel()
        self.timeout_timer = threading.Timer(self.session_timeout_seconds, self.on_session_expired)
        self.timeout_timer.start()

    def login(self, username, pwd):
        #returns None if not authenticated or a User instance, with the proper user_level
        self.user_dictionary = user_manager.load_user_dic()
        if username in self.user_dictionary.keys():
            #if pwd == self.user_dictionary[username].pwd:
            if pwd == user_manager.get_user_pwd(username):
                print("password ok")
                self.user_logged_instance = self.user_dictionary[username]
                self.renew_session()
                return self.user_dictionary[username] #self.user_logged_instance
        return None

    '''
    def add_user(self, user):
        #add a new user that can login, you can save it to a database
        self.user_dictionary[user.username] = user
    '''

class ContainerProxy():
    #given a container, this class allows to append widgets to it, keeping memory about widget user level.
    # when user level changes, this class hides or shows children widgets properly
    def __init__(self, container):
        self.container = container
        self.widgets_dictionary = {}

    def append(self, user_level, widget, key=None):
        key = self.container.append(widget, key)
        #here we store for each widget, the minimum user level for which it have to be visible
        self.widgets_dictionary[key] = {'widget':widget, 'user_level':user_level}

    def set_logged_user_level(self, user_level = user_manager.User.USER_LEVEL_NOT_AUTHENTICATED):
        self.user_level = user_level
        for widget_id in self.widgets_dictionary.keys():
            if self.widgets_dictionary[widget_id]['user_level'] > self.user_level:
                #here we replace the widget to hide in order to mantain a placeholder
                self.container.append(gui.Widget(style={'display':'none', 'width':'0px', 'height':'0px'}), widget_id)
            else:
                #here we put again the widget on the interface, the placeholder gets replaced because the same kay is used to append
                self.container.append(self.widgets_dictionary[widget_id]['widget'], widget_id)


class MyApp(App):
    def __init__(self, *args, **kwargs):
        super(MyApp, self).__init__(*args, static_file_path='./res/')

    def idle(self):
        #idle function called every update cycle
        pass

    def main(self):
        main_container = Container(margin="0px auto")
        self.container_proxy = ContainerProxy(main_container)
        main_container.attributes.update({"editor_baseclass":"Container","editor_tag_type":"widget","editor_newclass":"False","editor_constructor":"()","class":"Container","editor_varname":"main_container"})
        main_container.style.update({"width":"580.0px","position":"relative","overflow":"auto","height":"500.0px"})
        user_area_container = Container()
        user_area_container.attributes.update({"editor_baseclass":"Container","editor_tag_type":"widget","editor_newclass":"False","editor_constructor":"()","class":"Container","editor_varname":"user_area_container"})
        user_area_container.style.update({"width":"260.0px","border-style":"dotted","border-width":"1px","position":"absolute","top":"40.0px","left":"20.0px","margin":"0px","overflow":"auto","height":"440.0px"})
        lbl_user_panel = Label('User panel')
        lbl_user_panel.attributes.update({"editor_baseclass":"Label","editor_tag_type":"widget","editor_newclass":"False","editor_constructor":"('User panel')","class":"Label","editor_varname":"lbl_user_panel"})
        lbl_user_panel.style.update({"width":"100px","position":"absolute","top":"20.0px","left":"20.0px","margin":"0px","overflow":"auto","height":"30px"})
        user_area_container.append(lbl_user_panel,'lbl_user_panel')
        #main_container.append(user_area_container,'user_area_container')
        self.container_proxy.append(user_manager.User.USER_LEVEL_USER, user_area_container,'user_area_container')
        user_auth_container = HBox()
        user_auth_container.attributes.update({"editor_baseclass":"HBox","editor_tag_type":"widget","editor_newclass":"False","editor_constructor":"()","class":"HBox","editor_varname":"user_auth_container"})
        user_auth_container.style.update({"right":"1px","align-items":"center","visibility":"visible","height":"35px","overflow":"auto","top":"1px","flex-direction":"row","width":"300px","justify-content":"space-around","position":"absolute","margin":"0px","display":"flex"})
        bt_user_login = Button('login')
        bt_user_login.attributes.update({"editor_baseclass":"Button","editor_tag_type":"widget","editor_newclass":"False","editor_constructor":"('login')","class":"Button","editor_varname":"bt_user_login"})
        bt_user_login.style.update({"width":"100px","position":"static","top":"20px","order":"2","margin":"0px","overflow":"auto","height":"30px"})
        bt_user_login.onclick.do(self.on_prompt_login)
        self.bt_user_login = bt_user_login
        user_auth_container.append(bt_user_login,'bt_user_login')
        user_name = Label('not logged in')
        user_name.attributes.update({"editor_baseclass":"Label","editor_tag_type":"widget","editor_newclass":"False","editor_constructor":"('not logged in')","class":"Label","editor_varname":"user_name"})
        user_name.style.update({"width":"100px","font-weight":"bold","position":"static","top":"20px","order":"1","margin":"0px","overflow":"auto","height":"30px"})
        self.user_name = user_name
        user_auth_container.append(user_name,'user_name')
        bt_user_logout = Button('logout')
        bt_user_logout.attributes.update({"editor_baseclass":"Button","editor_tag_type":"widget","editor_newclass":"False","editor_constructor":"('logout')","class":"Button","editor_varname":"bt_user_logout"})
        bt_user_logout.style.update({"visibility":"visible","height":"30px","overflow":"auto","top":"20px","order":"3","width":"100px","position":"static","margin":"0px","display":"none","background-color":"#fa3200"})
        bt_user_logout.onclick.do(self.on_logout)
        self.bt_user_logout = bt_user_logout
        user_auth_container.append(bt_user_logout,'bt_user_logout')
        main_container.append(user_auth_container,'user_auth_container')
        admin_area_container = Container(layout_orientation=gui.Container.LAYOUT_VERTICAL)
        admin_area_container.attributes.update({"editor_baseclass":"Container","editor_tag_type":"widget","editor_newclass":"False","editor_constructor":"()","class":"Container","editor_varname":"admin_area_container"})
        admin_area_container.style.update({"border-color":"#030303","height":"440.0px","border-style":"dotted","overflow":"auto","top":"40.0px","border-width":"1px","width":"260.0px","position":"absolute","margin":"0px","left":"300.0px"})
        lbl_admin_panel = Label('Accounts management',margin='10px',style={'font-size': '15px', 'font-weight': 'bold'})
        #lbl_admin_panel.attributes.update({"editor_baseclass":"Label","editor_tag_type":"widget","editor_newclass":"False","editor_constructor":"('Administration panel')","class":"Label","editor_varname":"lbl_admin_panel"})
        #lbl_admin_panel.style.update({"width":"158px","position":"absolute","top":"20.0px","left":"20.0px","margin":"0px","overflow":"auto","height":"27px"})
        #----------------------------
        bt_addNewUser = Button('Add new user',width=200, height=30, margin='10px')
        bt_addNewUser.onclick.do(self.on_bt_addNewUser_pressed)

        bt_EditUser = Button('Edit user credentials',width=200, height=30, margin='10px')
        bt_EditUser.onclick.do(self.on_bt_EditUser_pressed)

        bt_delUser = Button('Delete user',width=200, height=30, margin='10px')
        bt_delUser.onclick.do(self.on_bt_delUser_pressed)

        self.lbl_admin_panel_message = Label(" ",margin='10px',style={'font-size': '15px', 'color': 'red'})

        admin_area_container.append([lbl_admin_panel,bt_addNewUser,bt_EditUser,bt_delUser, self.lbl_admin_panel_message])
        #----------------------------

        self.container_proxy.append(user_manager.User.USER_LEVEL_ADMIN, admin_area_container,'admin_area_container')

        #example_users = {}
        #example_users['admin'] = user_manager.User('admin', 'adminp', user_manager.User.USER_LEVEL_ADMIN)
        #example_users['user'] = user_manager.User('user', 'userp', user_manager.User.USER_LEVEL_USER)
        self.users_dic = user_manager.load_user_dic()
        self.login_manager = LoginManager(self.users_dic, CookieInterface(self), 60*60) #autologout 1 hour (60 seconds x 60 minutes)
        self.login_manager.on_session_expired.do(self.on_logout)

        self.main_container = main_container
        self.on_logout(None)
        return self.main_container


    #================================== Functions =====================================

    def on_bt_addNewUser_pressed(self, widget):
        #print("bt_addNewUser_pressed!")
        self.lbl_admin_panel_message.set_text('')
        self.addNewUser_dialog = gui.GenericDialog("Add new user", "Type here the user info", width=300)
        username_input = gui.Input(width=250)
        password_input = gui.Input(input_type='password', width=250)
        user_level_input = gui.DropDown.new_from_list(('Admin','Operator','guest'), width=200, height=20, margin='8px')
        password_input.attributes['type'] = 'password'
        self.addNewUser_dialog.add_field_with_label('username', 'Username', username_input)
        self.addNewUser_dialog.add_field_with_label('password', 'Password', password_input)
        self.addNewUser_dialog.add_field_with_label('userlevel', 'User level', user_level_input)

        self.addNewUser_dialog.confirm_dialog.do(self.on_addNewUser_confirm)
        self.addNewUser_dialog.show(self)


    def on_addNewUser_confirm(self, emitter):
        username = self.addNewUser_dialog.get_field('username').get_value()
        password = self.addNewUser_dialog.get_field('password').get_value()
        userlevel_text = self.addNewUser_dialog.get_field('userlevel').get_value()
        if user_manager.add_new_user(username, password, self.userlevel_convert(userlevel_text)):
            self.lbl_admin_panel_message.set_text('user \'' + username + '\' is added successfully')

    #-------------------
    def on_bt_EditUser_pressed(self, widget):
        #print("bt_EditUser_pressed!")
        self.lbl_admin_panel_message.set_text('')
        self.EditUser_dialog = gui.GenericDialog("Edit user credential", "Type here the user info", width=300)
        username_input = gui.Input(width=250)
        password_input = gui.Input(input_type='password', width=250)
        user_level_input = gui.DropDown.new_from_list(('Admin','Operator','guest'), width=200, height=20, margin='8px')
        password_input.attributes['type'] = 'password'
        self.EditUser_dialog.add_field_with_label('username', 'Username', username_input)
        self.EditUser_dialog.add_field_with_label('password', 'Password', password_input)
        self.EditUser_dialog.add_field_with_label('userlevel', 'User level', user_level_input)

        self.EditUser_dialog.confirm_dialog.do(self.on_EditUser_confirm)
        self.EditUser_dialog.show(self)

    def on_EditUser_confirm(self, emitter):
        username = self.EditUser_dialog.get_field('username').get_value()
        password = self.EditUser_dialog.get_field('password').get_value()
        userlevel_text = self.EditUser_dialog.get_field('userlevel').get_value()
        if user_manager.set_user_credential(username, password, self.userlevel_convert(userlevel_text)):
            self.lbl_admin_panel_message.set_text('user \'' + username + '\' is updated successfully')
    #--------------

    def on_bt_delUser_pressed(self, widget):
        #print("bt_delUser_pressed!")
        self.lbl_admin_panel_message.set_text('')
        self.delUser_dialog = gui.GenericDialog("Delete user", "Type here the user info", width=300)
        username_input = gui.Input(width=250)
        self.delUser_dialog.add_field_with_label('username', 'Username', username_input)

        self.delUser_dialog.confirm_dialog.do(self.on_delUser_confirm)
        self.delUser_dialog.show(self)

    def on_delUser_confirm(self, emitter):
        username = self.delUser_dialog.get_field('username').get_value()
        if user_manager.delete_user(username):
            self.lbl_admin_panel_message.set_text('user \'' + username + '\' is deleted successfully')
    #--------------

    def userlevel_convert(self, userlevel_text):
        if userlevel_text == 'Admin':
            userlevel=2
        elif userlevel_text == 'Operator':
            userlevel=1
        elif userlevel_text == 'guest':
            userlevel=0
        else:
            userlevel=None

        return userlevel
    #--------------

    def on_prompt_login(self, emitter):
        self.login_dialog = gui.GenericDialog("Login", "Type here login data", width=300)
        username_input = gui.Input(width=250)
        password_input = gui.Input(input_type='password', width=250)
        password_input.attributes['type'] = 'password'
        self.login_dialog.add_field_with_label('username', 'Username', username_input)
        self.login_dialog.add_field_with_label('password', 'Password', password_input)

        self.login_dialog.confirm_dialog.do(self.on_login_confirm)
        self.login_dialog.show(self)

    def on_login_confirm(self, emitter):
        #username = self.login_dialog.get_field('username').get_value()
        username = self.login_dialog.get_field('username').get_value().lower()
        password = self.login_dialog.get_field('password').get_value()
        user = self.login_manager.login(username, password)
        if user != None:
            print("logged in")
            self.user_name.set_text("hello " + user.username)
            self.bt_user_login.style['display'] = 'none'
            self.bt_user_logout.style['display'] = 'inline'
            self.container_proxy.set_logged_user_level(user.user_level)
            self.lbl_admin_panel_message.set_text('')

    def on_renew(self, emitter):
        #THIS METHOD HAVE TO BE CALLED EACH TIME A USER DOES SOMETHING ON THE INTERFACE
        # IT IS TO SAY EACH "INTERACTION" to keep the access alive, otherwise the user will be disconnected after a timeout
        #if the user is still logged in
        if not self.login_manager.user_logged_instance is None:
            self.login_manager.renew_session()
        else:
            self.on_logout(None)

    def on_logout(self, emitter):
        self.bt_user_login.style['display'] = 'inline'
        self.bt_user_logout.style['display'] = 'none'
        self.user_name.set_text("not logged in")
        self.container_proxy.set_logged_user_level()


if __name__ == "__main__":
    # starts the webserver
    start(MyApp, address='localhost', port=5000, start_browser=True, multiple_instance=True, debug=False)
