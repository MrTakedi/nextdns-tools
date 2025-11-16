#!/bin/bash
# Example script to download NextDNS logs and open the viewer
# This script demonstrates how to use the NextDNS log downloader

# Configuration
# Replace these with your actual NextDNS credentials
export NEXTDNS_API_KEY="your_api_key_here"
export NEXTDNS_PROFILE_ID="your_profile_id_here"

# Download ALL logs from the past 2 years (NextDNS maximum retention period)
# The tool automatically handles pagination to prevent timeouts
echo "Downloading ALL NextDNS logs from the past 2 years (max retention)..."
echo "This may take some time depending on your log size..."
python3 nextdns_logs.py

# Check if download was successful
if [ $? -eq 0 ]; then
    echo "✅ All logs downloaded successfully!"
    echo "📁 Files created:"
    echo "   - nextdns_logs.json"
    echo "   - nextdns_logs.csv"
    echo ""
    echo "🌐 To view the logs:"
    echo "   1. Open viewer.html in your web browser"
    echo "   2. Click 'Choose File' and select nextdns_logs.json or nextdns_logs.csv"
    echo ""
    
    # Optional: Open viewer in default browser (works on most systems)
    if command -v xdg-open > /dev/null; then
        xdg-open viewer.html
    elif command -v open > /dev/null; then
        open viewer.html
    elif command -v start > /dev/null; then
        start viewer.html
    else
        echo "ℹ️  Please open viewer.html manually in your browser"
    fi
else
    echo "❌ Error downloading logs"
    exit 1
fi
