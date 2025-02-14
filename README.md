# Database Automation and CI/CD for Azure MySQL Flexible Server

## Overview
This project automates database schema changes and implements a CI/CD pipeline for **Azure MySQL Flexible Server** using **GitHub Actions** and **Azure CLI**.

## Prerequisites
Ensure you have the following installed on your system:
- [Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli)
- [MySQL Client](https://dev.mysql.com/downloads/)
- Python 3.x
- `mysql-connector-python` library
- `schema_changes.sql` (contains database schema changes)
- `ci_cd_pipeline.yml` (GitHub Actions workflow file)

## 1️⃣ Setting Up Azure MySQL Flexible Server

### **Step 1: Create a Resource Group**
```bash
az group create --name my-db-group --location eastus
```

### **Step 2: Create MySQL Flexible Server**
```bash
az mysql flexible-server create \
    --resource-group my-db-group \
    --name my-db-server1 \
    --location eastus \
    --admin-user admin_user \
    --admin-password "Project@db" \
    --sku-name Standard_B1ms \
    --storage-size 5120 \
    --version 5.7 \
    --public-access Enabled
```

### **Step 3: Create the `companydb` Database**
```bash
az mysql flexible-server db create \
    --resource-group my-db-group \
    --server-name my-db-server1 \
    --database-name companydb
```

## 2️⃣ Running the SQL Schema Script

Ensure the **`ca-cert.pem`** file is downloaded and placed in your project directory.

```bash
mysql -h my-db-server1.mysql.database.azure.com \
    -u admin_user -p \
    --ssl-ca="/Users/hululu/Documents/richard/ca-cert.pem" \
    --ssl companydb \
    -e "source /Users/hululu/Documents/richard/schema_changes.sql"
```

## 3️⃣ Running the Python Script for Automation
Ensure `mysql-connector-python` is installed:
```bash
pip install mysql-connector-python
```

Run the script:
```bash
python execute_sql.py
```

## 4️⃣ Implementing CI/CD with GitHub Actions

### **Step 1: Add Secrets to GitHub Repository**
Go to **GitHub → Settings → Secrets and Variables → Actions** and add the following:
- `AZURE_MYSQL_HOST` → `my-db-server1.mysql.database.azure.com`
- `AZURE_MYSQL_USER` → `admin_user`
- `AZURE_MYSQL_PASSWORD` → `Project@db`
- `AZURE_MYSQL_DATABASE` → `companydb`

### **Step 2: Configure GitHub Actions Workflow**
Ensure **`ci_cd_pipeline.yml`** exists in `.github/workflows/` directory.

Push the changes to trigger GitHub Actions:
```bash
git add .
git commit -m "Added CI/CD workflow"
git push origin main
```

## 5️⃣ Verification
To verify that the database changes have been applied successfully, run:
```bash
mysql -h my-db-server1.mysql.database.azure.com -u admin_user -p --ssl companydb -e "SHOW TABLES;"
```

## Cleanup 
To delete all resources:
```bash
az group delete --name my-db-group --yes --no-wait
```

## Conclusion
This setup ensures a **fully automated database deployment pipeline**, integrating **Azure MySQL Flexible Server**, **Python scripts**, and **GitHub Actions CI/CD**.



