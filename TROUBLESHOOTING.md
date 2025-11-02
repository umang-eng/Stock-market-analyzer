# 🔧 Troubleshooting Guide

Common issues and their solutions for the Fintech AI News Platform.

## 🚨 Common Issues

### 1. Vite Dev Server Won't Start

**Error**: "Dynamic require of ... is not supported"

**Cause**: CommonJS/ESM module conflict in config files.

**Solution**: 
```bash
# Already fixed in the project, but if you see this error:
# Make sure vite.config.js uses ES module syntax
# Other configs should use .cjs extension
```

### 2. Blank Screen / No Styling

**Symptoms**: Browser shows blank page or unstyled content.

**Solutions**:
1. **Check mock backend is running**:
   ```bash
   curl http://localhost:3001/health
   ```

2. **Hard refresh browser**: `Cmd+Shift+R` (Mac) or `Ctrl+Shift+R` (Windows/Linux)

3. **Clear cache and restart**:
   ```bash
   pkill -f vite
   rm -rf node_modules/.vite
   npm run dev
   ```

### 3. Port Already in Use

**Error**: "Port 5173 is already in use"

**Solution**:
```bash
# Kill process on port 5173
lsof -ti:5173 | xargs kill -9

# Or specify different port
npm run dev -- --port 5174
```

### 4. Mock Backend Connection Error

**Error**: "Failed to fetch" in browser console

**Solutions**:
1. **Check backend is running**:
   ```bash
   # Terminal 1
   cd mock-backend
   node server.js
   ```

2. **Check API endpoints**:
   ```bash
   curl http://localhost:3001/market-data
   curl http://localhost:3001/articles
   ```

3. **Verify CORS**:
   - Backend should log: "🚀 Mock Backend Server running on http://localhost:3001"

### 5. Tailwind Styles Not Loading

**Symptoms**: No styling applied

**Solutions**:
1. **Check config files exist**:
   ```bash
   ls -la | grep config
   ```

2. **Restart dev server**:
   ```bash
   pkill -f vite
   npm run dev
   ```

3. **Clear PostCSS cache**:
   ```bash
   rm -rf node_modules/.cache
   ```

### 6. Module Not Found Errors

**Error**: "Cannot find module 'X'"

**Solution**:
```bash
# Clean install dependencies
rm -rf node_modules package-lock.json
npm install
```

### 7. API Endpoint 404

**Error**: "404 Not Found" for API calls

**Solutions**:
1. **Check environment variables**:
   ```bash
   cat .env
   # Should have: VITE_AI_API_URL=http://localhost:3001
   ```

2. **Verify mock backend routes**:
   Check `mock-backend/server.js` has all required endpoints

3. **Restart both servers**:
   ```bash
   # Terminal 1: Backend
   cd mock-backend && node server.js
   
   # Terminal 2: Frontend
   npm run dev
   ```

### 8. Build Errors

**Error**: Build fails with various errors

**Solutions**:
1. **Check Node.js version**:
   ```bash
   node -v  # Should be 18+
   ```

2. **Update dependencies**:
   ```bash
   npm update
   ```

3. **Clean build**:
   ```bash
   rm -rf dist node_modules/.vite
   npm run build
   ```

### 9. Git Issues

**Error**: Cannot push to GitHub

**Solutions**:
1. **Check authentication**:
   ```bash
   git config --global user.email "your-email@example.com"
   git config --global user.name "Your Name"
   ```

2. **Pull before push**:
   ```bash
   git pull origin main
   git push origin main
   ```

### 10. Firebase/Firestore Issues

**Error**: Firebase connection issues

**Solutions**:
1. **Check credentials file**:
   ```bash
   ls -la | grep firebase
   # Should not expose credentials in git
   ```

2. **Verify Firebase project**:
   - Check Firestore is enabled
   - Verify project ID is correct

## 🛠️ Quick Fixes

### Complete Reset (Nuclear Option)

If nothing works:
```bash
# Backup your work first!
git add -A
git commit -m "Backup before reset"

# Then reset
rm -rf node_modules dist .vite
npm install
cd mock-backend
rm -rf node_modules
npm install
cd ..
npm run dev
```

### Check System Requirements

```bash
# Node.js version
node -v  # Should be 18.0.0 or higher

# npm version
npm -v  # Should be 9.0.0 or higher

# Disk space
df -h

# Memory
free -h  # Linux
vm_stat  # macOS
```

## 📊 Diagnostic Commands

Run these to get diagnostic info:

```bash
# Check all services
echo "=== Node.js ==="
node -v
echo "=== npm ==="
npm -v
echo "=== Vite ==="
npx vite --version
echo "=== Running Processes ==="
ps aux | grep -E "(vite|node)" | grep -v grep

# Check network
echo "=== Port 5173 (Vite) ==="
lsof -i :5173
echo "=== Port 3001 (Mock Backend) ==="
lsof -i :3001

# Check logs
echo "=== Recent npm logs ==="
tail -20 ~/.npm/_logs/$(ls -t ~/.npm/_logs | head -1)
```

## 🆘 Still Stuck?

1. **Check GitHub Issues**: [Open an issue](https://github.com/umang-eng/Stock-market-analyzer/issues)
2. **Read Documentation**: Review [README.md](./README.md) and [QUICKSTART.md](./QUICKSTART.md)
3. **Browser Console**: Check for detailed errors (F12)
4. **Terminal Logs**: Look for error messages in terminal output

## 📝 Common File Locations

```
Project Root/
├── src/               # Source code
├── mock-backend/      # Development API
├── node_modules/      # Dependencies (don't edit)
├── dist/              # Build output
├── .vite/             # Vite cache
├── .env               # Environment variables
├── vite.config.js     # Vite configuration
├── tailwind.config.cjs # Tailwind configuration
└── postcss.config.cjs # PostCSS configuration
```

## ✅ Healthy System Checklist

Before reporting an issue, verify:

- [ ] Node.js 18+ installed
- [ ] All dependencies installed (`npm install`)
- [ ] No errors in terminal when running `npm run dev`
- [ ] Mock backend running on port 3001
- [ ] Frontend running on port 5173
- [ ] Browser console has no errors
- [ ] Network tab shows successful API calls
- [ ] No conflicting processes on ports

---

**Last Updated**: January 2025

