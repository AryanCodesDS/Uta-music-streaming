#!/bin/bash
celery -A main:celery_app worker --loglevel INFO