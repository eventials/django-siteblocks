#!/usr/bin/env python
import os
import sys
import django

if __name__ == "__main__":
    sys.path.append("./")
    sys.path.append("./examples")
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django-siteblocks-project.settings")

    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)


