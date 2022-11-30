import svgwrite
import datetime

dwg = svgwrite.Drawing('image.svg', profile='tiny', width="200", height="100")
dwg.add(dwg.line((0, 0), (20, 50), stroke=svgwrite.rgb(10, 10, 16, '%')))
dwg.add(dwg.text(str(datetime.datetime.now()), insert=(20, 50), fill='red'))
dwg.save()
