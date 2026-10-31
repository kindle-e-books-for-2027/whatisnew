#!/usr/bin/env python3
"""Builds 10 short original books about new technology as EPUB + MOBI, with covers,
plus a Kindle-friendly index.html. Needs only Python 3 and Pillow (pip install pillow).
Run:  python build_books.py
"""
import os, io, time, uuid, struct, zipfile, textwrap
from html import escape
from PIL import Image, ImageDraw, ImageFont

AUTHOR = "Tech Horizons Press"

BOOKS = [
 dict(slug="flying-cars", title="Flying Cars", sub="The Sky Is the New Road", c=((12, 30, 80), (0, 160, 200)),
  chapters=[
   ("The Dream Takes Off", [
    "For more than a century, people have imagined a car that could simply lift off and glide over traffic. Early inventors bolted wings and propellers onto automobiles, but the results were loud, heavy, expensive and hard to fly. The dream never died, though. It just waited for better technology.",
    "Three things finally changed: light batteries, powerful electric motors and smart flight software. Together they made it possible to build small aircraft that are simpler, quieter and safer than the helicopters and planes of the past."]),
   ("The eVTOL Revolution", [
    "Most modern flying cars are really eVTOLs: electric Vertical Take-Off and Landing aircraft. Instead of one big engine, they use many small electric rotors. If one stops working, the others keep the aircraft balanced and flying. That built-in backup is a major safety advantage.",
    "Computers do much of the hard work. Sensors measure the aircraft's tilt and speed hundreds of times a second, and the software adjusts each rotor to keep the ride smooth. A pilot gives simple commands such as go up, go forward or land, and the machine handles the details."]),
   ("Air Traffic for Everyone", [
    "A sky full of small aircraft needs rules. Regulators must certify each design, train pilots and decide where and how high these vehicles may fly. Cities need vertiports, which are small landing pads on rooftops and near stations, with charging equipment built in.",
    "Software will also manage the traffic. Instead of a human controller talking to each aircraft, digital systems can share routes and keep every vehicle apart automatically. Noise is another challenge, so designers focus on rotors that sound more like a soft hum than a roar."]),
   ("What a Ride Might Feel Like", [
    "Picture a trip that takes forty minutes by road but only ten minutes through the air. You walk onto a pad, buckle in and lift straight up. The cabin is quiet, the view is wide, and there is no traffic below to worry about.",
    "Challenges remain. Batteries limit range, bad weather can ground flights, and prices must fall before most people can afford a seat. Still, air taxis are likely to arrive first as short city hops, and that is how the flying car dream becomes real."])]),
 dict(slug="self-driving-cars", title="Self-Driving Cars", sub="Roads Without Drivers", c=((20, 20, 40), (255, 120, 40)),
  chapters=[
   ("Levels of Autonomy", [
    "Engineers describe driving automation in six levels, from zero to five. At level zero the human does everything. Cruise control and lane keeping sit in the middle. At level five a car could drive anywhere, in any weather, with no human at all.",
    "Today's most advanced robotaxis work at a high level, but only inside mapped areas and good conditions. Understanding these levels helps you see what a car can really do, and what it cannot yet do."]),
   ("How a Car Sees", [
    "A self-driving car uses several senses at once. Cameras read signs and lane lines, radar measures the speed of objects even in rain, and lidar sends out laser pulses to build a detailed three-dimensional map of the surroundings.",
    "Software combines these signals into a single picture. It labels each object as a car, a cyclist or a pedestrian, then predicts where each one will move in the next few seconds before choosing a safe path."]),
   ("The Hard Part: Surprises", [
    "Driving on an empty highway is easy. The difficulty lies in rare events: a ball rolling into the street, a police officer waving traffic through, or a construction zone with confusing signs. Humans handle these with common sense, and machines must learn it from huge amounts of data.",
    "Companies test in simulation and on real roads, replaying difficult moments millions of times. Each lesson learned by one car can be shared with the whole fleet, something no human driver can do."]),
   ("Cities Without Parking Lots?", [
    "If cars drive themselves, ownership may matter less. Shared autonomous vehicles could serve many people each day, which would reduce the need for parking and free space for parks and homes.",
    "There are open questions about jobs, safety rules and who is responsible after a crash. Even so, many experts expect that automation will make roads safer, since software never gets tired, distracted or impatient."])]),
 dict(slug="artificial-intelligence", title="Artificial Intelligence", sub="Machines That Learn", c=((60, 10, 90), (240, 70, 140)),
  chapters=[
   ("What Is AI?", [
    "Artificial intelligence is software that performs tasks which normally need human thinking, such as recognizing faces, translating languages or recommending a song. Instead of following a fixed list of rules, modern AI learns patterns from examples.",
    "Show a system millions of labeled photos of cats and it gradually learns what makes a cat look like a cat. This approach, called machine learning, powers most of the AI you meet every day."]),
   ("Neural Networks", [
    "Many AI systems use neural networks, which are layers of simple mathematical units loosely inspired by the brain. Each unit takes in numbers, adjusts them and passes them along. Training slowly tunes millions or billions of these adjustments.",
    "When the network makes a mistake, the training process nudges the numbers so that the next answer is slightly better. Repeat this enough times with enough data, and the network can perform surprisingly complex tasks."]),
   ("Language and Creativity", [
    "Large language models learn from vast amounts of text and can write, summarize, translate and answer questions. Image and music models can create new pictures and songs from a short description.",
    "These tools are powerful but imperfect. They can sound confident while being wrong, and they can reflect biases found in their training data. Checking important facts is still the user's job."]),
   ("Living With AI", [
    "AI can help doctors read scans, help farmers save water and help students practice a new language. It can also automate tasks, which raises real questions about work, privacy and fairness.",
    "The best approach is to stay curious and careful. Learn what AI does well, notice where it fails, and remember that people decide how this technology is used."])]),
 dict(slug="quantum-computing", title="Quantum Computing", sub="A New Kind of Math Machine", c=((5, 10, 40), (120, 80, 255)),
  chapters=[
   ("Beyond Bits", [
    "Ordinary computers store information in bits, and each bit is either zero or one. A quantum computer uses qubits. Thanks to a property called superposition, a qubit can be in a blend of zero and one until it is measured.",
    "This does not mean a quantum computer is simply faster at everything. It means certain problems can be approached in a completely different way."]),
   ("Entanglement", [
    "Qubits can also be entangled, which links their states so that measuring one tells you something about the other. Einstein found this strange, yet experiments have confirmed it again and again.",
    "Quantum algorithms use superposition and entanglement together so that wrong answers cancel out and right answers become more likely. Designing such algorithms is a special skill."]),
   ("What Is It Good For?", [
    "Promising uses include simulating molecules for new medicines and materials, optimizing complex schedules and routes, and breaking some of today's encryption codes. Researchers are already creating new encryption that quantum machines cannot break.",
    "For everyday tasks like email or video, regular computers will remain the better choice. Quantum computers are more like specialist tools than replacements."]),
   ("The Big Challenges", [
    "Qubits are fragile. Heat, vibration and stray radiation can destroy their delicate states, so many machines operate colder than outer space. Errors are common, and correcting them needs many extra qubits.",
    "Progress is steady rather than sudden. Each improvement in stability and error correction brings useful quantum computing a little closer."])]),
 dict(slug="humanoid-robots", title="Humanoid Robots", sub="Helpers With Two Legs", c=((30, 40, 50), (80, 220, 160)),
  chapters=[
   ("Why Human Shape?", [
    "Our world is built for people: doors, stairs, tools and shelves all fit the human body. A robot with two arms, two legs and hands can use these spaces without changing them, which is the main argument for humanoid design.",
    "Wheeled or specialized robots are often cheaper for one job. Humanoids aim to be flexible, able to do many different tasks in the same place."]),
   ("Balance and Movement", [
    "Walking on two legs is surprisingly hard. A humanoid robot constantly measures its tilt and the force on its feet, then adjusts dozens of motors many times per second to avoid falling.",
    "Modern robots can walk, climb stairs and even recover from a push. Strong, light electric actuators and better control software made this possible."]),
   ("The Robot Brain", [
    "Cameras and sensors let the robot see its surroundings, while AI helps it understand instructions such as please move these boxes to the shelf. The system plans the steps and adjusts when something goes wrong.",
    "Robots can now learn from demonstrations, watching a human do a task and then copying it. This lowers the need for painstaking programming."]),
   ("Working Beside Us", [
    "Early humanoids are likely to work in warehouses and factories, handling repetitive or heavy tasks. Later versions may help in hospitals, care homes and eventually homes.",
    "Society will need to think about safety, jobs and trust. The goal is not to replace people but to take over the dull, dirty and dangerous work."])]),
 dict(slug="space-travel-reborn", title="Space Travel Reborn", sub="Rockets That Come Back", c=((0, 0, 20), (255, 90, 90)),
  chapters=[
   ("Landing a Rocket", [
    "For decades, rockets were thrown away after one flight, like a jet that is scrapped after landing. Reusable rockets changed that by flying back to Earth and landing upright, ready for another trip.",
    "Reuse lowers the cost of reaching orbit. When launches become cheaper, more satellites, science missions and new businesses become possible."]),
   ("A Crowded Orbit", [
    "Thousands of satellites now circle the planet, providing internet, weather forecasts, navigation and images. Low orbits make fast communication possible but also increase the risk of collisions and space debris.",
    "Operators are learning to steer satellites away from danger and to bring them down safely at the end of their lives."]),
   ("Back to the Moon", [
    "Space agencies and companies are planning long-term bases on the Moon. It offers a place to test technology, search for useful resources and practice living away from Earth.",
    "Moon missions are also a stepping stone. Lessons learned there will help prepare for longer journeys deeper into space."]),
   ("Space for Visitors", [
    "Space tourism is beginning with short flights to the edge of space and longer stays in orbit. Tickets are costly today, but history shows that costs tend to fall as technology matures.",
    "The biggest dream is Mars. The trip is long and dangerous, with radiation, supplies and health all to consider, yet each year the technology gets closer."])]),
 dict(slug="fusion-energy", title="Fusion Energy", sub="Building a Star on Earth", c=((90, 20, 0), (255, 200, 40)),
  chapters=[
   ("Power of the Sun", [
    "The Sun shines because hydrogen atoms fuse together into helium, releasing enormous energy. Fusion power plants aim to copy this process on Earth.",
    "Fuel is abundant: forms of hydrogen can be taken from seawater. Fusion produces no carbon dioxide and creates much less long-lived waste than today's nuclear fission."]),
   ("Two Ways to Fuse", [
    "To fuse, atoms must be heated to over a hundred million degrees. One approach uses tokamaks, doughnut-shaped machines that hold the hot gas inside powerful magnetic fields. Another approach fires intense lasers at a tiny fuel pellet.",
    "Both methods have achieved major milestones in recent years, showing that the physics works."]),
   ("The Break-Even Challenge", [
    "The goal is net energy: getting more power out than you put in. That is hard, and doing it continuously and economically is harder still.",
    "Engineers must also build materials that survive intense heat and radiation, and systems that breed fuel safely. Private companies and governments are racing to solve each piece."]),
   ("A Cleaner Future", [
    "If fusion succeeds, it could provide steady, clean electricity day and night. It would complement solar and wind rather than replace them.",
    "Nobody knows exactly when fusion will reach the grid. Even so, steady progress makes it one of the most exciting energy stories of our time."])]),
 dict(slug="brain-computer-interfaces", title="Brain-Computer Interfaces", sub="Where Thought Meets Machine", c=((10, 40, 60), (200, 100, 255)),
  chapters=[
   ("Listening to the Brain", [
    "Your brain communicates using tiny electrical signals. A brain-computer interface, or BCI, picks up these signals and turns them into commands for a computer or device.",
    "Some systems sit on the scalp and are completely non-invasive. Others are implanted in or on the brain and can capture much more detailed information."]),
   ("Restoring Abilities", [
    "The most important use is helping people with paralysis or lost speech. Patients have used implants to move a cursor, control a robotic arm or turn their intended words into text on a screen.",
    "These results show that the brain can learn to control a machine, and the machine can learn to understand the brain."]),
   ("Beyond Medicine", [
    "Simple headsets are being explored for games, focus training and hands-free control. Their accuracy is still limited compared with implants.",
    "Researchers are also developing devices that send signals into the brain, for example to restore a sense of touch through a prosthetic hand."]),
   ("Privacy and Ethics", [
    "Brain data is deeply personal. Who owns it, how it is stored and who can use it are urgent questions that laws are only beginning to address.",
    "Clear rules, strong security and informed consent will be essential if this technology is to earn public trust."])]),
 dict(slug="drone-delivery", title="Drone Delivery", sub="Packages From the Sky", c=((0, 60, 70), (250, 230, 60)),
  chapters=[
   ("A Parcel in Minutes", [
    "A drone can lift a small package, fly straight to a doorstep and return, all without a truck or a traffic jam. For light items such as food, medicine and small parts, it can be faster than any road vehicle.",
    "Drones are especially useful where roads are poor or distances are large."]),
   ("How They Work", [
    "A delivery drone navigates using satellite positioning, cameras and obstacle sensors. It follows a planned route and can avoid birds, trees and wires.",
    "Many designs lower the parcel on a thin line or drop it gently into a marked spot, so that the drone never has to land near people."]),
   ("Saving Lives", [
    "Medical delivery is one of the most valuable uses. Drones have carried blood, vaccines and test samples to remote clinics in a fraction of the usual time.",
    "In emergencies, a drone can even bring a defibrillator to a patient before an ambulance arrives."]),
   ("Rules and Neighbors", [
    "Aviation authorities require drones to stay within safe heights, keep away from airports and follow approved routes. Operators also have to consider noise and privacy.",
    "As routes spread, communities will help decide where drones fly, and clear rules will make the skies friendly for everyone."])]),
 dict(slug="battery-revolution", title="The Battery Revolution", sub="Power for a New Age", c=((10, 50, 20), (150, 230, 60)),
  chapters=[
   ("Storing Energy", [
    "A battery stores energy in chemical form and releases it as electricity. Almost every modern device, from phones to electric cars, relies on rechargeable lithium-ion batteries.",
    "Their success came from a good balance of energy, weight, cost and lifetime, and years of steady improvement have made them cheaper and better."]),
   ("Solid-State Hopes", [
    "Solid-state batteries replace the liquid inside a cell with a solid material. Researchers hope this could allow faster charging, longer range and a lower risk of fire.",
    "Making them in large numbers at low cost is a difficult engineering task, which is why progress takes time."]),
   ("Batteries for the Grid", [
    "Solar and wind power vary with the weather. Large batteries store extra energy when production is high and release it in the evening, helping keep the lights on.",
    "Other options, such as pumped water storage and new battery chemistries based on cheaper materials, are growing too."]),
   ("Recycling and Responsibility", [
    "Batteries use metals that must be mined, so recycling is important. Recovery plants can reclaim valuable materials such as lithium, nickel and cobalt and use them in new batteries.",
    "Better design, longer lifetimes and strong recycling will make the battery revolution cleaner as well as more powerful."])]),
]

