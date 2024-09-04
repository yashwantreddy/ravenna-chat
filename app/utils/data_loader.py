from typing import List, Dict
from dotenv import load_dotenv
import os
from supabase import create_client, Client

load_dotenv()

url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_KEY")
supabase_client: Client = create_client(url, key)


def load_zendesk_tickets() -> List[Dict]:
    try:
        return supabase_client.table("zendesk").select("*").execute().data
    except Exception as e:
        print(f"Error loading Zendesk tickets through Supabase: {e}")
        return []