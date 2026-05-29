# Step 7 — Put the app online

This is the moment your app becomes a real website that anyone can open. We use
**Streamlit Community Cloud**, which is **free** for public apps.

## 7.1 What you need first

- Your code on GitHub (Step 6). ✅
- The file `streamlit_app.py` at the top of your project. ✅
- The file `requirements.txt` at the top of your project. ✅

### Why `requirements.txt`?

Streamlit Community Cloud reads this file to know which libraries to install. It
is a simple list:

```
streamlit>=1.58.0
numpy>=2.4.6
pandas>=3.0.3
matplotlib>=3.10.9
plotly>=6.7.0
handcalcs>=1.11.0
```

Keep it in step with the dependencies in `pyproject.toml`.

> **Note:** Streamlit Community Cloud installs from `requirements.txt`, not from
> `uv.lock`. That is why we keep both. On your own computer you use uv; the cloud
> uses this simple list.

## 7.2 Sign in to Streamlit Community Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io).
2. Click **Sign in** and choose **Continue with GitHub**.
3. Allow Streamlit to see your GitHub repositories.

## 7.3 Create the app

1. Click **Create app** (or **New app**).
2. Choose **Deploy a public app from GitHub**.
3. Fill in the boxes:
   - **Repository:** `YOUR-NAME/strapp`
   - **Branch:** `main`
   - **Main file path:** `streamlit_app.py`
4. Click **Deploy**.

Streamlit now reads your repo, installs the libraries, and starts the app. The
first time takes a few minutes. You will see the logs scroll by.

## 7.4 Your app is live!

When it finishes, you get a public web address, something like:

```
https://strapp-yourname.streamlit.app
```

Share it with anyone. They can open it in a browser with nothing to install.

## 7.5 Updating the live app

This is the best part. To change your live app, you just push to GitHub:

```bash
git add .
git commit -m "Improve the chart colors"
git push
```

Streamlit Community Cloud notices the new code and **updates the app by itself**
in a minute or two. No extra steps.

## 7.6 If something goes wrong

- **The app shows an error about a missing library.** Check that the library is
  listed in `requirements.txt`, then push again.
- **The app says it cannot find your code.** Check the **Main file path** is
  `streamlit_app.py` and that this file is at the top of your repo.
- **You see an old version.** Open the app's menu (top right) and choose
  **Reboot app**.
- **Read the logs.** On the app page, click **Manage app** to see the logs. They
  usually tell you exactly what is wrong.

## 🎉 You did it!

You started with an empty folder and finished with a real, online tool that
teaches structural load combinations. Along the way you learned uv, Streamlit,
NumPy, pandas, Plotly, handcalcs, ruff, ty, pytest, git, GitHub, and cloud
deployment. That is a full, modern Python workflow.

Go back and read any step again whenever you build your next app. Well done!
