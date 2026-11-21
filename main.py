"""20 November 2026: deterministic editorial composition and offline delivery.

Build-time only: --build writes the original vector artwork as SVG and HTML.
The sandbox's default path uses Python's standard library and the final PNG.
No network, fonts, subprocesses, third-party imports or browser on that path.
"""
from html import escape
from pathlib import Path
import argparse
import os
import struct
import zlib

ROOT = Path(__file__).resolve().parent
PAPER = '#F4EFE6'
INK = '#192B30'
RED = '#AA392D'
TEAL = '#236568'
GOLD = '#D6A54E'


def rect(x, y, w, h, fill, radius=0, stroke='none'):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" fill="{fill}" stroke="{stroke}"/>'


def path(d, fill, stroke='none', width=1.0):
    return f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{width}" stroke-linejoin="round" stroke-linecap="round"/>'


def circle(x, y, radius, fill, stroke='none', width=1):
    return f'<circle cx="{x}" cy="{y}" r="{radius}" fill="{fill}" stroke="{stroke}" stroke-width="{width}"/>'


def text(x, y, words, size=20, color=INK, weight=400, family='sans-serif', anchor='start'):
    return f'<text x="{x}" y="{y}" font-family="{family}" font-size="{size}" font-weight="{weight}" fill="{color}" text-anchor="{anchor}">{escape(words)}</text>'


def lines(x, y, words, size, leading=None, color=INK, family='sans-serif', weight=700):
    return ''.join(text(x, y+i*(leading or size*1.08), line, size, color, weight, family) for i, line in enumerate(words))


def globe(x, y, r):
    out = circle(x, y, r, '#90BDC1', INK, 2)
    out += path(f'M{x-r*.9} {y-r*.25} Q{x} {y-r*.7} {x+r*.9} {y-r*.25} M{x-r*.9} {y+r*.25} Q{x} {y+r*.7} {x+r*.9} {y+r*.25}', 'none', '#4A8386', 1)
    out += f'<ellipse cx="{x}" cy="{y}" rx="{r*.45}" ry="{r}" fill="none" stroke="#4A8386"/>'
    out += path(f'M{x-r*.7} {y-r*.52} l{r*.45} {-r*.15} {r*.25} {r*.3} {-r*.14} {r*.3} {-r*.3} {r*.08} {-r*.16} {-r*.22} Z', '#386D57')
    out += path(f'M{x-r*.13} {y+r*.04} l{r*.46} {-r*.12} {r*.18} {r*.35} {-r*.23} {r*.5} {-r*.2} {-r*.16} Z', '#386D57')
    return out


def skyline():
    out = ''
    for x, h in [(0,48),(25,70),(55,44),(84,84),(116,50),(145,68),(177,42),(205,77),(237,56),(269,40)]:
        out += rect(x, 141-h, 24, h, '#43636B')
        for wy in range(148-h, 134, 12):
            out += rect(x+5, wy, 4, 5, '#DCC285') + rect(x+15, wy, 4, 5, '#DCC285')
    return out


def poland_scene():
    out = rect(0,0,300,156,'#B8CFD0')
    out += circle(252,29,19,'#EBD7A5')
    out += path('M0 89 Q65 50 125 86 T300 65 V156 H0Z', '#8FADAD')
    out += skyline()
    out += rect(0,141,300,15,'#274B55')
    out += path('M145 156 L199 121 L216 156Z','#627C7E')
    out += path('M-10 29 Q80 17 180 65','none','#F6ECD5',6)
    out += path('M170 61 l25 3 -14 6 -7 -2 -10 5 2 -9Z',INK)
    out += path('M221 120 l-8 -23 14 7 6 -27 10 23 13 -5 -5 27Z','#C45A3F')
    out += path('M226 121 l6 -22 10 24Z','#E8AE50')
    out += rect(22,90,3,57,INK)
    out += rect(25,90,45,13,'#FFF9ED') + rect(25,103,45,13,'#B63C36')
    out += rect(251,81,3,65,INK)
    out += rect(254,81,37,11,'#4478AA') + rect(254,92,37,11,'#DDB949')
    out += path('M58 143 l15 -15 19 4 11 11Z','#D4C9AD',INK,1.5)
    out += circle(72,144,4,INK)+circle(93,144,4,INK)
    out += text(122,25,'POLAND / UKRAINE',11,INK,700)
    return out


