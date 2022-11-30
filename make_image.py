import random
import datetime
import zoneinfo

import svgwrite
import astral, astral.sun

def get_part_of_day(time, city):
    kwargs = {
        "date": time.date(),
        "tzinfo": city.timezone,
    }
    sun = astral.sun.sun(city.observer, **kwargs)
    midnight = astral.sun.midnight(city.observer, **kwargs)
    if sun['dawn'] <= time < sun['noon']:
        return "morning"
    elif sun["noon"] <= time < sun["sunset"]:
        return "afternoon"
    elif sun["sunset"] <= time < midnight:
        return "evening"
    else:
        return "night"

parts_of_day = ["morning", "afternoon", "evening", "night"]
square_colors = ["#fff59e", "#80ffcc", "#9cb29e", "#a10045"]
text_colors = ["#111", "#222", "#000", "#eee"]
background_colors = ["#eee", "#eee", "#eee", "#111"]
    
timezone = zoneinfo.ZoneInfo("America/Chicago")
now = datetime.datetime.now(timezone)

city = astral.LocationInfo(
    name='Chicago',
    region='USA',
    timezone=timezone,
    latitude=41.8781,
    longitude=-87.6298,
)

part_of_day = get_part_of_day(now, city)
color_index = parts_of_day.index(part_of_day)
square_color = square_colors[color_index]
text_color = text_colors[color_index]
background_color = background_colors[color_index]

message = f"It's {now:%A} {part_of_day} in Chicago"
n_characters = len(message)
text_height = 0.67

view_box = f"-1 0 {n_characters + 2} 2"
drawing = svgwrite.Drawing('image.svg', profile='full', viewBox=view_box)

drawing.add(drawing.rect(insert=(-1, 0), size=(n_characters + 2, 2), fill=background_color))

shape_group = drawing.add(drawing.g(fill=square_color, stroke=text_color, stroke_width=0.05, stroke_opacity=1))
for x, char in enumerate(message):
    if char.strip():
        shape_group.add(drawing.rect(insert=(x, 0.5), size=(1, 1), transform=f"rotate({x} {x + 0.5} {1})"))

text_group = drawing.add(drawing.g(font_size=text_height, font_family="sans-serif", text_anchor="middle", fill=text_color))
for x, char in enumerate(message):
    text_group.add(drawing.text(char.upper(), insert=(x + 0.5, 1), alignment_baseline="middle"))

outline_group = drawing.add(drawing.g(fill="none", stroke=text_color, stroke_width=0.05, stroke_opacity=1))
for x, char in enumerate(message):
    if char.strip():
        outline_group.add(drawing.rect(insert=(x, 0.5), size=(1, 1), transform=f"rotate({1 * x} {x + 0.5} {1})"))
    
drawing.saveas("image.svg", pretty=True)
