# Vercel Deployment Guide

This guide will help you deploy your React frontend to Vercel.

## Prerequisites

- ✅ Backend deployed on Render: `https://evoting-system-h779.onrender.com`
- ✅ Backend API working with all data imported
- ✅ Frontend code ready in the `frontend/` directory

## Deployment Steps

### Step 1: Prepare Your Repository

1. **Commit all changes:**
   ```bash
   git add .
   git commit -m "Prepare for Vercel deployment"
   git push origin main
   ```

### Step 2: Deploy to Vercel

#### Option A: Deploy via Vercel Dashboard (Recommended)

1. **Go to [vercel.com](https://vercel.com) and sign in**
2. **Click "New Project"**
3. **Import your GitHub repository:**
   - Select your `evoting-system` repository
   - Click "Import"

4. **Configure the project:**
   - **Framework Preset:** Create React App
   - **Root Directory:** `frontend`
   - **Build Command:** `npm run build`
   - **Output Directory:** `build`
   - **Install Command:** `npm install`

5. **Set Environment Variables:**
   - `REACT_APP_RENDER_BACKEND_URL` = `https://evoting-system-h779.onrender.com/api`
   - `REACT_APP_API_URL` = `https://evoting-system-h779.onrender.com/api`
   - `REACT_APP_FORCE_REMOTE` = `true`

6. **Click "Deploy"**

#### Option B: Deploy via Vercel CLI

1. **Install Vercel CLI:**
   ```bash
   npm i -g vercel
   ```

2. **Login to Vercel:**
   ```bash
   vercel login
   ```

3. **Deploy from the project root:**
   ```bash
   vercel --prod
   ```

4. **Set environment variables:**
   ```bash
   vercel env add REACT_APP_RENDER_BACKEND_URL
   # Enter: https://evoting-system-h779.onrender.com/api
   
   vercel env add REACT_APP_API_URL
   # Enter: https://evoting-system-h779.onrender.com/api
   
   vercel env add REACT_APP_FORCE_REMOTE
   # Enter: true
   ```

5. **Redeploy with environment variables:**
   ```bash
   vercel --prod
   ```

### Step 3: Verify Deployment

1. **Check your Vercel URL** (e.g., `https://your-app.vercel.app`)
2. **Test the application:**
   - Visit the homepage
   - Try logging in with: `admin` / `defaultpassword123`
   - Check if candidates are displayed
   - Test voting functionality

### Step 4: Update CORS Settings (If Needed)

If you encounter CORS errors, update your Render backend:

1. **Go to Render Dashboard → Your Backend Service → Environment**
2. **Update CORS_ALLOWED_ORIGINS:**
   ```
   https://your-app.vercel.app
   ```

3. **Redeploy the backend**

## Configuration Files

### vercel.json
```json
{
  "version": 2,
  "builds": [
    {
      "src": "frontend/package.json",
      "use": "@vercel/static-build",
      "config": {
        "distDir": "build"
      }
    }
  ],
  "routes": [
    {
      "src": "/static/(.*)",
      "dest": "/frontend/build/static/$1"
    },
    {
      "src": "/(.*)",
      "dest": "/frontend/build/$1"
    }
  ],
  "env": {
    "REACT_APP_RENDER_BACKEND_URL": "https://evoting-system-h779.onrender.com/api",
    "REACT_APP_API_URL": "https://evoting-system-h779.onrender.com/api",
    "REACT_APP_FORCE_REMOTE": "true"
  }
}
```

## Environment Variables

| Variable | Value | Description |
|----------|-------|-------------|
| `REACT_APP_RENDER_BACKEND_URL` | `https://evoting-system-h779.onrender.com/api` | Backend API URL |
| `REACT_APP_API_URL` | `https://evoting-system-h779.onrender.com/api` | Alternative API URL |
| `REACT_APP_FORCE_REMOTE` | `true` | Force remote API usage |

## Testing Checklist

- [ ] Frontend loads without errors
- [ ] Login page displays correctly
- [ ] Can login with admin credentials
- [ ] Candidates are displayed
- [ ] Voting functionality works
- [ ] Results page works (for admin users)
- [ ] No CORS errors in browser console
- [ ] API calls are successful

## Troubleshooting

### Common Issues

1. **CORS Errors:**
   - Update `CORS_ALLOWED_ORIGINS` in Render backend
   - Include your Vercel domain

2. **API Connection Issues:**
   - Verify environment variables are set correctly
   - Check that backend is running on Render
   - Test API endpoints directly

3. **Build Failures:**
   - Check that all dependencies are in `package.json`
   - Verify Node.js version compatibility
   - Check for TypeScript errors

4. **Routing Issues:**
   - Ensure `vercel.json` routes are configured correctly
   - Check that React Router is set up properly

### Getting Help

- Check Vercel deployment logs
- Check browser console for errors
- Test API endpoints directly with Postman
- Verify environment variables in Vercel dashboard

## Next Steps

After successful deployment:

1. **Set up custom domain** (optional)
2. **Configure automatic deployments** from GitHub
3. **Set up monitoring** and error tracking
4. **Update documentation** with production URLs

Your e-voting system will be live and accessible to users! 🎉
