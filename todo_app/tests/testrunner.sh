#!/bin/bash 
pytest /srv/www/tests/
curl -X POST --data-urlencode "payload={\"channel\": \"#buildstatus\", \"username\": \"Build Status\", \"text\": \"A change to the directory structure was noticed and you need to check your build logs @/srv/www/logs\", \"icon_emoji\": \":eight_spoked_asterisk:\"}" https://hooks.slack.com/services/$SLACKURL
