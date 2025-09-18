#!/usr/bin/env python
"""
Script to import exported data to production PostgreSQL database
Usage: python import_to_production.py --database-url "postgresql://..."
"""
import os
import sys
import json
import argparse
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime

def connect_to_database(database_url):
    """Connect to PostgreSQL database"""
    try:
        conn = psycopg2.connect(database_url)
        return conn
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None

def import_candidates(conn, candidates_data):
    """Import candidates data"""
    cursor = conn.cursor()
    
    print("Importing candidates...")
    imported_count = 0
    
    for candidate in candidates_data:
        try:
            # Check if candidate already exists
            cursor.execute("SELECT id FROM voting_candidate WHERE id = %s", (candidate['id'],))
            if cursor.fetchone():
                print(f"Candidate {candidate['name']} already exists, skipping...")
                continue
            
            # Insert candidate
            cursor.execute("""
                INSERT INTO voting_candidate (id, name, department)
                VALUES (%s, %s, %s)
            """, (candidate['id'], candidate['name'], candidate['department']))
            
            imported_count += 1
            print(f"Imported candidate: {candidate['name']}")
            
        except Exception as e:
            print(f"Error importing candidate {candidate['name']}: {e}")
    
    conn.commit()
    print(f"Imported {imported_count} candidates")
    return imported_count

def import_users(conn, users_data):
    """Import users data"""
    cursor = conn.cursor()
    
    print("Importing users...")
    imported_count = 0
    
    for user in users_data:
        try:
            # Check if user already exists
            cursor.execute("SELECT id FROM voting_user WHERE username = %s", (user['username'],))
            if cursor.fetchone():
                print(f"User {user['username']} already exists, skipping...")
                continue
            
            # Insert user (with default password)
            cursor.execute("""
                INSERT INTO voting_user (
                    id, username, email, first_name, last_name, role, 
                    is_staff, is_active, date_joined, password
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                user['id'], user['username'], user['email'], 
                user['first_name'], user['last_name'], user['role'],
                user['is_staff'], user['is_active'], user['date_joined'],
                'pbkdf2_sha256$1000000$default$defaultpassword123'  # Default password hash
            ))
            
            imported_count += 1
            print(f"Imported user: {user['username']}")
            
        except Exception as e:
            print(f"Error importing user {user['username']}: {e}")
    
    conn.commit()
    print(f"Imported {imported_count} users")
    return imported_count

def import_votes(conn, votes_data):
    """Import votes data"""
    cursor = conn.cursor()
    
    print("Importing votes...")
    imported_count = 0
    
    for vote in votes_data:
        try:
            # Check if vote already exists for this voter
            cursor.execute("SELECT id FROM voting_vote WHERE voter_id = %s", (vote['voter_id'],))
            if cursor.fetchone():
                print(f"Vote already exists for voter_id {vote['voter_id']}, skipping...")
                continue
            
            # Check if voter and candidate exist
            cursor.execute("SELECT id FROM voting_user WHERE id = %s", (vote['voter_id'],))
            if not cursor.fetchone():
                print(f"Voter with id {vote['voter_id']} not found, skipping vote...")
                continue
            
            cursor.execute("SELECT id FROM voting_candidate WHERE id = %s", (vote['candidate_id'],))
            if not cursor.fetchone():
                print(f"Candidate with id {vote['candidate_id']} not found, skipping vote...")
                continue
            
            # Insert vote
            cursor.execute("""
                INSERT INTO voting_vote (id, voter_id, candidate_id, timestamp)
                VALUES (%s, %s, %s, %s)
            """, (vote['id'], vote['voter_id'], vote['candidate_id'], vote['timestamp']))
            
            imported_count += 1
            print(f"Imported vote: voter {vote['voter_id']} -> candidate {vote['candidate_id']}")
            
        except Exception as e:
            print(f"Error importing vote: {e}")
    
    conn.commit()
    print(f"Imported {imported_count} votes")
    return imported_count

def main():
    parser = argparse.ArgumentParser(description='Import local data to production database')
    parser.add_argument('--database-url', required=True, help='PostgreSQL database URL')
    parser.add_argument('--clear-existing', action='store_true', help='Clear existing data before import')
    
    args = parser.parse_args()
    
    # Connect to database
    conn = connect_to_database(args.database_url)
    if not conn:
        return
    
    print("Connected to production database!")
    
    # Clear existing data if requested
    if args.clear_existing:
        print("Clearing existing data...")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM voting_vote")
        cursor.execute("DELETE FROM voting_candidate")
        cursor.execute("DELETE FROM voting_user WHERE is_superuser = false")  # Keep superusers
        conn.commit()
        print("Existing data cleared!")
    
    # Load exported data
    try:
        with open('candidates_export.json', 'r') as f:
            candidates_data = json.load(f)
        
        with open('users_export.json', 'r') as f:
            users_data = json.load(f)
        
        with open('votes_export.json', 'r') as f:
            votes_data = json.load(f)
        
        print(f"Loaded data: {len(candidates_data)} candidates, {len(users_data)} users, {len(votes_data)} votes")
        
    except FileNotFoundError as e:
        print(f"Export file not found: {e}")
        print("Please run the export script first to create the JSON files.")
        return
    
    # Import data
    candidates_imported = import_candidates(conn, candidates_data)
    users_imported = import_users(conn, users_data)
    votes_imported = import_votes(conn, votes_data)
    
    # Summary
    print("\n" + "="*50)
    print("IMPORT SUMMARY")
    print("="*50)
    print(f"Candidates imported: {candidates_imported}")
    print(f"Users imported: {users_imported}")
    print(f"Votes imported: {votes_imported}")
    print("="*50)
    
    conn.close()
    print("Import completed!")

if __name__ == '__main__':
    main()
