#!/bin/sh

set -e

celery -A config worker -l info
