

def read_conf(config):
    # -- default vaues ---
    gui_server = 'localhost'
    gui_server_port = 5000
    influx_server = 'localhost'
    influx_port = 8086
    influx_user = 'admin'
    influx_pass = ''
    influx_database ='defaultDB'

    coldbox_type = 'Default'
    n_chucks = 5
    plt_field = True

    gui_debug = False
    gui_start_browser = True
    gui_multiple_instance = False
    gui_enable_file_cache = False
    # ------------------------

    grf_panel_list=[]
    grf_intl_list=[]

    # Read configuration file
    for sec in config.sections():
        if sec == 'SERVER':
            for param in config[sec]:
                if param == 'gui_server':
                    gui_server = config[sec][param]
                elif param == 'gui_server_port':
                    gui_server_port = config[sec][param]
                elif param == 'influx_server':
                    influx_server = config[sec][param]
                elif param == 'influx_port':
                    influx_port = config[sec][param]
                elif param == 'influx_user':
                    influx_user = config[sec][param]
                elif param == 'influx_pass':
                    influx_pass = config[sec][param]
                elif param == 'influx_database':
                    influx_database = config[sec][param]

        if sec == 'COLDBOX':
            for param in config[sec]:
                if param == 'coldbox_type':
                    coldbox_type = config[sec][param]
                elif param == 'n_chucks':
                    n_chucks = int(config[sec][param],10)
                elif param == 'plt_field':
                    plt_field = (config[sec][param] == "True")


        if sec == 'GRAFANA':
            for param in config[sec]:
                if param.startswith('panel'):
                    grf_panel_list.append(config[sec][param])
                elif param.startswith('intl'):
                    grf_intl_list.append(config[sec][param])

        if sec == 'GUI':
            for param in config[sec]:
                if param == 'gui_debugging_mode':
                    gui_debug = (config[sec][param] == "True")
                elif param == 'gui_start_browser':
                    gui_start_browser = (config[sec][param] == "True")
                elif param == 'gui_multiple_instance':
                    gui_multiple_instance = (config[sec][param] == "True")
                elif param == 'gui_enable_file_cache':
                    gui_enable_file_cache = (config[sec][param] == "True")

        config_dic = {
            "gui_server": gui_server,
            "gui_server_port": int(gui_server_port),
            "coldbox_type": coldbox_type,
            "n_chucks": int(n_chucks),
            "plt_field": plt_field,
            "grf_panel_list": grf_panel_list,
            "grf_intl_list": grf_intl_list,
            "gui_debug": gui_debug,
            "gui_start_browser": gui_start_browser,
            "gui_multiple_instance": gui_multiple_instance,
            "gui_enable_file_cache": gui_enable_file_cache
        }

        config_influx = {
            "influx_server": influx_server,
            "influx_port": influx_port,
            "influx_user": influx_user,
            "influx_pass": influx_pass,
            "influx_database": influx_database,
        }

    return config_dic, config_influx
