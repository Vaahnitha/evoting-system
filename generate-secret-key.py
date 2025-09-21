#!/usr/bin/env python3
"""
Generate a secure Django secret key for production use.
This script creates a cryptographically secure secret key that should be used
in production environments.
"""

import secrets
import string


def generate_secret_key():
    """Generate a secure Django secret key."""
    # Django secret key characters
    chars = string.ascii_letters + string.digits + "!@#$%^&*(-_=+)"
    
    # Generate a 50-character secret key
    secret_key = ''.join(secrets.choice(chars) for _ in range(50))
    
    return secret_key


if __name__ == "__main__":
    print("Generated Django Secret Key:")
    print("=" * 50)
    print(generate_secret_key())
    print("=" * 50)
    print("\nIMPORTANT SECURITY NOTES:")
    print("1. Copy this key to your .env file as DJANGO_SECRET_KEY")
    print("2. Never commit this key to version control")
    print("3. Use different keys for different environments")
    print("4. Keep this key secure and private")
    print("\nExample .env entry:")
    print(f"DJANGO_SECRET_KEY={generate_secret_key()}")
