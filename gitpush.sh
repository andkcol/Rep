#!/bin/bash
cd /home/andy/MoodiAlgo/Rep
git add .
git commit -m "Auto update from RPI on $(date)"
git push origin main
