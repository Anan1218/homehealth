import { supabase } from '../../../shared/services/supabase';
import type { User, UserCreate, UserLogin, AuthToken } from '../../../shared/types/auth';

export class AuthService {
  /**
   * Register a new user
   */
  static async register(userData: UserCreate): Promise<AuthToken> {
    const { data, error } = await supabase.auth.signUp({
      email: userData.email,
      password: userData.password,
      options: {
        data: {
          full_name: userData.full_name,
        },
      },
    });

    if (error) throw error;
    if (!data.user || !data.session) throw new Error('Registration failed');

    return {
      access_token: data.session.access_token,
      token_type: 'bearer',
      expires_at: data.session.expires_at || 0,
      user: {
        id: data.user.id,
        email: data.user.email || '',
        full_name: data.user.user_metadata?.full_name,
        created_at: data.user.created_at,
      },
    };
  }

  /**
   * Login user
   */
  static async login(credentials: UserLogin): Promise<AuthToken> {
    const { data, error } = await supabase.auth.signInWithPassword({
      email: credentials.email,
      password: credentials.password,
    });

    if (error) throw error;
    if (!data.user || !data.session) throw new Error('Login failed');

    return {
      access_token: data.session.access_token,
      token_type: 'bearer',
      expires_at: data.session.expires_at || 0,
      user: {
        id: data.user.id,
        email: data.user.email || '',
        full_name: data.user.user_metadata?.full_name,
        created_at: data.user.created_at,
      },
    };
  }

  /**
   * Logout user
   */
  static async logout(): Promise<void> {
    const { error } = await supabase.auth.signOut();
    if (error) throw error;
  }

  /**
   * Get current user
   */
  static async getCurrentUser(): Promise<User | null> {
    const { data: { user } } = await supabase.auth.getUser();
    
    if (!user) return null;

    return {
      id: user.id,
      email: user.email || '',
      full_name: user.user_metadata?.full_name,
      created_at: user.created_at,
    };
  }
} 