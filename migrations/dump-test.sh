#!/usr/bin/env bash

# MariaDB [(none)]> SELECT @@character_set_database;
# +--------------------------+
# | @@character_set_database |
# +--------------------------+
# | utf8mb4                  |
# +--------------------------+

# this is a hack https://stackoverflow.com/questions/1916392/how-can-i-get-rid-of-these-comments-in-a-mysql-dump
pg_dump -U milestones -W -Fp --no-owner --no-acl --schema-only -d blueboard_milestones > schema.sql
