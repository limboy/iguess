<div class="box-white">
    <div class="header">达人秀</div>
    <div class="body" style="padding-bottom:0">
        <ul class="topuser clear">
        {% for item in topuser %}
        <li><a title="{{ item.name }}, 共答对了{{ item.count }}道题" href="https://profiles.google.com/{{item.name}}"><img src="{{ item.gravatar }}" /></a></li>
        {% endfor %}
        </ul>
    </div>
</div>
