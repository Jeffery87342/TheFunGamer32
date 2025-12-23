#!/usr/bin/env python3
"""
Console version of Roblox Auto-Group Joiner
Use this if tkinter is not available on your system
"""

import sys
from threading import Thread, Event
from time import gmtime, strftime, sleep
from counter import counter
from group_joiner import GroupJoiner
from output import Output
from util import Util
import os

def print_banner():
    banner = """
    ╔══════════════════════════════════════════════════════════╗
    ║       🚀 Roblox Auto-Group Joiner (Console Mode)         ║
    ║                  Powered by FunBypass.com                 ║
    ╚══════════════════════════════════════════════════════════╝
    """
    print(banner)

def get_input(prompt, required=True):
    while True:
        value = input(prompt).strip()
        if value or not required:
            return value
        print("This field is required. Please try again.")

def stats_updater(stop_event):
    """Updates and displays statistics"""
    elapsed = 0
    
    while not stop_event.is_set():
        joined = counter.get_value()
        runtime = strftime('%H:%M:%S', gmtime(elapsed))
        
        # Clear line and print stats
        sys.stdout.write(f"\r[STATS] Runtime: {runtime} | Groups Joined: {joined}    ")
        sys.stdout.flush()
        
        elapsed += 1
        sleep(1)

def main():
    print_banner()
    
    # Get configuration
    print("\n[1/4] Loading configuration...")
    config = Util.get_config()
    
    if not config.get("solverKey"):
        print("\n⚠️  WARNING: No FunBypass API key found in input/config.json")
        print("Please add your API key before running the script.")
        api_key = get_input("Enter your FunBypass API key (or press Enter to continue without): ", required=False)
        if api_key:
            config["solverKey"] = api_key
    else:
        print(f"✓ FunBypass API key loaded")
    
    # Get Group ID
    print("\n[2/4] Group Information")
    group_id = get_input("Enter Roblox Group ID: ")
    
    # Get Cookies
    print("\n[3/4] Roblox Cookies")
    print("Enter cookies (.ROBLOSECURITY values), one per line.")
    print("Press Enter twice when done:")
    
    cookies = []
    while True:
        cookie = input(f"Cookie #{len(cookies)+1}: ").strip()
        if not cookie:
            if len(cookies) > 0:
                break
            print("You must enter at least one cookie.")
            continue
        cookies.append(cookie)
    
    print(f"✓ {len(cookies)} cookie(s) loaded")
    
    # Check proxies
    print("\n[4/4] Proxy Configuration")
    proxies = Util.get_random_proxy()
    if proxies:
        print(f"✓ Proxies loaded from file")
    else:
        print("⚠️  No proxies found. The script will run without proxies.")
        print("   Add proxies to 'proxies.txt' for better performance.")
    
    # Confirm and start
    print("\n" + "="*60)
    print(f"Configuration Summary:")
    print(f"  Group ID: {group_id}")
    print(f"  Cookies: {len(cookies)}")
    print(f"  Proxies: {'Enabled' if proxies else 'Disabled'}")
    print("="*60)
    
    confirm = get_input("\nStart joining groups? (yes/no): ")
    if confirm.lower() not in ['yes', 'y']:
        print("Cancelled.")
        return
    
    # Start joining
    print(f"\n🚀 Starting group joiner with {len(cookies)} account(s)...\n")
    
    stop_event = Event()
    threads = []
    
    # Start stats updater
    stats_thread = Thread(target=stats_updater, args=(stop_event,), daemon=True)
    stats_thread.start()
    
    # Start joining threads
    for cookie in cookies:
        t = Thread(target=GroupJoiner.join_group, args=(group_id, cookie, stop_event))
        threads.append(t)
        t.start()
    
    try:
        # Wait for all threads to complete
        for t in threads:
            t.join()
        
        stop_event.set()
        print(f"\n\n✅ Finished! Total groups joined: {counter.get_value()}")
        
    except KeyboardInterrupt:
        print(f"\n\n⚠️  Interrupted by user. Stopping...")
        stop_event.set()
        for t in threads:
            t.join(timeout=2)
        print(f"✅ Stopped. Total groups joined: {counter.get_value()}")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        sys.exit(1)