def climate_scene():
    out = rect(0,0,300,156,'#B6CDC2')
    out += rect(0,112,300,44,'#56796F')
    out += path('M0 111 Q70 70 121 108 T300 104 V125 H0Z','#83A291')
    out += globe(150,64,48)
    out += path('M192 31 Q209 64 193 94','none','#D67B45',7)
    out += path('M203 18 l4 -7 m6 15 9 -5 m-12 21 11 1','none','#AA4F37',2)
    out += rect(84,104,132,34,'#E0CEAA',2,INK)
    out += text(150,125,'COP31',22,INK,900,anchor='middle')
    for x, skin, suit in [(38,'#AD7655','#274C56'),(75,'#D4A27A','#374D65'),(228,'#8A593E','#365B52'),(267,'#CF9B75','#364B64')]:
        out += path(f'M{x-11} 143 Q{x-12} 112 {x} 111 Q{x+12} 112 {x+11} 143Z',suit)
        out += circle(x,103,8,skin)
        out += path(f'M{x-8} 100 Q{x} 87 {x+8} 100',INK)
        out += path(f'M{x} 112 l-3 12 4 5 3 -5Z',GOLD)
    out += rect(20,32,3,64,INK)+rect(23,32,31,19,'#B84637')
    out += circle(35,41,6,'#F8E7C6')+circle(37,40,5,'#B84637')
    out += path('M20 146 H280','none',INK,2)
    out += text(150,17,'ANTALYA · TÜRKIYE',11,INK,700,anchor='middle')
    return out


def markets_scene():
    out = rect(0,0,300,156,'#DEC5AD')
    for x,h in [(8,69),(36,93),(69,78),(212,83),(244,100),(276,65)]:
        out += rect(x,148-h,21,h,'#B59A87')
        for y in range(155-h,143,12):
            out += rect(x+4,y,4,5,'#ECD9BA')+rect(x+13,y,4,5,'#ECD9BA')
    out += rect(81,51,137,85,INK,5)
    out += rect(89,59,121,63,'#32535B',2)
    for y in [71,88,105]:
        out += path(f'M95 {y} H204','none','#58767B',1)
    out += path('M96 68 L112 81 126 73 142 95 158 88 178 111 195 115','none','#F09A73',4)
    out += path('M185 111 L198 117 195 103Z','#F09A73')
    out += rect(132,136,34,9,INK)+rect(115,145,69,4,INK)
    out += rect(17,13,94,29,'#A54132',3)
    out += text(64,34,'AI STOCKS',14,'#FFF2D4',800,anchor='middle')
    out += circle(250,38,25,'#E9BF66',INK,2)
    out += text(250,46,'$',26,INK,700,anchor='middle')
    out += path('M250 14 V5 m-24 31 h-9 m35 27 v8','none',INK,2)
    out += rect(0,150,300,6,'#7E6B5E')
    return out


def icon(kind):
    out = circle(34,34,31,'#E2D8C3')
    if kind == 'bridge':
        out += path('M8 48 H61 M13 48 V22 M55 48 V22 M13 25 Q34 55 55 25','none',TEAL,4)
        for x in [23,34,45]:
            out += path(f'M{x} 40 V49','none',TEAL,2)
        out += circle(20,16,7,GOLD)+circle(49,16,7,RED)
    elif kind == 'health':
        out += rect(13,16,42,38,'#F7F0DE',3,TEAL)
        out += path('M28 23 H40 V30 H47 V40 H40 V47 H28 V40 H21 V30 H28Z',RED)
    elif kind == 'forest':
        for x,y in [(20,18),(43,16),(31,29)]:
            out += rect(x+3,y+15,5,22,INK)
            out += path(f'M{x+5} {y-7} l-15 27 h30Z','#3E795F')
        out += path('M8 57 Q34 47 61 58','none',GOLD,4)
    elif kind == 'port':
        out += path('M8 48 H60 L51 59 H20Z',TEAL)
        out += rect(22,33,25,14,GOLD)+rect(28,23,5,10,INK)
        out += path('M51 46 V17 H28 M51 17 L60 29 M34 17 V26','none',INK,3)
        out += path('M10 64 Q22 59 33 64 T60 64','none',TEAL,2)
    elif kind == 'server':
        for y in [12,28,44]:
            out += rect(14,y,40,12,TEAL,2)+circle(21,y+6,2,GOLD)
            out += path(f'M29 {y+6} H47','none','#D2DDCA',2)
        out += path('M12 60 L56 8','none',RED,5)
    elif kind == 'ocean':
        out += path('M8 24 Q20 16 32 24 T60 24 M8 35 Q20 27 32 35 T60 35','none',TEAL,3)
        out += path('M14 52 Q32 42 55 53 L55 60 H14Z',GOLD)
        out += circle(23,52,4,INK)+circle(35,50,3,INK)+circle(46,54,4,INK)
        out += path('M38 8 V40 L33 46 H48','none',RED,3)
    return out


