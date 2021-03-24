#!/bin/sh

set -e

celery -A config beat -l info -s /var/web/celerbybeat-schedule.db
