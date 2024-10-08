#!/bin/sh
TIMESTAMP=$(date +"%Y%m%d%H%M%S")
BACKUP_DIR="/backup/dumps/$TIMESTAMP"
mkdir -p "$BACKUP_DIR"
cp -r ../data/* "$BACKUP_DIR" # Podemos apontar para o GCS, etc... Para mais segurança. Somente para demonstração
echo "Backup realizado em $BACKUP_DIR"