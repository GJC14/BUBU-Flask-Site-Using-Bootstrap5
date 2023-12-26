# BUBU_Website
This is a Flask website hosting on GCP, designed with Bootstrap.

# Hosting a Flask Web on GCP for Free
This is a working Official Website running on GCP with Ubuntu. Flask, Gunicorn, NGINX, Let's Encrypt SSL used in backend. Frontend using Bootstrap, Javascript, CSS and HTML.
# Go through
<img width="3180" alt="How Internet Route to Your Web" src="https://github.com/GJC14/Flask_Web_GCP/assets/136115556/87c2f576-1241-4b60-b8fe-8f487dd1b49f">

# 1. GCP Free Tier
https://cloud.google.com/free/docs/free-cloud-features?hl=zh-tw
As of 2023/11/26, GCP offers monthly free Compute Engine e2-micro Instance in three US zone, with 30GB Standard disk, and free public IP which will renew after restart your instance.  
> 每個月可以在下列其中一個美國區域中使用 1 個非先佔 e2-micro VM 執行個體：  
> - 奧勒岡州：us-west1  
> - 愛荷華州：us-central1  
> - 南卡羅來納州：us-east1
> 
> 每月 30 GB 的標準永久磁碟  
> 在以下地區每個月可使用 5 GB 的快照儲存空間：  
> - 奧勒岡州：us-west1  
> - 愛荷華州：us-central1  
> - 南卡羅來納州：us-east1  
> - 台灣：asia-east1  
> - 比利時：europe-west1
> 
> 每月 1 GB 從北美輸出至所有地區的網路流量 (中國和澳洲除外)  
> 在免費方案中，e2-micro 執行個體的限制依據為時間，而非執行個體。每月使用所有符合資格的 e2-micro 執行個體均為免費，直到使用時數達到當月限定的總時數為止。計算用量時會加總所有支援地區的用量。  
> Compute Engine 免費方案不會針對外部 IP 位址收費。  
> GPU 和 TPU 不包含在免費方案優惠中。如果您在 VM 執行個體中新增 GPU 和 TPU，則一律須付費。

I put my Ubuntu in us-west1-c, using e2-micro + 30GB standard(Please remember to change your storage type). You could also install WordPress directly from Marketplace, remember to set the spec to cater to free tier.  
You should enable HTTP and HTTPS lest Let's Encrypt couldn't connect to your isntance.
<img width="1122" alt="截圖 2023-11-26 下午5 08 04" src="https://github.com/GJC14/Flask_Web_GCP/assets/136115556/d7576a9f-f017-483b-902e-8ca4141c8664">
<img width="1123" alt="截圖 2023-11-26 下午5 07 24" src="https://github.com/GJC14/Flask_Web_GCP/assets/136115556/6c0112ef-2f7b-4d81-b6fe-bf4442fb4bf2">

# 2. SSH into your instance
At your ~$ (which default to be your google account name) you could put your files here. I had put my flask here.
<img width="331" alt="285642387-1cd3bd08-f383-4fa1-8412-16280ef3e118" src="https://github.com/GJC14/Flask_Web_GCP/assets/136115556/af39c018-9dc4-4c12-9e04-90ffe077df79">

# 3. Setup your Flask
In order to use pip  
```sudo apt update```
```sudo apt install python3-pip```
<img width="979" alt="截圖 2023-11-26 下午5 47 33" src="https://github.com/GJC14/Flask_Web_GCP/assets/136115556/357a65a4-dc32-4970-b170-605c240343a8">
<img width="1453" alt="截圖 2023-11-26 下午5 48 05" src="https://github.com/GJC14/Flask_Web_GCP/assets/136115556/7386f91d-582d-4e6f-aa70-4d63267f9b87">  

```sudo pip3 install Flask```  
<img width="301" alt="截圖 2023-11-26 下午5 52 05" src="https://github.com/GJC14/Flask_Web_GCP/assets/136115556/f851668f-9eb7-4319-ba89-21b520a8c42b">

Add file in ~$
```python
# app.py
from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
```
```$ sudo python3 app.py```  
Now you could see your flask web hosting on your_ip:80. For server safety press ctrl+c to end and rewrite app.run to app.run() to prevent external links.  
We are going to use NGINX to reverse proxy.

# 4. NGINX opening port 80/443
## 4.1 Install NGINX  
```sudo apt update && sudo apt install nginx```  
<img width="895" alt="截圖 2023-11-26 下午6 16 21" src="https://github.com/GJC14/Flask_Web_GCP/assets/136115556/99fe3dcf-6dba-4640-b030-47140478921d">  

