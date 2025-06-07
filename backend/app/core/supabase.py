from supabase import create_client, Client
from app.core.config import settings


class SupabaseClient:
    """Singleton Supabase client following Single Responsibility Principle"""
    
    _instance: Client = None
    
    @classmethod
    def get_client(cls) -> Client:
        if cls._instance is None:
            cls._instance = create_client(
                settings.SUPABASE_URL,
                settings.SUPABASE_ANON_KEY
            )
        return cls._instance
    
    @classmethod
    def get_admin_client(cls) -> Client:
        """Admin client with service role key for server-side operations"""
        return create_client(
            settings.SUPABASE_URL,
            settings.SUPABASE_SERVICE_ROLE_KEY
        )


# Convenience functions
def get_supabase() -> Client:
    return SupabaseClient.get_client()

def get_supabase_admin() -> Client:
    return SupabaseClient.get_admin_client() 