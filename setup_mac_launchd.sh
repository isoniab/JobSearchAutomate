#!/bin/bash
# Setup script for automatic daily background job search execution on macOS via launchd

PLIST_PATH="$HOME/Library/LaunchAgents/com.jobsearch.automate.plist"
PROJECT_DIR="/Users/tarun/Desktop/JobSearchAutomate"

mkdir -p "$HOME/Library/LaunchAgents"

cat <<EOF > "$PLIST_PATH"
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.jobsearch.automate</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>${PROJECT_DIR}/main.py</string>
    </array>
    <key>WorkingDirectory</key>
    <string>${PROJECT_DIR}</string>
    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key>
        <integer>8</integer>
        <key>Minute</key>
        <integer>0</integer>
    </dict>
    <key>RunAtLoad</key>
    <true/>
    <key>StandardOutPath</key>
    <string>${PROJECT_DIR}/reports/scheduler_stdout.log</string>
    <key>StandardErrorPath</key>
    <string>${PROJECT_DIR}/reports/scheduler_stderr.log</string>
</dict>
</plist>
EOF

# Unload previous plist if exists and load new plist
launchctl unload "$PLIST_PATH" 2>/dev/null
launchctl load "$PLIST_PATH"

echo "✅ Successfully installed macOS launchd daily scheduler service!"
echo "📅 JobSearchAutomate will now run automatically every day at 8:00 AM."