# ---------------------------------------------------------------- covers
W, H = 1200, 1800
def font(bold, size):
    for p in (["/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf"] if bold else
              ["/usr/share/fonts/truetype/google-fonts/Poppins-Regular.ttf",
               "/usr/share/fonts/truetype/google-fonts/Poppins-Medium.ttf"]) + \
             ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"]:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()

def wrap(draw, text, fnt, maxw):
    lines, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= maxw:
            cur = t
        else:
            lines.append(cur); cur = w
    return lines + [cur]

def make_cover(book, idx, path):
    c1, c2 = book["c"]
    img = Image.new("RGB", (W, H))
    px = ImageDraw.Draw(img)
    for y in range(H):
        t = y / (H - 1)
        px.line([(0, y), (W, y)], fill=tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3)))
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    m = idx % 5
    cx, cy = W // 2, 600
    if m == 0:      # rings
        for r in range(80, 560, 70): d.ellipse([cx-r, cy-r, cx+r, cy+r], outline=(255, 255, 255, 110), width=6)
        d.ellipse([cx-40, cy-40, cx+40, cy+40], fill=(255, 255, 255, 200))
    elif m == 1:    # grid of dots
        for gx in range(150, W-100, 100):
            for gy in range(200, 1000, 100):
                d.ellipse([gx-12, gy-12, gx+12, gy+12], fill=(255, 255, 255, 140))
    elif m == 2:    # diagonal bars
        for k in range(-6, 12):
            d.polygon([(k*110, 1000), (k*110+60, 1000), (k*110+460, 200), (k*110+400, 200)], fill=(255, 255, 255, 70))
    elif m == 3:    # arcs
        for r in range(100, 700, 90):
            d.arc([cx-r, 1000-r, cx+r, 1000+r], 180, 360, fill=(255, 255, 255, 140), width=10)
    else:           # concentric squares
        for r in range(60, 520, 80):
            d.rectangle([cx-r, cy-r, cx+r, cy+r], outline=(255, 255, 255, 120), width=6)
    d.rectangle([60, 1080, W-60, 1700], fill=(0, 0, 0, 120))
    img = Image.alpha_composite(img.convert("RGBA"), ov).convert("RGB")
    d = ImageDraw.Draw(img)
    d.text((90, 90), "TECH HORIZONS", font=font(True, 36), fill=(255, 255, 255))
    d.rectangle([90, 150, 330, 156], fill=(255, 255, 255))
    ft, fs, fa = font(True, 104), font(False, 46), font(True, 38)
    y = 1120
    for line in wrap(d, book["title"].upper(), ft, W - 200):
        d.text((100, y), line, font=ft, fill=(255, 255, 255)); y += 122
    y += 10
    for line in wrap(d, book["sub"], fs, W - 200):
        d.text((100, y), line, font=fs, fill=(220, 220, 220)); y += 62
    d.text((100, 1630), AUTHOR, font=fa, fill=(255, 255, 255))
    img.save(path, "JPEG", quality=88)

