#!/usr/bin/python3

import os


class Static_Helpers:

    @staticmethod
    def exit_status_os_system(command):
        success = command.__bool__() == False
        return 0 if success == True else 1


if __name__ == "__main__":

    success = os.system("touch a.py ; rm a.py ; rm a.py")
    failed = os.system("rm nonexistent.py")
    print("Success", Static_Helpers.exit_status_os_system(success))
    print("Failed", Static_Helpers.exit_status_os_system(failed))
