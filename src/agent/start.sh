#!/bin/bash
curl -fsSL https://raw.githubusercontent.com/thin-edge/thin-edge.io/main/get-thin-edge_io.sh | sudo sh -s

read -p 'URL of the tenant:' url
read -p 'Cumulocity username:' username
read -p 'Device Name:' deviceid
sudo tedge config set c8y.url $url
sudo tedge cert create --device-id $deviceid
sudo tedge cert upload c8y --user $username
sudo tedge connect c8y

dir=$(pwd)
sudo echo "[Unit]
Description=Device Agent-tedge
After=multi-user.target

StartLimitIntervalSec=60
StartLimitBurst=10

[Service]
Restart=on-failure
RestartSec=5
Type=idle
ExecStart=/usr/bin/python3 $dir/agent.py
WorkingDirectory=$dir
User=pi
[Install]
WantedBy=multi-user.target" > /lib/systemd/system/ifdeviceagent.service

sudo echo "[Unit]
Description=Device Connector
After=multi-user.target
StartLimitIntervalSec=60
StartLimitBurst=10

[Service]
Restart=on-failure
RestartSec=5
Type=idle
ExecStart=/usr/bin/python3 $dir/device.py
WorkingDirectory=$dir
User=pi
[Install]
WantedBy=multi-user.target" > /lib/systemd/system/ifdeviceconnector.service
sudo chmod 644 /lib/systemd/system/ifdeviceagent.service
sudo chmod 644 /lib/systemd/system/ifdeviceconnector.service
sudo systemctl daemon-reload
sudo systemctl enable --now ifdeviceconnector.service
sudo systemctl enable --now ifdeviceagent.service