def compose():
    out = ['<svg xmlns="http://www.w3.org/2000/svg" width="1024" height="1024" viewBox="0 0 1024 1024">']
    out += [rect(0,0,1024,1024,PAPER)]
    out += [text(28,28,'THE DAILY PICTURE',14,TEAL,800),text(996,28,'ONE DAY · SIX CONTINENTS',14,TEAL,800,anchor='end')]
    out += [text(512,84,'THE WORLD, IN FOCUS',55,INK,900,'serif','middle')]
    out += [rect(28,98,968,3,INK),text(512,129,'FRIDAY 20 NOVEMBER 2026',25,INK,800,anchor='middle')]
    out += [text(512,151,'WAR & SECURITY  /  CLIMATE  /  MARKETS  /  PEOPLE',13,TEAL,700,anchor='middle'),rect(28,160,968,1,INK)]
    leads = [
        (28,['Russian strikes','reach Poland'],['Warsaw: missiles and a drone;','no reported injuries in Poland.'],poland_scene,'01  EUROPE · SECURITY','Guardian / Polish officials'),
        (358,['COP31 runs','into overtime'],['Fossil-fuel dispute stalls talks;','no final deal on Friday.'],climate_scene,'02  ASIA · CLIMATE','Guardian; Al Jazeera'),
        (688,['AI sell-off','shakes markets'],['Anthropic shares fall 9%;','Nasdaq loses its 2026 gains.'],markets_scene,'03  GLOBAL · ECONOMY','Guardian / market close'),
    ]
    for x,title,deck,scene,label,source in leads:
        out += [text(x,185,label,13,RED,800),lines(x,222,title,34,36,family='serif')]
        out += [f'<g transform="translate({x},272)">{scene()}</g>']
        out += [lines(x,453,deck,19,23,weight=500),text(x,497,source,12,TEAL,600)]
    out += [rect(28,511,968,3,INK),text(28,539,'THE WORLD BEYOND THE LEADS',16,RED,800)]
    cards = [
        ('EUROPE','UK–EU reset',['Trade & youth','mobility deal'],['Agreed package;','legal steps remain.'],'bridge','AJ · AFP / AP / Reuters'),
        ('AFRICA','DR Congo',['Ebola families','count the cost'],['Bunia dispatch details','outbreak’s human toll.'],'health','Guardian · 20 Nov report'),
        ('SOUTH AMERICA','Brazil',['Ancestral land','recognised'],['Kapot Nhinore; final','demarcation still pending.'],'forest','AJ / AFP · 20 Nov report'),
        ('ASIA','Yemen & Saudi Arabia',['Rival forces','threaten ports'],['Houthis warn; coalition','says it struck Hodeidah.'],'port','AJ · AFP / Reuters'),
        ('NORTH AMERICA','United States',['Trump floats','overseas AI ban'],['Data-centre threat,','not enacted policy.'],'server','BBC · Rachel Clun'),
        ('OCEANIA','American Samoa',['Seabed auction','sparks outcry'],['Exploration leases face','legal opposition.'],'ocean','Guardian · 20 Nov report'),
    ]
    for i,(region,place,title,deck,symbol,source) in enumerate(cards):
        x = 28+(i%3)*330
        y = 555+(i//3)*171
        out += [rect(x,y,308,155,'#ECE5D7',4)]
        out += [text(x+12,y+19,region,11,TEAL,800),text(x+12,y+40,place,14,RED,700)]
        out += [lines(x+12,y+64,title,25,27,family='serif')]
        out += [f'<g transform="translate({x+236},{y+42}) scale(.87)">{icon(symbol)}</g>']
        out += [lines(x+12,y+117,deck,19,23,weight=500)]
    out += [rect(28,899,968,2,INK),text(28,924,'MORE IN THE DAY’S REPORTING',14,RED,800)]
    out += [text(28,953,'Nigeria: ferry deaths  ·  AI proof claim: verification pending  ·  Colombia: tax protests',18,INK,800)]
    out += [rect(28,989,968,1,INK),text(28,1008,'Sources: The Guardian · Al Jazeera · BBC  |  Full ledger: SOURCES.md',11,TEAL,600)]
    out += [text(996,1008,'Original symbolic illustrations',11,TEAL,500,anchor='end'),'</svg>']
    return '\n'.join(out)


def build():
    svg = compose()
    (ROOT/'frontpage.svg').write_text(svg,encoding='utf-8')
    page = '<!doctype html><html><head><meta charset="utf-8"><title>World · 20 November 2026</title><style>html,body{margin:0;width:1024px;height:1024px;overflow:hidden;background:'+PAPER+'}svg{display:block}</style></head><body>'+svg+'</body></html>'
    (ROOT/'frontpage.html').write_text(page,encoding='utf-8')
    return ROOT/'frontpage.html'


def validate_png(data):
    """Validate the exact offline artifact before handing it to the grader."""
    if len(data) > 1048576 or not data.startswith(b'\x89PNG\r\n\x1a\n'):
        raise ValueError('PNG signature or size is invalid')
    offset, dimensions, payload, finished, channels = 8, None, bytearray(), False, 0
    while offset < len(data):
        if offset + 12 > len(data):
            raise ValueError('Truncated chunk')
        count = struct.unpack_from('>I', data, offset)[0]
        kind = data[offset+4:offset+8]
        end = offset+12+count
        if end > len(data):
            raise ValueError('Truncated chunk payload')
        body = data[offset+8:end-4]
        expected = struct.unpack_from('>I', data, end-4)[0]
        if zlib.crc32(kind+body) & 0xffffffff != expected:
            raise ValueError('Invalid chunk checksum')
        if dimensions is None:
            if kind != b'IHDR' or count != 13:
                raise ValueError('Missing image header')
            w,h,depth,color,compression,filtering,interlace = struct.unpack('>IIBBBBB',body)
            if (w,h) != (1024,1024) or depth != 8 or color not in (2,6) or compression or filtering or interlace:
                raise ValueError('Unexpected raster format')
            dimensions = (w,h)
            channels = 3 if color == 2 else 4
        elif kind == b'IHDR':
            raise ValueError('Duplicate header')
        if kind == b'IDAT':
            payload.extend(body)
        if kind == b'IEND':
            if count or end != len(data):
                raise ValueError('Invalid image terminator')
            finished = True
            break
        offset = end
    if not finished or dimensions is None or not payload:
        raise ValueError('Incomplete PNG')
    try:
        decoder = zlib.decompressobj()
        expected_bytes = dimensions[1]*(1+dimensions[0]*channels)
        raster = decoder.decompress(payload, expected_bytes+1)
    except zlib.error as exc:
        raise ValueError('Invalid compressed pixels') from exc
    if len(raster) != expected_bytes or not decoder.eof or decoder.unused_data:
        raise ValueError('Invalid raster length')
    stride = 1+dimensions[0]*channels
    if any(raster[i] > 4 for i in range(0,len(raster),stride)):
        raise ValueError('Invalid scanline filter')
    return dimensions


def deliver():
    data = (ROOT/'frontpage.png').read_bytes()
    validate_png(data)
    destination = Path(os.environ.get('MAKEFUN_OUTPUT_DIR','/output'))
    destination.mkdir(parents=True,exist_ok=True)
    (destination/'entry.png').write_bytes(data)
    return destination/'entry.png'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--build',action='store_true',help='write SVG and HTML for local rasterisation')
    args = parser.parse_args()
    print(build() if args.build else deliver())


if __name__ == '__main__':
    main()
