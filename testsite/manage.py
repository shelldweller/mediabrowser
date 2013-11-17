#!/usr/bin/env python
import os
import sys

mb_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, mb_dir)

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "testsite.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
