<!DOCTYPE html>
<html lang="zh-CN">
<head>
	<meta charset="UTF-8" />
	<meta content="True" name="HandheldFriendly" />
	<meta name="viewport" content="maximum-scale=1.0,width=device-width,initial-scale=1.0" />
	<title>猜电影</title>
    <link rel="stylesheet" type="text/css" media="screen"  href="/css/style.mobi.css?v={{ system_version }}" />
	<link rel="shortcut icon" href="/favicon.ico" />
    <script src="/js/jquery.min.js" type="text/javascript"></script>
	<meta name="apple-mobile-web-app-capable" content="yes" />
    <script src="/js/main.js?v={{ system_version }}"></script>
</head>

<body>
    {% include 'header.mobi.tpl' %}
    <div id="entity-list">
    {{ topic_list }}
    </div>
</body>
