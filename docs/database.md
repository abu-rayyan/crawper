## Crawper Database Configurations
Use the following guideline for creating backup dumps and restoring backup dumps. 
This guide is intended to use of **linux deployment environment** and **postgre-sql** database.
Tested on **Ubuntu**.

### Creating backup
Use the following steps to create backup of the existing database.
   1. Log in to the user **postgres**
   ```bash
      sudo su postgres  
   ```
   2. Use **pg_dump** command to create backup.
   ```bash
        pg_dump dbname > outfile
   ```
   3. To create a backup on a remote system use:
   ```bash
    pg_dump -h remote_host -p remote_port name_of_database > name_of_backup_file
   ```
### Restoring backup
To restore backup to the postgres follow the following steps:
1. Login to the postgres user
    ```bash
    sudo su postgres
    ```
2. For a .sql file use
    ```bash
    psql -U <username> -d <dbname> -1 -f <filename>.sql   
    ```
3. For custom backup file use
    ```bash
    pg_restore -U <username> -d <dbname> -1 <filename>.dump
    ```
4. For Automatic create Schema and restore Data
   ```bash
   psql dbname < infile
   ```
