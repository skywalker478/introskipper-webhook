# Intro Skipper Webhook for Jellyfin

This project provides a lightweight Flask-based webhook to automate **Intro Skipper tasks** in Jellyfin, triggered by Sonarr or Radarr events. It’s containerized with Docker and easily deployable via Docker Compose.

---

## **Features**

* Triggers **Intro Skipper Clean Cache** immediately when media is imported or upgraded.
* Waits a short delay (`DELAY_SECONDS`) for Jellyfin library scan to finish.
* Triggers **Detect & Analyze Media Segments** automatically after the delay.
* Works with both **Sonarr** and **Radarr** webhooks.
* Fully configurable via `.env`.

---

## **Repository Structure**

```
.
├── app.py
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── .env.example
└── README.md
```

---

## **Getting Started**

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/introskipper-webhook.git
cd introskipper-webhook
```

### 2. Copy `.env.example` to `.env` and edit

```bash
cp .env.example .env
```

Edit `.env` with your actual values:

```env
JELLYFIN_URL=https://your_jellyfin_url_here
JELLYFIN_API_KEY=your_api_key_here
CLEAN_CACHE_TASK_ID=your_clean_cache_guid
ANALYZE_TASK_ID=your_analyze_task_guid
DELAY_SECONDS=300  # 5 minutes delay to account for library scan
```

> **Note:** Do **not** commit `.env` to GitHub; it contains sensitive keys.

---

### 3. Build and run with Docker Compose

```bash
docker-compose up -d
```

* The webhook will run on **port 5000**.
* Logs are viewable via:

```bash
docker-compose logs -f introskipper-webhook
```

---

### 4. Configure Sonarr / Radarr Webhooks

* Use your container’s IP (or host) and port `5000` with the path `/trigger`.
* Recommended triggers:

**Sonarr:**

* On Import
* On Upgrade
* On Series Delete
* On Episode File Delete / For Upgrade

**Radarr:**

* On Import
* On Upgrade
* On Movie Delete
* On Movie File Delete / For Upgrade

---

### 5. Optional: Adjust Delay

* `DELAY_SECONDS` in `.env` sets the wait time before triggering the **Detect & Analyze Media Segments** task.
* Default: `300` seconds (5 minutes).

---

### 6. Stopping the Service

```bash
docker-compose down
```

---

### 7. Updating

If you make changes to `app.py` or dependencies:

```bash
docker-compose build
docker-compose up -d
```

---

### 8. License

This project is licensed under the GNU GENERAL PUBLIC LICENSE v3.0. See [LICENSE](LICENSE).
