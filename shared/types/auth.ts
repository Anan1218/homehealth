export interface User {
  id: string;
  email: string;
  full_name?: string;
  created_at: string;
}

export interface UserCreate {
  email: string;
  password: string;
  full_name?: string;
}

export interface UserLogin {
  email: string;
  password: string;
}

export interface AuthToken {
  access_token: string;
  token_type: string;
  expires_at: number;
  user: User;
} 