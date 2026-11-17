#!/usr/bin/env python3
"""
Password Hash Generator for DnD Virtual Map Index
Generates secure password hashes using Werkzeug for storage in .env.
"""
import sys
import getpass
from werkzeug.security import generate_password_hash


def main():
    print("=" * 60)
    print("DnD Virtual Map Index - Password Hash Generator")
    print("=" * 60)

    if len(sys.argv) == 3:
        role = sys.argv[1].strip().lower()
        password = sys.argv[2]
    else:
        print("\nSelect role to generate hash for:")
        print("  1) Gamemaster (GM_PASSWORD_HASH)")
        print("  2) Player     (PLAYER_PASSWORD_HASH)")
        choice = input("\nEnter choice (1 or 2, default: 1): ").strip()
        role = "player" if choice == "2" else "gamemaster"

        password = getpass.getpass(f"Enter password for {role}: ")
        confirm = getpass.getpass("Confirm password: ")
        if password != confirm:
            print("Error: Passwords do not match.")
            sys.exit(1)

    if not password:
        print("Error: Password cannot be empty.")
        sys.exit(1)

    pw_hash = generate_password_hash(password)
    env_var_name = "GM_PASSWORD_HASH" if role == "gamemaster" else "PLAYER_PASSWORD_HASH"

    print("\nGenerated Werkzeug Password Hash:")
    print("-" * 60)
    print(f"{env_var_name}={pw_hash}")
    print("-" * 60)
    print("Copy and paste this line into your .env file.")


if __name__ == "__main__":
    main()
