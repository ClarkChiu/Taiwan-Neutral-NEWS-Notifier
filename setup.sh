wget https://dl.google.com/linux/direct/google-chrome-beta_current_amd64.deb
sudo dpkg -i google-chrome-beta_current_amd64.deb
rm google-chrome-beta_current_amd64.deb

sudo rm /usr/bin/google-chrome
sudo ln -s /usr/bin/google-chrome-beta /usr/bin/google-chrome
