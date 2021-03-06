#!/usr/bin/env python

import os
import sys

## GETTING-STARTED: make sure the next line points to your settings.py:
import traceback

os.environ['DJANGO_SETTINGS_MODULE'] = 'cnto.settings'

## GETTING-STARTED: make sure the next line points to your django project dir:
if 'OPENSHIFT_REPO_DIR' in os.environ:
    sys.path.append(os.path.join(os.environ['OPENSHIFT_REPO_DIR'], 'libs'))
    sys.path.append(os.path.join(os.environ['OPENSHIFT_REPO_DIR'], 'wsgi', 'cnto'))

    from distutils.sysconfig import get_python_lib

    os.environ['PYTHON_EGG_CACHE'] = get_python_lib()

import django
from cnto_warnings.models import MemberWarning
from cnto_warnings.warning_utils import add_and_update_low_attendance_for_previous_cycle, \
    add_and_update_mod_assessment_due, \
    add_and_update_grunt_qualification_due, send_warning_emails, add_and_update_contribution_about_to_expire, \
    send_exception_email, add_absence_monitoring_warnings, allocate_ranks_and_add_warnings_for_previous_cycle

if __name__ == "__main__":

    django.setup()

    start_count = MemberWarning.objects.all().count()

    print("Adding and updating warnings...")
    try:
        allocate_ranks_and_add_warnings_for_previous_cycle()
        add_and_update_low_attendance_for_previous_cycle()
        add_and_update_mod_assessment_due()
        add_and_update_grunt_qualification_due()
        add_and_update_contribution_about_to_expire()
        add_absence_monitoring_warnings()
    except Exception as e:
        send_exception_email(str(traceback.format_exc()))
        raise

    end_count = MemberWarning.objects.all().count()

    if start_count < end_count:
        print("Added %s warnings!" % (end_count - start_count))
    elif end_count < start_count:
        print("Removed %s warnings!" % (start_count - end_count))
    else:
        print("No change to warnings!")

    try:
        print("Sending emails...")
        send_warning_emails()
    except Exception as e:
        send_exception_email(str(traceback.format_exc()))
        raise
