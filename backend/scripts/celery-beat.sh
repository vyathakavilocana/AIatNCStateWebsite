#!/bin/sh

set -e

celery -A config beat -l info -s /vol/web/celerbybeat-schedule.db
