#!/bin/bash

git config --global init.defaultBranch main
git config --global user.email "szelest@web.de"
git config --global user.name "Tiberio Szeles"
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/szelestibi/Reloj_Catedral_Lima
git branch -M main
#git push -u origin main
