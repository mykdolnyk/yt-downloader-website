# Video Downloader and Viewer

A simple Django website that lets you watch and download videos from YouTube. It integrates such services as **Docker**, **Nginx**, **Celery**, **RabbitMQ**, **Memcached** and **MySQL** database. 

It utilizes **cron** jobs to clear old files and entries. 

You can also set up an SSL certificate for your website if you attach it to a domain name using **Certbot**.

### Contents

- [Features](#features)
- [Set Up](#set-up)
  - [Using PostgreSQL](#using-postgresql)
  - [Setting up the SSL](#setting-up-the-ssl)

## Features

- ▶️ **YouTube video downloading functionality**

- ⏳ **Real-time progress bars**:
  - A progress bar gets smoothly updated using the information retrieved from the module used to download video files.
- 💣 **Automated deletion of old video files**:
  - Implemented a custom Django `manage.py` command to clear up old files and entries. It is being triggered by a **shell** script that gets executed by cron.
- 📃 **File logging system**:
  - Logs from the website, Nginx, RabbitMQ are agregated in the `logs` folder of the project.
- 🔐 **SSL support**:
  - The project provides an ability to set up an SSL certificate for a website if it is connected to a domain name (using the [Let's Encrypt](https://letsencrypt.org/) certs). 
  

## Set Up 

First, you will need to clone the project in your working folder:

```bash
git clone https://github.com/mykdolnyk/yt-downloader-website.git
cd yt-downloader-website
```

Ensure that you have Docker and Docker Compose installed on your system. Then, head to the project folder so you can run the project:

```bash
docker compose up
```

By default, the project is using the preconfigured `test.env` file, but it is strongly encouraged to change it if you decide to deploy the project online.

> ℹ️ Note: If you encounter the `Sign in to confirm you’re not a bot` error when trying to download a video, then you should add your cookies to the `ytdlp_cookies.txt` file. You can retrieve them using the [official yt-dlp guide](https://github.com/yt-dlp/yt-dlp/wiki/Extractors#exporting-youtube-cookies).

---

### Using PostgreSQL

In case you decide to host your project using the DB in the container, but you find the MySQL DB too heavy on memory, you can use the `psql` branch instead. It is updated to match the state of the `main` branch, so there should be no issues using it.

To do so, clone the project this way:
```bash
git clone --branch psql https://github.com/mykdolnyk/yt-downloader-website.git
cd yt-downloader-website
``` 

Feel free to proceed with further steps afterward.

---

### Setting up the SSL
 
You can set up a free SSL certificate for your domain name using a Certbot. However, it requires a bit more manual setup. 

You should modify a few lines of code before starting the project. 

- [`nginx\default_ssl.conf`](nginx\default_ssl.conf)
  - [Line 17](nginx\default_ssl.conf#L17): replace %DOMAINNAME% with your domain name;
  - [Line 31](nginx\default_ssl.conf#L31): replace %DOMAINNAME% with your domain name;
- [`compose_ssl.yml`](compose_ssl.yml)
  - [Line 86](compose_ssl.yml#L86): replace %DOMAINNAME% with your domain name;
  - [Line 86](compose_ssl.yml#L86): replace %EMAIL% with your email address.
  
Once that is done, you can run the project using the following command:

```bash
docker compose -f compose_ssl.yml up
```
