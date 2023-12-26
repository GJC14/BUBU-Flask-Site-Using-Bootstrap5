# This is a Flask website hosting on GCP, designed with Bootstrap.

# Hosting a Flask Web on GCP for Free
This is a working Official Website running on GCP with Ubuntu. Flask, Gunicorn, NGINX, Let's Encrypt SSL used in backend. Frontend using Bootstrap, Javascript, CSS and HTML.
# Go through
<img width="3180" alt="How Internet Route to Your Web" src="https://github.com/GJC14/BUBU-Flask-Site-Using-Bootstrap5/assets/136115556/aa135905-6460-4688-8148-b296af7dee84">  

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
<img width="1122" alt="截圖 2023-11-26 下午5 08 04" src="https://github.com/GJC14/BUBU-Flask-Site-Using-Bootstrap5/assets/136115556/e348c04c-1a34-47f5-87f3-1b15793b9a31">  
<img width="1123" alt="截圖 2023-11-26 下午5 07 24" src="https://github.com/GJC14/BUBU-Flask-Site-Using-Bootstrap5/assets/136115556/46c6b554-0f19-4d58-a1fd-4962df5880d5">  

# 2. SSH into your instance
At your ~$ (which default to be your google account name) you could put your files here. I had put my flask here.
<img width="331" alt="285642387-1cd3bd08-f383-4fa1-8412-16280ef3e118" src="https://github.com/GJC14/BUBU-Flask-Site-Using-Bootstrap5/assets/136115556/9e003a66-e183-4430-89f0-ed3177b2e659">  

# 3. Setup your Flask
In order to use pip  
```sudo apt update```
```sudo apt install python3-pip```
<img width="979" alt="截圖 2023-11-26 下午5 47 33" src="https://github.com/GJC14/BUBU-Flask-Site-Using-Bootstrap5/assets/136115556/3d1eddcd-7df3-4bbc-ae4f-913bfdedd075">  
<img width="1453" alt="截圖 2023-11-26 下午5 48 05" src="https://github.com/GJC14/BUBU-Flask-Site-Using-Bootstrap5/assets/136115556/6ff93edd-ee6e-4dc8-a779-33215a88469e">  

```sudo pip3 install Flask```  
<img width="301" alt="截圖 2023-11-26 下午5 52 05" src="https://github.com/GJC14/BUBU-Flask-Site-Using-Bootstrap5/assets/136115556/aa898fea-bbee-40b5-b63f-8ea8d3dccda2">  

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
<img width="895" alt="截圖 2023-11-26 下午6 16 21" src="https://github.com/GJC14/BUBU-Flask-Site-Using-Bootstrap5/assets/136115556/cf82cedb-2273-4636-b40d-28bfa086b6ad">  

## 4.2 Open Ubuntu FireWall to allow Nginx control  
```
sudo ufw status
sudo ufw app list
sudo ufw allow OpenSSH
sudo ufw allow 'Nginx Full'
```
<img width="633" alt="截圖 2023-11-26 下午6 21 45" src="https://github.com/GJC14/BUBU-Flask-Site-Using-Bootstrap5/assets/136115556/043a716d-f12d-4333-8496-d7856863926c">  
  
To check if NGINX is active. Also, you can now enter your ip to directly get NGINX welcome page  
```systemctl status nginx```  
<img width="774" alt="截圖 2023-11-26 下午6 27 31" src="https://github.com/GJC14/Flask_Web_GCP/assets/136115556/33090ac6-3617-4639-9025-4cbf998263ac">

## 4.3 Configure NGINX
The site file is stored in "sites-available", we are going to creat a file for my web and link it to "sites-enabled", thus Let's Encrypt could get our domain informations.  
<img width="945" alt="截圖 2023-11-26 下午6 30 36" src="https://github.com/GJC14/BUBU-Flask-Site-Using-Bootstrap5/assets/136115556/ffabd655-9e64-48a4-9d27-f04d2031acb2">  
  
**Remember to point your domain DNS to your server in advance.**  
Listen to port 80 (Default port) ; Server_name is your domain ; Later we will use Let's Encrypt to set the NGINX ports.
```
server {
        listen 80;
        server_name test.com;
}
```
<img width="948" alt="截圖 2023-11-26 下午6 58 00" src="https://github.com/GJC14/BUBU-Flask-Site-Using-Bootstrap5/assets/136115556/850b51c9-565a-4458-8e6b-47cb9aafe0e0">  