# ---------------------------------------------------------------- EPUB
CSS = """body{font-family:serif;line-height:1.5;margin:5%}h1,h2{font-family:sans-serif}
h2{margin-top:1.5em}p{text-indent:1.2em;margin:0 0 .6em}.c{text-align:center}img{max-width:100%}"""

def xh(title, body):
    return ('<?xml version="1.0" encoding="utf-8"?>\n<!DOCTYPE html>\n'
            '<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" lang="en"><head>'
            f'<title>{escape(title)}</title><link rel="stylesheet" type="text/css" href="style.css"/></head><body>{body}</body></html>')

def make_epub(book, cover_path, out):
    bid = "urn:uuid:" + str(uuid.uuid5(uuid.NAMESPACE_URL, "techhorizons/" + book["slug"]))
    title, chs = book["title"], book["chapters"]
    files = {}
    files["OEBPS/style.css"] = CSS
    files["OEBPS/cover.xhtml"] = xh(title, f'<div class="c"><img src="cover.jpg" alt="Cover"/></div>')
    files["OEBPS/title.xhtml"] = xh(title, f'<div class="c"><h1>{escape(title)}</h1><h2>{escape(book["sub"])}</h2><p class="c">{AUTHOR}</p></div>')
    for i, (ct, paras) in enumerate(chs, 1):
        files[f"OEBPS/ch{i}.xhtml"] = xh(ct, f"<h2>{i}. {escape(ct)}</h2>" + "".join(f"<p>{escape(p)}</p>" for p in paras))
    nav_items = "".join(f'<li><a href="ch{i}.xhtml">{escape(c[0])}</a></li>' for i, c in enumerate(chs, 1))
    files["OEBPS/nav.xhtml"] = xh("Contents", f'<nav epub:type="toc"><h2>Contents</h2><ol>{nav_items}</ol></nav>')
    ncx = "".join(f'<navPoint id="n{i}" playOrder="{i}"><navLabel><text>{escape(c[0])}</text></navLabel><content src="ch{i}.xhtml"/></navPoint>'
                  for i, c in enumerate(chs, 1))
    files["OEBPS/toc.ncx"] = ('<?xml version="1.0" encoding="utf-8"?><ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1">'
        f'<head><meta name="dtb:uid" content="{bid}"/></head><docTitle><text>{escape(title)}</text></docTitle><navMap>{ncx}</navMap></ncx>')
    manifest = ('<item id="ncx" href="toc.ncx" media-type="application/x-dtbncx+xml"/>'
                '<item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>'
                '<item id="css" href="style.css" media-type="text/css"/>'
                '<item id="cover-image" href="cover.jpg" media-type="image/jpeg" properties="cover-image"/>'
                '<item id="cover" href="cover.xhtml" media-type="application/xhtml+xml"/>'
                '<item id="title" href="title.xhtml" media-type="application/xhtml+xml"/>')
    manifest += "".join(f'<item id="ch{i}" href="ch{i}.xhtml" media-type="application/xhtml+xml"/>' for i in range(1, len(chs)+1))
    spine = '<itemref idref="cover"/><itemref idref="title"/>' + "".join(f'<itemref idref="ch{i}"/>' for i in range(1, len(chs)+1))
    files["OEBPS/content.opf"] = ('<?xml version="1.0" encoding="utf-8"?>'
        '<package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="uid">'
        '<metadata xmlns:dc="http://purl.org/dc/elements/1.1/">'
        f'<dc:identifier id="uid">{bid}</dc:identifier><dc:title>{escape(title)}: {escape(book["sub"])}</dc:title>'
        f'<dc:creator>{AUTHOR}</dc:creator><dc:language>en</dc:language>'
        '<meta property="dcterms:modified">2026-10-31T00:00:00Z</meta><meta name="cover" content="cover-image"/></metadata>'
        f'<manifest>{manifest}</manifest><spine toc="ncx">{spine}</spine></package>')
    with zipfile.ZipFile(out, "w") as z:
        z.writestr(zipfile.ZipInfo("mimetype"), "application/epub+zip", compress_type=zipfile.ZIP_STORED)
        z.writestr("META-INF/container.xml", '<?xml version="1.0"?><container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">'
                   '<rootfiles><rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/></rootfiles></container>',
                   compress_type=zipfile.ZIP_DEFLATED)
        for name, data in files.items():
            z.writestr(name, data, compress_type=zipfile.ZIP_DEFLATED)
        z.write(cover_path, "OEBPS/cover.jpg", compress_type=zipfile.ZIP_STORED)

