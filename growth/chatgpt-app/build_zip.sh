#!/bin/bash
# Package the ChatGPT plugin for upload in OpenAI's plugin dashboard (DLC-184): plugin.json and mcp.json at the ZIP's
# root, icons under assets/. Fails while demo_recording_url is still the placeholder unless --draft is given.
#   bash growth/chatgpt-app/build_zip.sh [--draft]   ->  growth/chatgpt-app/dealectric-plugin.zip
set -euo pipefail
cd "$(dirname "$0")/plugin"
if grep -q REPLACE_WITH_VIDEO_URL plugin.json && [ "${1:-}" != "--draft" ]; then
  echo "plugin.json still has REPLACE_WITH_VIDEO_URL: set review.demo_recording_url first (or pass --draft)" >&2; exit 2
fi
python3 -c 'import json; json.load(open("plugin.json")); json.load(open("mcp.json"))'
rm -f ../dealectric-plugin.zip
zip -q -X -r ../dealectric-plugin.zip plugin.json mcp.json assets -x '.*'
unzip -l ../dealectric-plugin.zip