## 4.4 Link your configuration from available to enabled.  
```sudo ln -s /etc/nginx/sites-available/my_test_website.com /etc/nginx/sites-enabled/```  
You could see all the links with  
```ls -l /etc/nginx/sites-enabled/```
Remove the failed link with  
```sudo rm /etc/nginx/sites-enabled/which_failed```  

---
## 4.5 Restart NGINX, and you should be able to enter your web with your domain.  
```sudo systemctl restart nginx```
<img width="788" alt="截圖 2023-11-26 下午7 17 04" src="https://github.com/GJC14/BUBU-Flask-Site-Using-Bootstrap5/assets/136115556/29d845ec-6378-4167-a73d-23422b3ab61e">  

# 5. Let's Encrypt w/ certbot
https://certbot.eff.org/instructions?ws=nginx&os=ubuntufocal  
Follow the instruction from official website, in my case, I'm using NGINX with Ubuntu.  
## 5.1 Install certbot with snap  
```sudo snap install --classic certbot```  
## 5.2 Prepare command  
```sudo ln -s /snap/bin/certbot /usr/bin/certbot```  
## 5.3 Get certificate  
```sudo certbot --nginx```  
<img width="832" alt="截圖 2023-11-26 下午7 26 45" src="https://github.com/GJC14/BUBU-Flask-Site-Using-Bootstrap5/assets/136115556/8d6e6f3a-d9ac-4976-a495-4d0f12fefde7">  

We could see that the previous my_test_website.com has been revised by certbot, with new lines with # in the end. It first redirect 80 port to 443 port, or return 404 for 80  
<img width="723" alt="截圖 2023-11-26 下午7 37 43" src="https://github.com/GJC14/BUBU-Flask-Site-Using-Bootstrap5/assets/136115556/41dfda42-5da7-49ce-a225-bf0b17f0dd3c">

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

## 6.2 Install Gunicorn and test running on port 5050
Install Gunicorn  
```sudo pip3 install gunicorn```  
Route to where your app.py locate  
```cd ~/```  
Run Gunicorn with 3 workers binding port 5050  
```gunicorn --workers 3 --bind 127.0.0.1:5050 app:app```  
<img width="683" alt="截圖 2023-11-26 下午8 57 03" src="https://github.com/GJC14/BUBU-Flask-Site-Using-Bootstrap5/assets/136115556/83b12840-bdc5-4470-809b-b030bec24ea4">


# 7. Pack all of your server to systemd
Lastly, you probably wouldn't like to start gunicorn everytime, and prefer run it in the background, thus last step is to pack the gunicorn to systemd.   
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
<img width="1470" alt="截圖 2023-11-26 下午9 05 01" src="https://github.com/GJC14/BUBU-Flask-Site-Using-Bootstrap5/assets/136115556/805b1953-c1f3-4548-b890-52dc581daa3c">  

# Conclusion, start your flask using systemctl
```sudo systemctl start my_web.service``` To start  
```sudo systemctl restart my_web.service``` To restart  
```sudo systemctl status my_web.service``` To see status  
```sudo systemctl enable my_web.service``` To make it auto run after start the server  
If you edit the .service file, you should always ```sudo systemctl daemon-reload```  
<img width="997" alt="截圖 2023-11-26 下午9 14 17" src="https://github.com/GJC14/BUBU-Flask-Site-Using-Bootstrap5/assets/136115556/346300cc-9812-4a63-8641-98916caca0a4">  

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

## e.1 Open SSH Configuration, which locate in /Users/username/.ssh/config   

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
![截圖 2023-11-26 下午9 35 30](https://github.com/GJC14/BUBU-Flask-Site-Using-Bootstrap5/assets/136115556/5df26235-21fd-45a6-9bfb-170e875aff8a)  
Get the public key  
```cat keyname.pub```  
Remember to put your key to where IdentityFile points to.  

## e.4 Put it on GCP
In your Compute Engine>Edit>Add your public key  

## e.5 There you go
In VSCode using >Remote-SSH Connect to Host  
Here you could open a folder just like on your own laptop.  

You could refer to this video, such a clear video.
https://www.youtube.com/watch?v=0Bjx3Ra8PRM