# ---------------------------------------------------------------- MOBI (MOBI6, uncompressed)
def exth(records):
    body = b"".join(struct.pack(">II", t, len(d) + 8) + d for t, d in records)
    n = len(records)
    length = 12 + len(body)
    pad = (-length) % 4
    return b"EXTH" + struct.pack(">II", length + pad, n) + body + b"\0" * pad

def make_mobi(book, cover_path, out):
    title = f'{book["title"]}: {book["sub"]}'
    h = [f"<h1>{escape(book['title'])}</h1><h3>{escape(book['sub'])}</h3><p>{AUTHOR}</p><mbp:pagebreak/>"]
    h.append("<h2>Contents</h2>" + "".join(f"<p>{i}. {escape(c[0])}</p>" for i, c in enumerate(book["chapters"], 1)) + "<mbp:pagebreak/>")
    for i, (ct, paras) in enumerate(book["chapters"], 1):
        h.append(f"<h2>{i}. {escape(ct)}</h2>" + "".join(f"<p>{escape(p)}</p>" for p in paras) + "<mbp:pagebreak/>")
    html = ("<html><head><guide></guide></head><body>" + "".join(h) + "</body></html>").encode("ascii", "xmlcharrefreplace")
    text_recs = [html[i:i + 4096] for i in range(0, len(html), 4096)]
    n_text = len(text_recs)

    im = Image.open(cover_path).convert("RGB")
    def jpg(size):
        b = io.BytesIO(); im.resize(size).save(b, "JPEG", quality=85); return b.getvalue()
    images = [jpg((800, 1200)), jpg((330, 495))]          # cover + thumbnail
    first_img = n_text + 1
    flis_no, fcis_no = first_img + len(images), first_img + len(images) + 1
    flis = (b"FLIS\x00\x00\x00\x08\x00\x41\x00\x00\x00\x00\x00\x00\xff\xff\xff\xff\x00\x01\x00\x03"
            b"\x00\x00\x00\x03\x00\x00\x00\x01\xff\xff\xff\xff")
    fcis = (b"FCIS\x00\x00\x00\x14\x00\x00\x00\x10\x00\x00\x00\x01\x00\x00\x00\x00" + struct.pack(">I", len(html)) +
            b"\x00\x00\x00\x00\x00\x00\x00\x20\x00\x00\x00\x08\x00\x01\x00\x01\x00\x00\x00\x00")
    eof = b"\xe9\x8e\x0d\x0a"

    ex = exth([(100, AUTHOR.encode()), (503, title.encode()), (524, b"en"), (204, struct.pack(">I", 201)),
               (201, struct.pack(">I", 0)), (202, struct.pack(">I", 1))])
    name = title.encode("ascii", "replace")
    name_off = 16 + 232 + len(ex)
    m = bytearray(232)
    def put(off, fmt, *v): struct.pack_into(fmt, m, off, *v)
    m[0:4] = b"MOBI"; put(4, ">I", 232); put(8, ">I", 2); put(12, ">I", 65001)
    put(16, ">I", uuid.uuid5(uuid.NAMESPACE_URL, book["slug"]).int & 0xFFFFFFFF); put(20, ">I", 6)
    for o in range(24, 64, 4): put(o, ">I", 0xFFFFFFFF)
    put(64, ">I", first_img); put(68, ">I", name_off); put(72, ">I", len(name))
    put(76, ">I", 0x409); put(88, ">I", 6); put(92, ">I", first_img)
    put(112, ">I", 0x50); put(148, ">I", 0xFFFFFFFF); put(152, ">I", 0xFFFFFFFF)
    put(176, ">HH", 1, n_text); put(180, ">I", 1)
    put(184, ">I", fcis_no); put(188, ">I", 1); put(192, ">I", flis_no); put(196, ">I", 1)
    put(208, ">I", 0xFFFFFFFF); put(216, ">I", 0xFFFFFFFF); put(220, ">I", 0xFFFFFFFF); put(228, ">I", 0xFFFFFFFF)
    palm = struct.pack(">HHIHHHH", 1, 0, len(html), n_text, 4096, 0, 0)
    rec0 = palm + bytes(m) + ex + name + b"\0" * 1024

    recs = [rec0] + text_recs + images + [flis, fcis, eof]
    n = len(recs)
    now = int(time.time()) + 2082844800
    hdr = (title[:31].replace(" ", "_").encode("ascii", "replace").ljust(32, b"\0") +
           struct.pack(">HHIII", 0, 0, now, now, 0) + struct.pack(">IIII", 0, 0, 0, 0)[:12] +
           b"BOOKMOBI" + struct.pack(">IIH", 2 * n - 1, 0, n))
    off = len(hdr) + 8 * n + 2
    table = b""
    for i, r in enumerate(recs):
        table += struct.pack(">I", off) + bytes([0]) + (2 * i).to_bytes(3, "big")
        off += len(r)
    with open(out, "wb") as f:
        f.write(hdr + table + b"\0\0" + b"".join(recs))

