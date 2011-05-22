<!doctype html>
<html>
    <head>
        <title>猜电影</title>
        <link rel="stylesheet/less" type="text/css" href="/css/style.less?v={{ system_version }}">
        <script src="/js/less.min.js" type="text/javascript"></script>
        <script src="/js/jquery.min.js" type="text/javascript"></script>
        <script src="/js/main.js?v={{ system_version }}" type="text/javascript"></script>
    </head>

    <body>
        {% include 'header.tpl' %}
        <div id="main">
            <div class="inner clear">
                <div class="left">
                    {% if user.logged_in %}
                    <div class="box-grey" id="publish">
                        <div class="body">
                            <form action="/publish" method="post">
                                <p><textarea name="sentence" placeholder="来段NB的电影台词"></textarea></p>
                                <p><input name="answer" placeholder="电影名 (中文名或英文名)"  type="TEXT" /><input type="SUBMIT" class="btn disabled" value="让他们猜去吧" /></p>
                            </form>
                        </div>
                    </div>
                    <p class="seperator"></p>
                    {% endif %}

                    <div class="box-white" id="entity-list">
                        <div class="header">
							{% if user.logged_in %}
                            <span class="rand" style="padding-left:5px"> 我拼命读书为了将来，谁知道没有将来 </span>
							{% else %}
                            <span class="rand" style="padding-left:5px">登录后就可以添加台词让大家猜啦~~~</span>
							{% endif %}
                            <ul class="type">
                                <li><a class="latest" href="/">最新</a></li>
								<!--<li><a class="hot" href="#">热门</a></li>-->
                                <li><a class="top" href="/top">排行榜</a></li>
                            </ul>
                        </div>
                        <div class="body" style="padding:0 15px 10px">
                            {% if user.logged_in %}
                            <div class="segment clear hide" id="segment-tpl">
                                <div class="vote">
                                    <a class="upvote disabled"></a>
                                    <div class="mark">0</div>
                                    <a class="downvote disabled"></a>
                                </div>
                                <div class="rt">
                                    <p class="sentence">
                                    </p>
									<p class="clear"><a class="btn c-answer" href="#">看影名</a><span class="hide real-answer"></span> <a href="{{ user.link }}" class="author">{{ user.nickname }}</a></p>
                                </div>
                            </div>
                            {% endif %}

							{{ topic_list }}

                        </div>
                    </div>
                </div>

                <div class="right">
                    <div class="box-white">
                        <div class="header">关于iGuess</div>
                        <div class="body">
                            <p>某天与朋友出去聚餐，闲着没事，就想来猜电影，但是各种搜索，都没找到一个比较靠谱的地方，于是就做了这个小应用</p>
                            <p>看过不少电影，但很多都被埋藏在记忆深处，只有看到那熟悉的台词时，才会勾起那部电影的记忆，不知你是否也有同感</p>
                        </div>
                    </div>

                    <p class="seperator"></p>

					{{ top_user }}
                    <p class="seperator"></p>

                    <div class="box-white">
                        <div class="header">最新进展</div>
                        <div class="body">
                            <p>11/05/23 添加了台词的挑战记录</p>
                            <p>11/05/14 绑定新域名:www.iguess.me</p>
                            <p>11/05/13 添加了达人秀功能</p>
                            <p>11/05/12 可以猜电影了~~~</p>
                        </div>
                    </div>

                </div>
            </div>
        </div>

        {% include 'footer.tpl' %}

    </body>
