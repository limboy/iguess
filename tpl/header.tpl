<div id="header">
    <div class="inner">
        <div id="logo"><a href="/">iGuess</a></div>
        <ul>
            {% if not user.logged_in %}
            <li><a href="{{ user.login_url }}">使用Google帐号登录</a></li>
            {% else %}
            <li>{{ user.nickname }}</li>
            <li><a href="{{ user.logout_url }}">登出</a></li>
            {% endif %}
        </ul>
    </div>
</div>