## 4.2 Open Ubuntu FireWall to allow Nginx control  
```
sudo ufw status
sudo ufw app list
sudo ufw allow OpenSSH
sudo ufw allow 'Nginx Full'
```
<img width="633" alt="截圖 2023-11-26 下午6 21 45" src="https://github.com/GJC14/Flask_Web_GCP/assets/136115556/baf3a5eb-688c-4669-a3f6-323705e9ed1b">  
  
To check if NGINX is active. Also, you can now enter your ip to directly get NGINX welcome page  
```systemctl status nginx```  
<img width="774" alt="截圖 2023-11-26 下午6 27 31" src="https://github.com/GJC14/Flask_Web_GCP/assets/136115556/33090ac6-3617-4639-9025-4cbf998263ac">

## 4.3 Configure NGINX
The site file is stored in "sites-available", we are going to creat a file for my web and link it to "sites-enabled", thus Let's Encrypt could get our domain informations.  
<img width="945" alt="截圖 2023-11-26 下午6 30 36" src="https://github.com/GJC14/Flask_Web_GCP/assets/136115556/ee042b6f-a1ac-4af4-a5f0-1580863228a9">  
  
**Remember to point your domain DNS to your server in advance.**  
Listen to port 80 (Default port) ; Server_name is your domain ; Later we will use Let's Encrypt to set the NGINX ports.
```
server {
        listen 80;
        server_name test.com;
}
```
<img width="1470" alt="截圖 2023-11-26 下午6 54 54" src="https://github.com/GJC14/Flask_Web_GCP/assets/136115556/6f4e5522-4433-49b2-aef7-8590112ababa">  
<img width="948" alt="截圖 2023-11-26 下午6 58 00" src="https://github.com/GJC14/Flask_Web_GCP/assets/136115556/44cb67b2-3278-431c-8ec2-3e75a5ebca7f">

## 4.4 Link your configuration from available to enabled.  
```sudo ln -s /etc/nginx/sites-available/my_test_website.com /etc/nginx/sites-enabled/```  
You could see all the links with  
```ls -l /etc/nginx/sites-enabled/```
Remove the failed link with  
```sudo rm /etc/nginx/sites-enabled/which_failed```  

---
## 4.5 Restart NGINX, and you should be able to enter your web with your domain.  
```sudo systemctl restart nginx```
<img width="788" alt="截圖 2023-11-26 下午7 17 04" src="https://github.com/GJC14/Flask_Web_GCP/assets/136115556/ecaea5d1-8c5f-421a-ae32-61bb781add54">

# 5. Let's Encrypt w/ certbot
https://certbot.eff.org/instructions?ws=nginx&os=ubuntufocal  
Follow the instruction from official website, in my case, I'm using NGINX with Ubuntu.  
## 5.1 Install certbot with snap  
```sudo snap install --classic certbot```  
## 5.2 Prepare command  
```sudo ln -s /snap/bin/certbot /usr/bin/certbot```  
## 5.3 Get certificate  
```sudo certbot --nginx```  
<img width="832" alt="截圖 2023-11-26 下午7 26 45" src="https://github.com/GJC14/Flask_Web_GCP/assets/136115556/5efe7e99-5fc3-432a-9d46-0e0807df9b0a">

We could see that the previous my_test_website.com has been revised by certbot, with new lines with # in the end. It first redirect 80 port to 443 port, or return 404 for 80  
<img width="1470" alt="截圖 2023-11-26 下午7 32 24" src="https://github.com/GJC14/Flask_Web_GCP/assets/136115556/42b403ba-1709-4b8c-be4b-d54cf5b73739">
<img width="723" alt="截圖 2023-11-26 下午7 37 43" src="https://github.com/GJC14/Flask_Web_GCP/assets/136115556/3a9247f4-dc11-4a75-ba0b-42f46ef5d211">

# 6. Using Gunicorn to run flask
## 6.1 Adding NGINX reverse proxy
Add location in 443 of my_test_website.com, which return to http://localhost:5050. You could change 5050 to which you would like to run Gunicorn.  
```
    location / {
        proxy_pass http://localhost:5050;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        add_header Content-Security-Policy "frame-ancestors 'none';";
        add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    }
```
```sudo systemctl restart nginx```
<img width="1468" alt="截圖 2023-11-26 下午8 08 06" src="https://github.com/GJC14/Flask_Web_GCP/assets/136115556/48011bce-4270-44ef-bae6-0b2827839424">

## 6.2 Install Gunicorn and test running on port 5050
Install Gunicorn  
```sudo pip3 install gunicorn```  
Route to where your app.py locate  
```cd ~/```  
Run Gunicorn with 3 workers binding port 5050  
```gunicorn --workers 3 --bind 127.0.0.1:5050 app:app```  
<img width="683" alt="截圖 2023-11-26 下午8 57 03" src="https://github.com/GJC14/Flask_Web_GCP/assets/136115556/7ffabea7-28a4-4258-aeab-aa2f67d10851">
<img width="1470" alt="test_success" src="https://github.com/GJC14/Flask_Web_GCP/assets/136115556/f4a7d2b5-f4c8-4352-a472-07b025285939">


