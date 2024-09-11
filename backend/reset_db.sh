#!/bin/bash
echo "Resetting the database and re-running migrations and seeds..."
rm -f dev.db
rm -rf migrations/versions/*
flask db init
flask db migrate
flask db upgrade
flask seed all
echo "Database reset and seeded successfully."
