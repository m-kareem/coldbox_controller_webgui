
def read_conf(config):
    str_server = 'localhost'
    coldbox_type = 'Default'
    n_chucks = 5
    plt_field = True
    gui_debug = False
    grf_panel_list=[]
    grf_intl_list=[]
    # Read configuration file
    for sec in config.sections():
        if sec == 'SERVER':
            for param in config[sec]:
                str_server = config[sec][param]

        if sec == 'COLDBOXTYPE':
            for param in config[sec]:
                if param == 'coldbox_type':
                    coldbox_type = config[sec][param]

        if sec == 'CHUCKS':
            for param in config[sec]:
                if param == 'n_chucks':
                    n_chucks = int(config[sec][param],10)

        if sec == 'PELTIERS':
            for param in config[sec]:
                if param == 'plt_field':
                    plt_field = (config[sec][param] == "True")


        if sec == 'GRAFANA':
            for param in config[sec]:
                if param.startswith('panel'):
                    grf_panel_list.append(config[sec][param])
                elif param.startswith('intl'):
                    grf_intl_list.append(config[sec][param])

        if sec == 'GUI':
            for param in config[sec]:
                if param == 'debugging_mode':
                    gui_debug = (config[sec][param] == "True")

    return str_server, coldbox_type, n_chucks, plt_field, grf_panel_list, grf_intl_list, gui_debug
