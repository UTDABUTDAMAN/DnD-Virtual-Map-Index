#!/usr/bin/env python3
"""
Secret Key Generator for DnD Virtual Map Index
Generates a cryptographically secure SECRET_KEY for Flask session signing.
"""
import secrets


def main():
    print("=" * 60)
    print("DnD Virtual Map Index - Secret Key Generator")
    print("=" * 60)

    # Generate 32 bytes (256 bits) of cryptographic randomness as a 64-char hex string
    secret_key = secrets.token_hex(32)

    print("\nGenerated Cryptographic SECRET_KEY:")
    print("-" * 60)
    print(f"SECRET_KEY={secret_key}")
    print("-" * 60)
    print("Copy and paste this line into your .env file.\n")


if __name__ == "__main__":
    main()