# 7. Pack all of your server to systemd
Lastly, you probably wouldn't like to start gunicorn everytime, and prefer run it in the background, thus last step is to pack the gunicorn to systemd.  
<img width="1395" alt="截圖 2023-11-26 下午9 01 44" src="https://github.com/GJC14/Flask_Web_GCP/assets/136115556/93347601-b7b5-4de9-a9f1-df50d47e809d">  
```sudo vim /etc/systemd/system/my_web.service```  
Type in your username(default default to be your google account name, and should be same as your ~$ foldername).  
```
[UNIT]
Description=Gunicorn running my website
After=network.target

[Service]
User=user
Group=www-data
WorkingDirectory=/home/user
Environment="PATH=/usr/bin/python3"
ExecStart=/usr/local/bin/gunicorn --workers 3 --bind 127.0.0.1:5050 app:app

[Install]
WantedBy=multi-user.target
```
<img width="1470" alt="截圖 2023-11-26 下午9 05 01" src="https://github.com/GJC14/Flask_Web_GCP/assets/136115556/64c97470-d810-485f-aed1-0ad39c481fef">  

# Conclusion, start your flask using systemctl
```sudo systemctl start my_web.service``` To start  
```sudo systemctl restart my_web.service``` To restart  
```sudo systemctl status my_web.service``` To see status  
```sudo systemctl enable my_web.service``` To make it auto run after start the server  
If you edit the .service file, you should always ```sudo systemctl daemon-reload```  
<img width="997" alt="截圖 2023-11-26 下午9 14 17" src="https://github.com/GJC14/Flask_Web_GCP/assets/136115556/87f234c2-0c07-4348-a110-6b079f3bf55d">

## Increasing your security with block directly entering from ip
**If you would like to remove default Welcome to NGINX page. This will also disable entering directly from ip, increasing safety of the website**
1. Annotation the settings in default under "sites-available"
2. Edit your site's configuration
```
server {
    if ($host = gabrielexp.site) {
        return 301 https://$host$request_uri;
    } # managed by Certbot

    listen 80 default_server;
    listen [::]:80 default_server;
    server_name gabrielexp.site;
    return 301 https://gabrielexp.site$request_uri;
    #return 404; # managed by Certbot
}
```
3. Then reload nginx
```
sudo nginx -t
sudo systemctl reload nginx
```

# (extra) . SSH througn VSCode
You could use Remote SSH on VSCode  
<img width="1022" alt="截圖 2023-11-26 下午9 20 56" src="https://github.com/GJC14/Flask_Web_GCP/assets/136115556/41648efc-a5bd-4184-ac80-e161064be803">  

## e.1 Open SSH Configuration, which locate in /Users/username/.ssh/config  
<img width="1021" alt="截圖 2023-11-26 下午9 21 29" src="https://github.com/GJC14/Flask_Web_GCP/assets/136115556/23077332-5ef2-49c2-9144-fabfdd16dde0">  

## e.2 Configure SSH
With  
1. Host enter the name you want to call it in VSCode  
2. Host name at your GCP public IP
3. User as your username in server (default to your Google account name)
4. IdentityFile as where you store your SSH keys  
```
Host SSH_to_test_GCP
    HostName YOUR_HOST_IP
    User YOUR_USERNAME_IN_SERVER
    IdentityFile /Users/username/Documents/ssh_keys/keyname
```

## e.3 Make a key  
```ssh-keygen -t rsa -f remote-ssh-demo -C YOUR_USERNAME_IN_SERVER -b 2048```  
<img width="1021" alt="截圖 2023-11-26 下午9 35 30" src="https://github.com/GJC14/Flask_Web_GCP/assets/136115556/6b4b9ec3-a4fa-4596-b24d-516c3364311f">  
Get the public key  
```cat keyname.pub```  
Remember to put your key to where IdentityFile points to.  

## e.4 Put it on GCP
In your Compute Engine>Edit>Add your public key  
<img width="649" alt="截圖 2023-11-26 下午9 44 22" src="https://github.com/GJC14/Flask_Web_GCP/assets/136115556/ca4f0d36-c368-4dd8-880f-268ac9fc3bb2">

## e.5 There you go
In VSCode using >Remote-SSH Connect to Host  
Here you could open a folder just like on your own laptop.  
<img width="1023" alt="截圖 2023-11-26 下午9 50 09" src="https://github.com/GJC14/Flask_Web_GCP/assets/136115556/5a0de6fd-98db-4a30-9e85-d0b2053b3888">

You could refer to this video, such a clear video.
https://www.youtube.com/watch?v=0Bjx3Ra8PRM
