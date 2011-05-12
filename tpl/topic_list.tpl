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
        <p class="clear" style="padding-bottom:1px"><a class="btn c-answer" href="#">看影名</a>
        <span class="hide answer">{{ segment.answer }}</span>
        <a href="https://profiles.google.com/{{ segment.author.nickname }}" target="_blank" class="author">{{ segment.author.nickname }}</a></p>
    </div>
</div>
{% endfor %}

{% if list_length == 15 %}
<a class="page_btn" href="/?page={{ page }}">更多</a>
{% else %}
<p class="no-more">莫有了，要不您来贡献点？</p>
{% endif %}
