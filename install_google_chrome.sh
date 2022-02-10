sudo apt install xdg-utils wget fonts-liberation -y
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo dpkg --install google-chrome-stable_current_amd64.deb
rm -rf google-chrome-stable_current_amd64.deb
which google-chrome