# 🚀 GIT BASH COMMANDS FOR GITHUB PUSH

Git is working! Now use Git Bash to push to GitHub.

## 📋 EXACT COMMANDS TO RUN IN GIT BASH:

### Step 1: Configure Git (run once)
```bash
git config --global user.name "Nithish0333"
git config --global user.email "nithishh7639@gmail.com"
```

### Step 2: Create .gitignore file
```bash
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
venv/
env/
ENV/

# Django
*.log
local_settings.py
db.sqlite3
db.sqlite3-journal

# Environment Variables
.env
.venv

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Node.js
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Frontend build
frontend/dist/
frontend/build/

# Media files
backend/media/
backend/staticfiles/

# Temporary files
*.tmp
*.temp
EOF
```

### Step 3: Add all files
```bash
git add .
```

### Step 4: Make initial commit
```bash
git commit -m "Initial commit: CookieCrave E-commerce Platform"
```

### Step 5: Add remote repository
```bash
git remote add origin https://github.com/Nithish0333/CookieCrave.git
```

### Step 6: Push to GitHub
```bash
git branch -M main
git push -u origin main
```

## 🔑 GITHUB CREDENTIALS

When prompted:
- **Username**: `Nithish0333`
- **Password**: Use Personal Access Token (not your GitHub password)
- **Create token**: https://github.com/settings/tokens

## 🎯 SUCCESS!

After completing these steps, your project will be on GitHub at:
**https://github.com/Nithish0333/CookieCrave**

## 📋 ALL COMMANDS IN ONE BLOCK

Copy and paste this entire block in Git Bash:

```bash
git config --global user.name "Nithish0333"
git config --global user.email "nithishh7639@gmail.com"
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
venv/
env/
ENV/

# Django
*.log
local_settings.py
db.sqlite3
db.sqlite3-journal

# Environment Variables
.env
.venv

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Node.js
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Frontend build
frontend/dist/
frontend/build/

# Media files
backend/media/
backend/staticfiles/

# Temporary files
*.tmp
*.temp
EOF
git add .
git commit -m "Initial commit: CookieCrave E-commerce Platform"
git remote add origin https://github.com/Nithish0333/CookieCrave.git
git branch -M main
git push -u origin main
```

## 🚀 READY TO PUSH!

Open Git Bash and run the commands above. Your CookieCrave project will be live on GitHub!
