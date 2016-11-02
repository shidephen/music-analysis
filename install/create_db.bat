@echo off
ECHO "start to import mysql"
mysql -h127.0.0.1 -uroot -ptuya2016 music_db < db.sql
ECHO "import mysql end"