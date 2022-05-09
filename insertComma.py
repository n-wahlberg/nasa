import json



with open('Data/natural/database.json', 'r') as f:
    s = f.read()

while True:
    try:
        data = json.loads(s)
        break
    except json.decoder.JSONDecodeError as e:
        if not e.args[0].startswith("Expecting ',' delimiter:"):
            raise
        a = s[:(e.pos)]
        b = s[(e.pos):]
        s = ','.join((a, b))
        print ('%s  ::  %s' % (e.pos, len(s)))

dict = json.loads(s)
with open('Data/natural/newDB.json', 'w') as f:
    json.dump(s, f)
