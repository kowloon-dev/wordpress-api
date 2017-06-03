# wordpress-api
WordpressのREST API v2を利用して記事の投稿・更新を行うPythonスクリプト。

Python Scripts posting/updating your article with WordPress REST API v2.

## Description

`wordpress-api` is the tool that handles post/update action to your own WordPress site with CLI-based operation.

## Features

- POST article to your WordPress website with REST API over HTTPS.
- Automatically handle whether "New post" or "Update post".
- If the case "New post", this script will ask you to choose categories regarding the article.

## Requirement

### Web site side
- WordPress with REST API v2
- HTTPS capability (TCP:443 is opened)

  Because this scripts carries authentication information in HTTP request headers(BASIC Auth code), so securing with HTTPS is strongly recommended.
- [Application Passwords](https://wordpress.org/plugins/application-passwords/) plugin
- [JP Markdown](https://wordpress.org/plugins/jetpack-markdown/) plugin

## Client side

- Python3 or more

  As long as python3.x is available, Windows/Mac/Linux will be fine.
- [requests library](http://docs.python-requests.org/en/master/)

- Your articles for WordPress

***IMPORTANT***

This script expects that your local articles are written in `Markdown`.

## Usage

1. To post your article:

```
post.py (status_option) yourfilename.md
```

status_option:
- -p: "published" status
- -d: "draft" status

Status option is NOT mandatory, you can handle "default status" in `wp-api.ini` file.
If you don't designate status option in CLI, scripts obey "default status".

If this is the 1st time you post this article, you'll be asked which category do you correlate with.

Example:

```
kowloon$ post.py -p "How to use this script.md"

Please select category id.
2 : MarkDown
3 : WordPress
1 : 未分類
>>> 2,3

POST action has succeeded.
id : 119
title : How to use this script
link : https://blog.kowloonet.org/archives/119

```

After POST process has finished, this script adds `management information`(assigned post_id, date, publishedURL) to the 1st line of your local article file which is used for next time.


2. To update your articles:

```
kowloon$ post.py -p "How to use this script.md"
```

This script always reads the 1st line of your local article file and search "article_id" json code section.
If "article_id" has found, this script handles your article as "Update" action.

In the case "Update", the script will not ask you category id again.


## Installation

1. Clone repository

```
$ git clone git@github.com:kowloon-dev/wordpress-api.git
```

1. Copy .ini and log file to your home directory.

```
$ copy wordpress-api/files/wp-api.* ~/
```

1. Add a path `wordpress-api.git/post.py` to your $PATH.

```
$ echo "export PATH=$PATH:/Users/kowloon/wordpress-api" >> ~/.bash_profile
$ source ~/.bash_profile
```

1. Install [JP Markdown ](https://wordpress.org/plugins/jetpack-markdown/) plugin on your WordPress site.

1. Install [Application Passwords](https://wordpress.org/plugins/application-passwords/) plugin on your WordPress site.

1. Make application password regarding your username on WordPress site.

1. Base64 Encode your name and application password.

1. Define your Base64-based Authorization code and base URL in wp-api.ini file.


## Author

[@_kowloon](https://twitter.com/_kowloon)
