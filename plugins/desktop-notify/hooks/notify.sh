#!/bin/bash
# Claude Code notification hook - sends desktop notifications via notify-send

input=$(cat)

message=$(echo "$input" | jq -r '.message // "Claude Code needs attention"')
notification_type=$(echo "$input" | jq -r '.notification_type // "general"')

# Set urgency based on notification type
# TODO notifications don't work with timeouts and any other urgency than "low"
#case "$notification_type" in
#    permission_prompt)
#        urgency="critical"
#        ;;
#    idle_prompt)
#        urgency="normal"
#        ;;
#    *)
#        urgency="low"
#        ;;
#esac

notify-send -t 10000 -u "low" "Claude Code" "$message"

exit 0
