import hashlib
import json
import logging
from datetime import datetime

import requests
from django.core.management.base import BaseCommand
from django.db import transaction
from products.models import Produk, Kategori, Status

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Fetches products from the API and syncs them to the database'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='API Username')

    def handle(self, *args, **options):
        username = options['username']
        self.stdout.write(f"Starting sync for user: {username}")

        # Calculate password hash
        today = datetime.now()
        # Format: bisacoding-DD-MM-YY
        # Note: The requirement says "bisacoding-DD-MM-YY". 
        # Usually it is 'bisacoding-dd-mm-yy' (lowercase) or strictly formatted.
        # Assuming the standard date format day-month-2digitYear.
        password_raw = f"bisacoding-{today.strftime('%d-%m-%y')}"
        password_hash = hashlib.md5(password_raw.encode()).hexdigest()
        
        self.stdout.write(f"Generated password hash for {password_raw}: {password_hash}")

        url = "https://recruitment.fastprint.co.id/tes/api_tes_programmer"
        
        session = requests.Session()
        
        # Standard browser headers
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-Requested-With': 'XMLHttpRequest'
        }

        # Password is always bisacoding-DD-MM-YY
        password_raw = f"bisacoding-{today.strftime('%d-%m-%y')}"
        password_hash = hashlib.md5(password_raw.encode()).hexdigest()

        # Determine usernames to try
        usernames_to_try = [username] if username != 'auto' else []
        
        if username == 'auto' or 'tesprogrammer' in username:
             # Generate dynamic username: tesprogrammerDDMMYYCHH
             # Try current hour and previous hour to handle server time mismatch
             base_name = "tesprogrammer"
             date_part = today.strftime('%d%m%y')
             current_hour = int(today.strftime('%H'))
             
             # Hours to try: current, previous (handle 00 case), and next (just in case)
             hours = [current_hour, current_hour - 1, current_hour + 1]
             
             for h in hours:
                 if 0 <= h <= 23:
                     # Pads hour with 0 if needed e.g. 09
                     h_str = f"{h:02d}" 
                     usernames_to_try.append(f"{base_name}{date_part}C{h_str}")
        
        # Deduplicate preserving order
        usernames_to_try = list(dict.fromkeys(usernames_to_try))

        self.stdout.write(f"Password Hash: {password_hash} (Raw: {password_raw})")

        success = False
        for user_candidate in usernames_to_try:
            self.stdout.write(f"Attempting with username: {user_candidate} ...")
            
            payload = {
                'username': user_candidate,
                'password': password_hash
            }

            try:
                response = session.post(url, data=payload, headers=headers)
                
                if response.status_code == 200:
                    try:
                        data = response.json()
                        if isinstance(data, dict) and data.get('error') == 0:
                            self.stdout.write(self.style.SUCCESS(f"Login successful with {user_candidate}!"))
                            
                            # Proceed with processing
                            if 'data' in data:
                                products_list = data['data']
                                self.process_data(products_list) # Refactoring process logic out might be cleaner, but for now inline below
                                success = True
                                break
                            else:
                                self.stdout.write(self.style.WARNING("No 'data' field in response."))
                        else:
                             err_msg = data.get('ket', 'Unknown error') if isinstance(data, dict) else str(data)
                             self.stdout.write(self.style.WARNING(f"Failed with {user_candidate}: {err_msg}"))
                    except json.JSONDecodeError:
                        self.stdout.write(self.style.ERROR("Invalid JSON response"))
                else:
                    self.stdout.write(self.style.WARNING(f"HTTP {response.status_code} with {user_candidate}"))

            except requests.RequestException as e:
                self.stdout.write(self.style.ERROR(f"Connection error: {e}"))
                break # Network error is likely fatal for all attempts
        
        if not success:
            self.stdout.write(self.style.ERROR("All attempts failed."))
            return


    def process_data(self, products_list):
        self.stdout.write(f"Received {len(products_list)} items. Syncing database...")
        with transaction.atomic():
            count_created = 0
            count_updated = 0
            
            for item in products_list:
                # Map fields
                # item keys might be 'id_produk', 'nama_produk', 'harga', 'kategori', 'status'
                
                # Skip if critical fields are missing
                if 'nama_produk' not in item:
                    continue
                    
                nama_produk = item['nama_produk']
                harga = item.get('harga', 0)
                if not str(harga).isdigit():
                    harga = 0
                
                opt1 = item.get('kategori', 'Uncategorized')
                opt2 = item.get('status', 'Unknown')

                # Get or Create Category
                kategori_obj, _ = Kategori.objects.get_or_create(nama_kategori=opt1)
                
                # Get or Create Status
                status_obj, _ = Status.objects.get_or_create(nama_status=opt2)

                # Update or Create Product
                obj, created = Produk.objects.update_or_create(
                    nama_produk=nama_produk,
                    defaults={
                        'harga': harga,
                        'kategori': kategori_obj,
                        'status': status_obj
                    }
                )
                
                if created:
                    count_created += 1
                else:
                    count_updated += 1
        
        self.stdout.write(self.style.SUCCESS(f"Sync complete! Created: {count_created}, Updated: {count_updated}"))



