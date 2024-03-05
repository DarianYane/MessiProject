#!/bin/bash
FILE_NAME=$(date +%F-%H_%M_Automations.sql)

mysqldump -u root -ppgl8677 --databases Automations > /usr/db-backup/$FILE_NAME