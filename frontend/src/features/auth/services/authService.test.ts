import { describe, it, expect, vi, beforeEach } from 'vitest'
import { AuthService } from './authService'
import type { UserCreate, UserLogin } from '../../../shared/types/auth'

// Mock the supabase client
vi.mock('../../../shared/services/supabase', () => ({
  supabase: {
    auth: {
      signUp: vi.fn(),
      signInWithPassword: vi.fn(),
      signOut: vi.fn(),
      getUser: vi.fn(),
    },
  },
}))

// Import after mocking
const { supabase } = await import('../../../shared/services/supabase')

describe('AuthService', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  describe('register', () => {
    it('should register a new user successfully', async () => {
      // Arrange
      const userData: UserCreate = {
        email: 'test@example.com',
        password: 'password123',
        full_name: 'Test User',
      }

      const mockSupabaseResponse = {
        data: {
          user: {
            id: '123',
            email: 'test@example.com',
            created_at: '2024-01-01T00:00:00Z',
            user_metadata: { full_name: 'Test User' },
          },
          session: {
            access_token: 'token123',
            expires_at: 1234567890,
          },
        },
        error: null,
      }

      vi.mocked(supabase.auth.signUp).mockResolvedValue(mockSupabaseResponse as any)

      // Act
      const result = await AuthService.register(userData)

      // Assert
      expect(supabase.auth.signUp).toHaveBeenCalledWith({
        email: userData.email,
        password: userData.password,
        options: {
          data: {
            full_name: userData.full_name,
          },
        },
      })

      expect(result).toEqual({
        access_token: 'token123',
        token_type: 'bearer',
        expires_at: 1234567890,
        user: {
          id: '123',
          email: 'test@example.com',
          full_name: 'Test User',
          created_at: '2024-01-01T00:00:00Z',
        },
      })
    })

    it('should throw error when registration fails', async () => {
      // Arrange
      const userData: UserCreate = {
        email: 'test@example.com',
        password: 'password123',
        full_name: 'Test User',
      }

      const mockSupabaseResponse = {
        data: { user: null, session: null },
        error: new Error('Email already exists'),
      }

      vi.mocked(supabase.auth.signUp).mockResolvedValue(mockSupabaseResponse as any)

      // Act & Assert
      await expect(AuthService.register(userData)).rejects.toThrow('Email already exists')
    })

    it('should throw error when user or session is null', async () => {
      // Arrange
      const userData: UserCreate = {
        email: 'test@example.com',
        password: 'password123',
        full_name: 'Test User',
      }

      const mockSupabaseResponse = {
        data: { user: null, session: null },
        error: null,
      }

      vi.mocked(supabase.auth.signUp).mockResolvedValue(mockSupabaseResponse as any)

      // Act & Assert
      await expect(AuthService.register(userData)).rejects.toThrow('Registration failed')
    })
  })

  describe('login', () => {
    it('should login user successfully', async () => {
      // Arrange
      const credentials: UserLogin = {
        email: 'test@example.com',
        password: 'password123',
      }

      const mockSupabaseResponse = {
        data: {
          user: {
            id: '123',
            email: 'test@example.com',
            created_at: '2024-01-01T00:00:00Z',
            user_metadata: { full_name: 'Test User' },
          },
          session: {
            access_token: 'token123',
            expires_at: 1234567890,
          },
        },
        error: null,
      }

      vi.mocked(supabase.auth.signInWithPassword).mockResolvedValue(mockSupabaseResponse as any)

      // Act
      const result = await AuthService.login(credentials)

      // Assert
      expect(supabase.auth.signInWithPassword).toHaveBeenCalledWith({
        email: credentials.email,
        password: credentials.password,
      })

      expect(result).toEqual({
        access_token: 'token123',
        token_type: 'bearer',
        expires_at: 1234567890,
        user: {
          id: '123',
          email: 'test@example.com',
          full_name: 'Test User',
          created_at: '2024-01-01T00:00:00Z',
        },
      })
    })

    it('should throw error when login fails', async () => {
      // Arrange
      const credentials: UserLogin = {
        email: 'test@example.com',
        password: 'wrongpassword',
      }

      const mockSupabaseResponse = {
        data: { user: null, session: null },
        error: new Error('Invalid credentials'),
      }

      vi.mocked(supabase.auth.signInWithPassword).mockResolvedValue(mockSupabaseResponse as any)

      // Act & Assert
      await expect(AuthService.login(credentials)).rejects.toThrow('Invalid credentials')
    })
  })

  describe('logout', () => {
    it('should logout user successfully', async () => {
      // Arrange
      const mockSupabaseResponse = { error: null }
      vi.mocked(supabase.auth.signOut).mockResolvedValue(mockSupabaseResponse as any)

      // Act
      await AuthService.logout()

      // Assert
      expect(supabase.auth.signOut).toHaveBeenCalled()
    })

    it('should throw error when logout fails', async () => {
      // Arrange
      const mockSupabaseResponse = { error: new Error('Logout failed') }
      vi.mocked(supabase.auth.signOut).mockResolvedValue(mockSupabaseResponse as any)

      // Act & Assert
      await expect(AuthService.logout()).rejects.toThrow('Logout failed')
    })
  })

  describe('getCurrentUser', () => {
    it('should return current user when authenticated', async () => {
      // Arrange
      const mockSupabaseResponse = {
        data: {
          user: {
            id: '123',
            email: 'test@example.com',
            created_at: '2024-01-01T00:00:00Z',
            user_metadata: { full_name: 'Test User' },
          },
        },
      }

      vi.mocked(supabase.auth.getUser).mockResolvedValue(mockSupabaseResponse as any)

      // Act
      const result = await AuthService.getCurrentUser()

      // Assert
      expect(supabase.auth.getUser).toHaveBeenCalled()
      expect(result).toEqual({
        id: '123',
        email: 'test@example.com',
        full_name: 'Test User',
        created_at: '2024-01-01T00:00:00Z',
      })
    })

    it('should return null when user is not authenticated', async () => {
      // Arrange
      const mockSupabaseResponse = {
        data: { user: null },
      }

      vi.mocked(supabase.auth.getUser).mockResolvedValue(mockSupabaseResponse as any)

      // Act
      const result = await AuthService.getCurrentUser()

      // Assert
      expect(result).toBeNull()
    })
  })
}) 