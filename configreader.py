
def read_conf(config):
    inst_name = 'Default'
    n_chucks = 5
    plt_field = True
    gui_debug = False
    # Read configuration file
    for sec in config.sections():
        if sec == 'INSTITUTE':
            for param in config[sec]:
                if param == 'inst_name':
                    inst_name = config[sec][param]

        if sec == 'CHUCKS':
            for param in config[sec]:
                if param == 'n_chucks':
                    n_chucks = int(config[sec][param],10)

        if sec == 'PELTIERS':
            for param in config[sec]:
                if param == 'plt_field':
                    plt_field = (config[sec][param] == "True")

        if sec == 'GUI':
            for param in config[sec]:
                if param == 'debugging_mode':
                    gui_debug = (config[sec][param] == "True")

    return inst_name, n_chucks, plt_field, gui_debug