# ---------------------------------------------------------------- index page
def build_index():
    rows = ""
    for b in BOOKS:
        s = b["slug"]
        rows += (f'<tr><td width="90"><img src="covers/{s}.jpg" width="80" alt=""></td>'
                 f'<td><b>{escape(b["title"])}</b><br>{escape(b["sub"])}<br><br>'
                 f'<a href="books/{s}.mobi">[ Download MOBI ]</a>&nbsp;&nbsp;'
                 f'<a href="books/{s}.epub">[ Download EPUB ]</a></td></tr>'
                 '<tr><td colspan="2"><hr></td></tr>\n')
    open("index.html", "w", encoding="utf-8").write(
        '<!DOCTYPE html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">'
        '<title>Tech Library</title></head><body bgcolor="#ffffff" text="#000000"><h1>Tech Library</h1>'
        '<p>10 short books about new technology. MOBI for older Kindles, EPUB for newer ones.</p><hr>'
        f'<table width="100%" cellpadding="6">\n{rows}</table></body></html>')

if __name__ == "__main__":
    os.makedirs("books", exist_ok=True); os.makedirs("covers", exist_ok=True)
    for i, b in enumerate(BOOKS):
        cp = f"covers/{b['slug']}.jpg"
        make_cover(b, i, cp)
        make_epub(b, cp, f"books/{b['slug']}.epub")
        make_mobi(b, cp, f"books/{b['slug']}.mobi")
        print("built", b["title"])
    build_index()
    print("done: index.html, books/, covers/")
