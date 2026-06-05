# GitHub Setup

This project is ready to be added to a GitHub repository.

## Steps to add your project to GitHub

1. Create a new empty repository on GitHub.
2. From the project root, run:
   ```bash
   git init
   git branch -M main
   git remote add origin https://github.com/<your-username>/<your-repo>.git
   git add .
   git commit -m "Initial project commit"
   git push -u origin main
   ```

## If you already have a GitHub repository

Replace the `remote add` command with your existing repository URL:
```bash
git remote add origin https://github.com/<your-username>/<your-repo>.git
```

## Important notes

- The repository already ignores common sensitive files, including `.env`.
- Do not commit API keys or secrets. Keep them only in local `.env` or service environment variables.
- For Streamlit Cloud, set `API_URL` in the app settings to point to your deployed backend.
