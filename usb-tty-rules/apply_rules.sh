sudo cp stickbot.rules /etc/udev/rules.d/
sudo udevadm control --reload-rules && sudo udevadm trigger
sudo cp -r .solo ~/