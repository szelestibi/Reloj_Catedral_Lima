#!/bin/bash

#git config --global init.defaultBranch main
#git config --global user.email "szelest@web.de"
#git config --global user.name "Tiberio Szeles"
#git init
#git add .
#git commit -m "Initial commit"
#git remote add origin https://github.com/szelestibi/Reloj_Catedral_Lima
#git branch -M main
#git push -u origin main
#git push --force-with-lease origin main
#git push --force origin main
#ssh-keygen -t edXXXXX -C "szelest@web.de"
#eval "$(ssh-agent -s)"
#ssh-add ~/.ssh/id_edXXXXX
#git remote set-url origin git@github.com:szelestibi/Reloj_Catedral_Lima.git
#git push -u origin main
git add -A
#it commit -m "2025.11.05 20:00:00"
git commit -m "$(date '+%Y.%m.%d %H:%M:%S')"
git push origin main
