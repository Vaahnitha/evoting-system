# Data Sync Instructions

This guide will help you sync your local database data to the Render production database.

## What We're Syncing

**Candidates (4 total):**
- john doe (eng)
- jane doe (hr) 
- alex b (pm)
- cow (moo)

**Users (5 total):**
- Vaahnitha (superuser)
- employee1 (employee)
- Admin (superuser)
- localadmin (superuser)
- admin (superuser)

**Votes (3 total):**
- employee1 voted for john doe
- Vaahnitha voted for john doe
- localadmin voted for jane doe

## Method 1: Automatic Import on Startup (Recommended for Free Tier)

### Step 1: Deploy with Updated Configuration
1. Commit and push your changes to GitHub
2. Redeploy your Render service to pick up the updated `render.yaml` with PostgreSQL connection and `IMPORT_LOCAL_DATA=true`

### Step 2: Automatic Import
The data will be automatically imported when your application starts up! No shell access needed.

**What happens:**
- When Render deploys your app, it will run migrations first
- Then it will automatically import all your local data
- The import only runs if the database is empty (safe to run multiple times)
- You'll see import messages in the Render logs

### Step 3: Verify Import
1. Check your API endpoint: `https://evoting-system-z3os.onrender.com/api/candidates/`
2. You should see all 4 candidates
3. Try logging in with any of the user credentials
4. Check Render logs to see import messages

## Method 2: Using Django Management Command (Requires Shell Access)

**Note:** This method requires Render shell access, which is not available on the free tier.

### Step 1: Deploy with Updated Configuration
1. Commit and push your changes to GitHub
2. Redeploy your Render service to pick up the updated `render.yaml` with PostgreSQL connection

### Step 2: Run Import Command on Render
1. Go to your Render dashboard
2. Navigate to your backend service
3. Go to the "Shell" tab
4. Run the following command:

```bash
python manage.py import_local_data
```

This will import all the data using hardcoded values (no JSON files needed).

### Step 3: Verify Import
1. Check your API endpoint: `https://evoting-system-z3os.onrender.com/api/candidates/`
2. You should see all 4 candidates
3. Try logging in with any of the user credentials

## Method 3: Using JSON Files (Alternative)

### Step 1: Upload JSON Files to Render
1. Upload the exported JSON files (`candidates_export.json`, `users_export.json`, `votes_export.json`) to your Render service
2. You can do this by:
   - Adding them to your GitHub repository
   - Or uploading them via Render's file manager

### Step 2: Run Import Command
```bash
python manage.py import_local_data
```

## Method 4: Manual Database Import (Advanced)

If you have direct access to your PostgreSQL database:

### Step 1: Get Database Connection String
1. Go to your Render dashboard
2. Navigate to your PostgreSQL database
3. Copy the connection string

### Step 2: Run Import Script Locally
```bash
python import_to_production.py --database-url "postgresql://..."
```

## Default Passwords

All imported users will have the default password: `defaultpassword123`

**Important:** Users should change their passwords after the first login for security.

## Troubleshooting

### If Import Fails
1. Check that your Render service is using the production settings
2. Verify the PostgreSQL database is connected
3. Check the Render logs for error messages

### If Users Can't Login
1. Verify the users were imported correctly
2. Check that the default password is being used
3. Try resetting passwords through Django admin

### If Candidates Don't Appear
1. Check the API endpoint directly
2. Verify the candidates were imported
3. Check for any authentication issues

## Verification Commands

After import, you can verify the data by running these commands in Render shell:

```bash
# Check candidates
python manage.py shell -c "from voting.models import Candidate; print([c.name for c in Candidate.objects.all()])"

# Check users
python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); print([u.username for u in User.objects.all()])"

# Check votes
python manage.py shell -c "from voting.models import Vote; print([f'{v.voter.username} -> {v.candidate.name}' for v in Vote.objects.all()])"
```

## Security Notes

- All imported users have the same default password
- Users should change their passwords immediately
- The import preserves existing superuser accounts
- Vote data is preserved to maintain election integrity
