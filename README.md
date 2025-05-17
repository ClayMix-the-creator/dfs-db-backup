# DFS DB and Backup Service 💾🔄

A robust and distributed database startup and backup solution designed for cloud environments. Part of the Distributed File System Project with:
- [Nikita Maximenko](https://github.com/Nexonm)
- [Ilsaf Abdulkhakov](https://github.com/harutoyume)

Check out other Project Repositories:
- [Web Server](https://github.com/harutoyume/dfs_web_server)
- [Metadata Server](https://github.com/Nexonm/dfs-metadata)
- [Storage Node](https://github.com/Nexonm/dfs-storage-node)

## Overview 📖

DFS Database and Backup service is a database startup and its backup utility that seamlessly integrates with distributed file systems (DFS) to provide a reliable and scalable service. Ideal for enterprise environments and distributed systems that require consistent data protection.

**Key Features**:
- 💾 Running a PostgreSQL database
- 🚀 Automated database backup
- ⏱️ Point-in-time restore capability.
- 🔄 Cross-platform compatibility
- 📋 Detailed backup auditing

## Installation ⚙️

### Prerequisites
- Python 3.12+
- Access to supported database systems

### Quick Start
```bash
# Сlone repository
git clone https://github.com/ClayMix-the-creator/dfs-db-backup.git
cd dfs-db-backup
pip install -r requirements.txt
```

## Configuration ⚙️

Set environment variables in :
```bash
# Docker config
CONTAINER_DB='<Name of database container>'
CONTAINER_BACKUP='<Name of backup container>'

# Database config
DB_USER='<Database user>'
DB_PASSWORD='<Database password>'
DB_HOST=${CONTAINER_DB}
DB_PORT='<Host OS port for database>'
DB_NAME='<Database name>'

# Backup config
BACKUP_DIR='<Name of backup directory>'
BACKUP_PORT='<Host OS port for backup>'
BACKUP_REMOVAL_AMOUNT=<Max amount of backup files | 0 to disable>
BACKUP_REMOVAL_DAYS=<Max amount of days since backup created | 0 to disable>
BACKUP_REMOVAL_HOURS=<Max amount of hours since backup created | 0 to disable>
BACKUP_REMOVAL_MINUTES=<Max amount of minutes since backup created | 0 to disable>
BACKUP_REMOVAL_SECONDS=<Max amount of seconds since backup created | 0 to disable>
BACKUP_REMOVAL=...

BACKUP_INTERVAL_AMOUNT=<Backup creation time interval>
# seconds/minutes/hours/days
BACKUP_INTERVAL_TYPE=<Backup creation interval type>
BACKUP_INTERVAL=...
```

## Usage 🚀

Set up Docker Compose for the [Web Server](https://github.com/harutoyume/dfs_web_server)
```bash
docker-compose -f docker-compose-front.yml --env-file front.env up --build --force-recreate
```

Set up Docker Compose for the [Metadata Server](https://github.com/Nexonm/dfs-metadata)
```bash
docker-compose -f docker-compose-back.yml --env-file back.env up --build --force-recreate
```

## License 📄

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments 🙏

- Thanks to all contributors who help improve this project
- Inspired by enterprise backup solutions
- Built with ❤️ by ClayMix
