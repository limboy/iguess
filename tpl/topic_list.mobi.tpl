{% for segment in list %}
<div class="segment clear" id="{{ segment.key }}">
    <div class="rt">
        <p class="sentence">
        {{ segment.sentence }}
        </p>
        <div class="clear">
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
        </div>
    </div>
</div>
{% endfor %}

{% if list_length == 15 %}
<a class="page_btn" href="/?page={{ page }}">更多</a>
{% else %}
<p class="no-more">莫有了~~~</p>
{% endif %}

