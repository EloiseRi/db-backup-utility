# DB Backup Utility

## 📑​ Description
**DB Backup Utility** is a command-line tool designed to simplify database backup and restoration.  
It supports multiple database management systems (DBMS) and provides an intuitive interface for automating backups and restores.
**⚠️ Keep in mind that this is an ongoing project — improvements and new features are expected in future updates.**

## ⚡ Features
✔️ Simple and intuitive CLI  
✔️ Backup a database  
✔️ Restore a database from a backup file  
✔️ Support for MySQL, PostgreSQL, and SQLite (more to be added)  
✔️ Manage backup files with timestamped naming  
 
## 🔧 Installation & Requirements

### 📌 Requirements  
- Python 3.8+  
- Database client tools (e.g., `mysqldump` for MySQL, `pg_dump` for PostgreSQL) 

### Installation

#### 1. Clone the repository

```bash
git clone https://github.com/EloiseRi/db-backup-utility.git
cd mysql-backup-tool
```


#### 2. (Optional) Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

#### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## ⚙️ Configuration

Setup a `config.yaml` file at the root of the project based on the config.example.yaml:

```yaml
database:
  type: db-type #mtsql, postgresql, mongodb
  host: localhost
  port: 3000
  user: usr
  password: pwd
  dbname: dbname

backup:
  backup_dir: path/to/backup_dir
  backup_type: full
  compress: false

cloud:
  aws:
    enabled: false
    access_key_id: YOUR_AWS_ACCESS_KEY_ID
    secret_access_key: YOUR_AWS_SECRET_ACCESS_KEY
    region: us-east-1
    bucket_name: YOUR_BUCKET_NAME

  gcp:
    enabled: false
    service_account_key: YOUR_SERVICE_ACCOUNT_KEY
    bucket_name: YOUR_BUCKET_NAME

  azure:
    enabled: false
    connection_string: YOUR_CONNECTION_STRING
    container_name: YOUR_CONTAINER_NAME

notifications:
  slack:
    enabled: false
    webhook_url: YOUR_SLACK_WEBHOOK_URL
```

> ✅ Use **absolute paths** for `backup_dir` to avoid path issues.

---

## 🚀 Usage

You can run a backup directly using the main script:

```bash
python -m backup_utility [ backup | restore ] --config config.yaml
```

### ✅ Available Arguments

| Argument       | Description                                                | Required | Example                           |
|----------------|------------------------------------------------------------|----------|-----------------------------------|
| `--config`     | Path to the YAML config file                               | ✅       | `--config config.yaml`            |
| `--type`       | Backup type: `full`, `incremental`, or `differential`      | ❌       | `--type full`                     |
| `--compress`   | Override compression setting from config (`true` or `false`) | ❌       | `--compress true`                 |

---

## 📟 Logging

Execution logs and error messages are saved to a file named `db_backup.log` in the project root.

---

## 🧠 Notes

- Ensure `mysqldump` is installed and accessible from your system's `PATH`.
- **Incremental** and **differential** backup types require implementation if not yet supported.
- When compression is enabled, the raw `.sql` file is automatically deleted after the `.gz` file is created.
