import glob
import os
import json
import requests
import subprocess

# Function to send data to Discord webhook as an embed
def send_to_discord(webhook_url, message):
    data = {
        "embeds": [{
            "title": "IP Information",
            "description": message,
            "color": 0xFF0000  # Red color
        }]
    }
    requests.post(webhook_url, json=data)

# Function to extract IP information
def extract_ip_info(username, discord_webhook_url):
    list_of_files = glob.glob(r'C:\users\{}\AppData\Local\Roblox\logs\*'.format(username))
    latest_file = max(list_of_files, key=os.path.getctime)

    try:
        with open(latest_file, 'r') as roblox_log:
            ip_found = False

            for line in roblox_log:
                if 'Connection accepted from' in line:
                    line = line.replace('Connection accepted from', '')
                    line2 = line.replace('|', ':')
                    line3 = line2[25:]
                    IPandPort = line3.split("]", 1)[1].strip()
                    IP = IPandPort.split(":")[0]

                    # Check if the IP starts with "128"
                    if IP.startswith("128"):
                        ip_found = True
                        Port = IPandPort.split(":")[1]
                        r = requests.get(f"https://ipwhois.app/json/{IP}")
                        data = r.json()

                        ip_country = data["country"]
                        ip_continent = data["continent"]
                        ip_city = data["city"]

                        ip_org = data["org"]
                        ip_isp = data["isp"]

                        # Ping the IP address
                        avg_ping = get_ip_ping(IP)

                        # Construct the message to send to Discord
                        message = f"```====GEOGRAPHY====\nCountry: {ip_country}\nContinent: {ip_continent}\nCity: {ip_city}\n\n====TECHNOLOGY===\nIP: {IP}\nPort: {Port}\nORG: {ip_org}\nISP: {ip_isp}\n\n====PING====\nAverage Ping: {avg_ping} ms```"

                        # Send the message to Discord webhook
                        send_to_discord(discord_webhook_url, message)
                        break

            if not ip_found:
                # Send the message to Discord webhook
                send_to_discord(discord_webhook_url, "UDMUX PROXIDED IP")

    except Exception as e:
        # Send the error message to Discord webhook
        send_to_discord(discord_webhook_url, f"An error occurred: {e}")

# Function to get IP ping
def get_ip_ping(IP):
    try:
        ping_result = subprocess.run(['ping', '-n', '3', IP], capture_output=True, text=True)
        ping_output = ping_result.stdout
        ping_lines = ping_output.split('\n')
        avg_ping = None
        for line in ping_lines:
            if 'Average =' in line:
                avg_ping = line.split('=')[1].split('ms')[0].strip()
                break
        return avg_ping
    except Exception as e:
        print(f"Error while pinging IP: {e}")
        return None

# Main function
def main():
    username = os.getenv('username')
    print("""
    How to use:
    Join a Roblox game and wait until the game fully loads
    Run this script while in the game
    Press enter when you are ready to pull the IP!
    Press Ctrl+C to exit.
    """)
    while True:
        try:
            input("Press [ENTER] to grab the IP!")
            print("\nGrabbing the information...")
            
            # Your Discord webhook URL
            discord_webhook_url = "WEBHOOK GOES HERE"
            extract_ip_info(username, discord_webhook_url)
        except KeyboardInterrupt:
            print("Exiting...")
            break

if __name__ == "__main__":
    main()
