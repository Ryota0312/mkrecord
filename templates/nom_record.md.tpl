記録書 No.{{Number}}
* 種別 :: 記録書
* 期間 :: {{Start}} - {{End}}
* 所属 :: {{Belongs}}
* 氏名 :: {{Name}}
* 日付 :: {{Date}}

# 実績，詳細，および反省・感想
## 研究関連
{{PrevCopy.Research}}

## 研究室関連
{% if not Calendars.Univ.events.prev -%}
特になし
{% else -%} 
{% for event in Calendars.Labo.events.prev -%}
{{ event.fmt("+ (%START) %SUMMARY", "%-m/%-d") }}
{% endfor -%}
{% endif %}

## 大学院関連
{% if not Calendars.Univ.events.prev -%}
特になし
{% else -%} 
{% for event in Calendars.Univ.events.prev -%}
{{ event.fmt("+ (%START) %SUMMARY", "%-m/%-d") }}
{% endfor -%}
{% endif %}

# 今後の予定
## 研究室関連
{% if not Calendars.Labo.events.next -%}
特になし
{% else -%} 
{% for event in Calendars.Labo.events.next -%}
{{ event.fmt("+ (%START) %SUMMARY", "%-m/%-d") }}
{% endfor -%}
{% endif %}

## 大学院関連
{% if not Calendars.Labo.events.next -%}
特になし
{% else -%} 
{% for event in Calendars.Univ.events.next -%}
{{ event.fmt("+ (%START) %SUMMARY", "%-m/%-d") }}
{% endfor -%}
{% endif %}

# NOTE

# 近況報告
