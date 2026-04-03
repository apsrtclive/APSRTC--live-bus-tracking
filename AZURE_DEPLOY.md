# ☁️ Azure Deployment Guide

This guide will walk you through the process of deploying the APSRTC Live Bus Tracking system to Microsoft Azure using **Azure App Service (Linux)**. The project is already pre-configured with the necessary startup scripts (`startup.sh` and `.deployment`) to make this process seamless.

---

## 1. Prerequisites 
- An active [Microsoft Azure account](https://azure.microsoft.com/en-us/free/).
- Your code must be pushed to a **GitHub repository** (this project is already set up as a Git repository). Make sure all your recent changes are pushed.

## 2. Create the Azure App Service
1. Log in to the [Azure Portal](https://portal.azure.com/).
2. In the search bar at the top, type **"App Services"** and select it.
3. Click the **"+ Create"** button and choose **"Web App"**.
4. Fill in the **Basics** tab:
   - **Subscription**: Select your active subscription.
   - **Resource Group**: Click "Create new" and name it (e.g., `APSRTC-RG`).
   - **Name**: Give your app a unique name (e.g., `apsrtc-live-vizag`). This will become your URL: `https://apsrtc-live-vizag.azurewebsites.net`.
   - **Publish**: Select **Code**.
   - **Runtime stack**: Choose **Python 3.11** (or 3.10 depending on your environment).
   - **Operating System**: **Linux**.
   - **Region**: Choose the region closest to your users (e.g., *South India* or *Central India*).
   - **Pricing Plan**: You can choose the **Free F1** tier for testing, or a **Basic (B1)** tier if you need more resources like Always On.
5. Click **"Review + create"**, and then **"Create"**. Wait for the resource to be deployed (this takes a few minutes).

## 3. Connect to GitHub (Continuous Deployment)
Once your Web App is deployed, go to the resource page by clicking **"Go to resource"**.

1. In the left navigation menu under **Deployment**, click **Deployment Center**.
2. Under "Source", select **GitHub**.
3. Authorize Azure to access your GitHub account if prompted.
4. Fill in the connection details:
   - **Organization**: Your GitHub username.
   - **Repository**: Select your `APSRTC--live-bus-tracking` repository.
   - **Branch**: Select the branch you want to deploy (usually `main` or `master`).
5. Click **"Save"** at the top. This will automatically create a GitHub Action in your repository and queue your first build!

## 4. Configure Application Settings
Your application requires environment variables and a specific startup command to run correctly with WebSockets.

1. In the left navigation menu under **Settings**, click **Environment variables** (or **Configuration** in some portal versions).
2. Under the **App settings** tab, click **"+ Add"** to create a new setting:
   - **Name**: `SECRET_KEY`
   - **Value**: *(enter a secure random string, e.g. `aprtc_my_secure_prod_key`)*
3. Add another setting if it doesn't exist:
   - **Name**: `WEBSITES_ENABLE_APP_SERVICE_STORAGE`
   - **Value**: `true`
   *(This ensures your SQLite database file isn't deleted when the server restarts).*
4. Click **Apply / Save** at the bottom/top.

## 5. Configure the Startup Command & WebSockets
Although the repository has a `.deployment` file, setting the Startup Command explicitly in Azure ensures maximum reliability:

1. In the Azure Portal, go back to **Configuration** > **General settings**.
2. Scroll down to the **Startup Command** field.
3. Enter exactly:
   ```bash
   bash startup.sh
   ```
4. Turn **Web sockets** to **On** (very important for live tracking).
5. Ensure **Always On** is set to **On** (if you chose a Basic/Standard tier; the Free tier doesn't support Always On but it works fine for testing).
6. Click **Save** and wait for the app to restart.

## 6. Verify the Deployment
1. Go to the **Overview** page of your App Service.
2. Click the **Default domain** link (e.g., `https://apsrtc-live-vizag.azurewebsites.net`).
3. You should see your live bus tracking application running! The database will be automatically initialized by the startup script on the first run.

---

> **Note on Databases:** Since you are using **SQLite**, the database file (`apsrtc_local.db`) will be stored within the App Service filesystem. If you plan to heavily scale the application to multiple instances in the future, you will need to provision an **Azure Database for PostgreSQL** and set the `DATABASE_URL` app setting with the connection string.
