# NextDNS Tools

A comprehensive collection of tools for downloading and analyzing NextDNS logs.

## Features

- 🚀 **Automatic Pagination**: Handles large log files by automatically paginating through the NextDNS API
- ♾️ **Unlimited Downloads**: Downloads your ENTIRE log history by default with no limits
- 📊 **Multiple Export Formats**: Export logs to both JSON and CSV formats
- 🌐 **Interactive HTML Viewer**: Beautiful, responsive web interface to view and analyze logs
- 📱 **Device Analysis**: Group and filter logs by device
- 🎨 **Favicon Integration**: Uses NextDNS favicon service to display domain icons
- 📈 **Statistics Dashboard**: View total queries, blocked queries, unique domains, and device counts

## Installation

1. Clone the repository:
```bash
git clone https://github.com/MrTakedi/nextdns-tools.git
cd nextdns-tools
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Quick Start

For a quick start, you can use the provided example script:

```bash
# Edit example.sh and set your API credentials
nano example.sh  # or use your preferred editor

# Run the script to download ALL logs
./example.sh
```

This will download your **entire log history** (no limits) and automatically open the viewer in your browser.

### Downloading Logs

The `nextdns_logs.py` script downloads logs from the NextDNS API with automatic pagination support.

#### Basic Usage

Download **ALL** your NextDNS logs (entire history):

```bash
python nextdns_logs.py --api-key YOUR_API_KEY --profile YOUR_PROFILE_ID
```

This will download your **complete log history** and save it to `nextdns_logs.json` and `nextdns_logs.csv`. The tool uses automatic pagination to prevent timeouts, so even very large log histories will download successfully.

#### Using Environment Variables

You can set environment variables to avoid passing credentials on the command line:

```bash
export NEXTDNS_API_KEY="your_api_key"
export NEXTDNS_PROFILE_ID="your_profile_id"
python nextdns_logs.py
```

#### Advanced Options

```bash
# Optionally limit the number of logs (only if you don't want the full history)
python nextdns_logs.py --api-key YOUR_API_KEY --profile YOUR_PROFILE_ID --max-logs 1000

# Specify custom output filename
python nextdns_logs.py --api-key YOUR_API_KEY --profile YOUR_PROFILE_ID --output my_logs

# Download JSON only (skip CSV)
python nextdns_logs.py --api-key YOUR_API_KEY --profile YOUR_PROFILE_ID --json-only

# Download CSV only (skip JSON)
python nextdns_logs.py --api-key YOUR_API_KEY --profile YOUR_PROFILE_ID --csv-only
```

**Note:** The `--max-logs` option is optional. By default, the tool downloads your **entire log history** without any limits.

#### Command-Line Options

- `--api-key`: Your NextDNS API key (or set `NEXTDNS_API_KEY` environment variable)
- `--profile`: Your NextDNS profile/configuration ID (or set `NEXTDNS_PROFILE_ID` environment variable)
- `--output`: Output filename prefix (default: `nextdns_logs`)
- `--max-logs`: **Optional** - Maximum number of logs to download. **Default: ALL logs (no limit)**
- `--json-only`: Only save JSON output (skip CSV)
- `--csv-only`: Only save CSV output (skip JSON)

### Viewing Logs

After downloading logs, you can view them using the `viewer.html` file:

1. Open `viewer.html` in a web browser
2. Click "Choose File" and select your downloaded JSON or CSV file
3. Explore your logs with the interactive interface

#### Viewer Features

- **Statistics Dashboard**: See total queries, blocked queries, unique domains, and device counts
- **Device View**: See all devices and their query counts, click on a device to see its logs
- **All Logs View**: Browse all logs in a paginated table
- **Search**: Filter logs by domain name
- **Responsive Design**: Built with Bootstrap 5, works on all screen sizes
- **Favicon Support**: Domain favicons from NextDNS favicon service

## Getting Your NextDNS API Key

1. Log in to your NextDNS account at https://my.nextdns.io
2. Go to Settings → API
3. Generate an API key
4. Note your profile/configuration ID (shown in the URL or in the profile list)

## Requirements

- Python 3.6+
- requests
- python-dateutil

## License

MIT

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
