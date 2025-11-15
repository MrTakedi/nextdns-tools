#!/usr/bin/env python3
"""
NextDNS Log Downloader
A CLI tool to download logs from NextDNS API with pagination support and export to JSON/CSV.
"""

import argparse
import csv
import json
import os
import sys
import time
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional

try:
    import requests
    from dateutil import parser as date_parser
except ImportError:
    print("Error: Required dependencies not installed.")
    print("Please run: pip install -r requirements.txt")
    sys.exit(1)


class NextDNSLogDownloader:
    """Handle downloading logs from NextDNS API with pagination."""
    
    BASE_URL = "https://api.nextdns.io"
    
    def __init__(self, api_key: str, profile_id: str):
        """
        Initialize the NextDNS log downloader.
        
        Args:
            api_key: NextDNS API key
            profile_id: NextDNS profile/configuration ID
        """
        self.api_key = api_key
        self.profile_id = profile_id
        self.session = requests.Session()
        self.session.headers.update({
            'X-Api-Key': api_key
        })
    
    def get_logs(self, limit: int = 100, cursor: Optional[str] = None) -> Dict[str, Any]:
        """
        Fetch logs from NextDNS API.
        
        Args:
            limit: Number of logs per request (max 100)
            cursor: Pagination cursor for next page
            
        Returns:
            Dictionary containing logs data and pagination info
        """
        url = f"{self.BASE_URL}/profiles/{self.profile_id}/logs"
        params = {'limit': min(limit, 100)}
        
        if cursor:
            params['cursor'] = cursor
        
        try:
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching logs: {e}")
            return {'data': [], 'meta': {}}
    
    def download_all_logs(self, max_logs: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Download all logs with automatic pagination.
        
        Args:
            max_logs: Maximum number of logs to download (None for all)
            
        Returns:
            List of all log entries
        """
        all_logs = []
        cursor = None
        page = 1
        
        print("Starting log download...")
        
        while True:
            print(f"Fetching page {page}...", end=' ')
            
            response = self.get_logs(cursor=cursor)
            logs = response.get('data', [])
            meta = response.get('meta', {})
            
            if not logs:
                print("No more logs.")
                break
            
            all_logs.extend(logs)
            print(f"Retrieved {len(logs)} logs (Total: {len(all_logs)})")
            
            # Check if we've reached the max limit
            if max_logs and len(all_logs) >= max_logs:
                all_logs = all_logs[:max_logs]
                print(f"Reached maximum log limit of {max_logs}")
                break
            
            # Check for next page cursor
            cursor = meta.get('cursor')
            if not cursor:
                print("All logs downloaded.")
                break
            
            page += 1
            # Small delay to avoid rate limiting
            time.sleep(0.5)
        
        return all_logs
    
    def save_to_json(self, logs: List[Dict[str, Any]], filename: str):
        """
        Save logs to JSON file.
        
        Args:
            logs: List of log entries
            filename: Output filename
        """
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(logs, f, indent=2, ensure_ascii=False)
        print(f"Saved {len(logs)} logs to {filename}")
    
    def save_to_csv(self, logs: List[Dict[str, Any]], filename: str):
        """
        Save logs to CSV file.
        
        Args:
            logs: List of log entries
            filename: Output filename
        """
        if not logs:
            print("No logs to save to CSV")
            return
        
        # Extract all possible fields from logs
        fieldnames = set()
        for log in logs:
            fieldnames.update(self._flatten_dict(log).keys())
        
        fieldnames = sorted(list(fieldnames))
        
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            
            for log in logs:
                flattened = self._flatten_dict(log)
                writer.writerow(flattened)
        
        print(f"Saved {len(logs)} logs to {filename}")
    
    def _flatten_dict(self, d: Dict[str, Any], parent_key: str = '', sep: str = '_') -> Dict[str, Any]:
        """
        Flatten nested dictionary for CSV export.
        
        Args:
            d: Dictionary to flatten
            parent_key: Parent key for nested items
            sep: Separator for nested keys
            
        Returns:
            Flattened dictionary
        """
        items = []
        for k, v in d.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            
            if isinstance(v, dict):
                items.extend(self._flatten_dict(v, new_key, sep=sep).items())
            elif isinstance(v, list):
                # Convert lists to comma-separated strings
                items.append((new_key, ', '.join(map(str, v)) if v else ''))
            else:
                items.append((new_key, v))
        
        return dict(items)


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description='Download ALL logs from NextDNS API with automatic pagination support. '
                    'By default, this tool downloads your entire log history without any limits.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Download ALL logs (entire history) and save to JSON and CSV
  python nextdns_logs.py --api-key YOUR_API_KEY --profile YOUR_PROFILE_ID
  
  # Optionally limit the number of logs (use only if needed)
  python nextdns_logs.py --api-key YOUR_API_KEY --profile YOUR_PROFILE_ID --max-logs 1000
  
  # Specify custom output filenames
  python nextdns_logs.py --api-key YOUR_API_KEY --profile YOUR_PROFILE_ID --output my_logs

Environment Variables:
  NEXTDNS_API_KEY      - Your NextDNS API key
  NEXTDNS_PROFILE_ID   - Your NextDNS profile/configuration ID

Note: By default, this tool downloads your ENTIRE log history from NextDNS.
      Large log histories may take some time to download but pagination prevents timeouts.
        """
    )
    
    parser.add_argument(
        '--api-key',
        type=str,
        default=os.environ.get('NEXTDNS_API_KEY'),
        help='NextDNS API key (or set NEXTDNS_API_KEY env var)'
    )
    
    parser.add_argument(
        '--profile',
        type=str,
        default=os.environ.get('NEXTDNS_PROFILE_ID'),
        help='NextDNS profile/configuration ID (or set NEXTDNS_PROFILE_ID env var)'
    )
    
    parser.add_argument(
        '--output',
        type=str,
        default='nextdns_logs',
        help='Output filename prefix (default: nextdns_logs)'
    )
    
    parser.add_argument(
        '--max-logs',
        type=int,
        default=None,
        help='Optional: Maximum number of logs to download. By default, ALL logs are downloaded (no limit).'
    )
    
    parser.add_argument(
        '--json-only',
        action='store_true',
        help='Only save JSON output (skip CSV)'
    )
    
    parser.add_argument(
        '--csv-only',
        action='store_true',
        help='Only save CSV output (skip JSON)'
    )
    
    args = parser.parse_args()
    
    # Validate required arguments
    if not args.api_key:
        parser.error("--api-key is required (or set NEXTDNS_API_KEY environment variable)")
    
    if not args.profile:
        parser.error("--profile is required (or set NEXTDNS_PROFILE_ID environment variable)")
    
    # Initialize downloader
    downloader = NextDNSLogDownloader(args.api_key, args.profile)
    
    # Download logs
    try:
        logs = downloader.download_all_logs(max_logs=args.max_logs)
        
        if not logs:
            print("No logs downloaded.")
            return
        
        # Save to files
        if not args.csv_only:
            json_filename = f"{args.output}.json"
            downloader.save_to_json(logs, json_filename)
        
        if not args.json_only:
            csv_filename = f"{args.output}.csv"
            downloader.save_to_csv(logs, csv_filename)
        
        print(f"\nDownload complete! Total logs: {len(logs)}")
        
    except KeyboardInterrupt:
        print("\n\nDownload interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\nError: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
