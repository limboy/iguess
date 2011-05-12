{% for segment in list %}
<div class="segment clear" id="{{ segment.key }}">
    <div class="vote">
        {% if segment.can_vote %}
        <a class="upvote" href="#"></a>
        {% else %}
        <a class="upvote disabled" title="您尚未登陆或已投过票" href="#"></a>
        {% endif %}
        <div class="mark">{{ segment.votedown|default:0|add:segment.voteup|default:0 }}</div>
        {% if segment.can_vote %}
        <a class="downvote" href="#"></a>
        {% else %}
        <a class="downvote disabled" title="您尚未登陆或已投过票" href="#"></a>
        {% endif %}
    </div>
    <div class="rt">
        <p class="sentence">
        {{ segment.sentence }}
        </p>
        <div class="clear" style="padding-bottom:1px">
            {% if segment.has_answered %}
            <a class="btn c-answer" href="#">看影名</a>
            <span class="hide real-answer">{{ segment.answer }}</span>
            {% else %}
            <span class="answer">
                <form action="/guess" method="post">
                <input name="id" value="{{ segment.key.id }}" type="hidden" />
                <input type="text" name="answer" placeholder="输入电影名，回车" />
                </form>
                <span class="success"></span>
                <span class="fail"></span>
            </span>
            {% endif %}
            <a href="https://profiles.google.com/{{ segment.author.nickname }}" target="_blank" class="author">{{ segment.author.nickname }}</a>
        </div>
    </div>
</div>
{% endfor %}

{% if list_length == 15 %}
<a class="page_btn" href="/?page={{ page }}">更多</a>
{% else %}
<p class="no-more">莫有了，要不您来贡献点？</p>
{% endif %}
