{% for segment in list %}
<div class="segment clear" id="{{ segment.key }}">
    <div class="rt">
        <p class="sentence">
        {{ segment.sentence }}
        </p>
        <p class="clear" style="padding-bottom:1px"><a class="btn c-answer" href="#">看影名</a>
        <span class="hide answer">{{ segment.answer }}</span>
    </div>
</div>
{% endfor %}

{% if list_length == 15 %}
<a class="page_btn" href="/?page={{ page }}">更多</a>
{% else %}
<p class="no-more">莫有了~~~</p>
{% endif %}

