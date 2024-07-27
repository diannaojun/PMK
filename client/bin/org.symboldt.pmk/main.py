#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import sys, getopt
import PackageManager


def main(argv):
    def show_help():
        print("ask for help -h/--help")
        print("install -i/--install <package_id>")
        print("update -u/--update <package_id>")
        print("uninstall -r/--remove <package_id>")
        print("list all packages -l/--list")
        print("list all hubs --list_hub")
        print("list all packages installed --list_installed")
    try:
        opts, args = getopt.getopt(argv,"hli:u:r:c:",
            ["help","install=","remove=","update=","list","list_installed","list_hub","check="])
    except getopt.GetoptError:
        show_help()
        sys.exit(2)
    if len(opts)==0:
        show_help()
        sys.exit()
    for opt, arg in opts:
        if opt in ('-h','--help'):
            show_help()
            sys.exit()
        elif opt in ("-i", "--install"):
            pmk=PackageManager.PackageManager()
            pmk.install_package(arg)
            del pmk
        elif opt in ("-r", "--remove"):
            pmk=PackageManager.PackageManager()
            pmk.uninstall_package(arg)
            del pmk
        elif opt in ("-u", "--update"):
            pmk=PackageManager.PackageManager()
            pmk.update_package(arg)
            del pmk
        elif opt in ("-c", "--check"):
            pmk=PackageManager.PackageManager()
            print(pmk.get_installed(arg))
            del pmk
        elif opt in ("-l", "--list"):
            pmk=PackageManager.PackageManager()
            pmk.list_packages()
            del pmk
        elif opt in ("--list_hub"):
            pmk=PackageManager.PackageManager()
            pmk.list_hubs()
            del pmk
        elif opt in ("--list_installed"):
            pmk=PackageManager.PackageManager()
            pmk.list_installed_packages()
            del pmk
        else:
            show_help()
            sys.exit(2)

if __name__ == "__main__":
    main(sys.argv[1:])
