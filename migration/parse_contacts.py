# coding=utf-8
from BeautifulSoup import BeautifulSoup, Comment


files = ['print/%i.html' % i for i in range(1, 6)]
soups = [BeautifulSoup(open(file)) for file in files]
layouts = ['layout%i' % i for i in (3, 5, 9, 10, 11, 13, 14, 16)]
municipalities = [
    'Baar', 'Cham', 'Neuheim', 'Zug', 'Rotkreuz', u'Unterägeri', 'Risch',
    u'Hünenberg', u'Oberägeri', 'Menzingen', "H'berg",
    'Morgarten', 'Steinhausen', 'Finstersee'
]
name_parts = ['de', 'den', 'del', 'di', 'von', 'van']


class Contact(object):
    def __init__(self):
        self.name = ''
        self.vorname = ''
        self.partei = ''
        self.jahrgang = ''
        self.beruf = ''
        self.adresse = ''
        self.nummer = ''
        self.direkt_nr = ''
        self.titel = ''
        self.asterisk = False

    def __str__(self):
        str = '%s, %s, %s, %s, %s, %s, %s, %s, %s' % (
            self.name, self.vorname, self.titel, self.beruf, self.jahrgang,
            self.partei, self.adresse, self.nummer, self.direkt_nr
        )
        return str.encode('utf8')


def strip(text):
    if isinstance(text, list):
        text = ''.join(text)
    return text.replace('&nbsp;', ' ').strip()


def get_comments(soup):
    """ Returns alls comments in a soup. """
    return soup.findAll(text=lambda text: isinstance(text, Comment))


def get_unique_comments():
    """ Returns all unique comments in a soup.

    Useful to find the layouts used in this script.
    """
    comments = []
    for soup in soups:
        comments.extend(get_comments(soup))
        comments = list(set(comments))
    return comments


def get_person_tables(soup):
    """ Returns all tables which contains informations about people.

    Tables with such information are preceeded by a commment indicating a
    special layout, e.g. 'PERSON: Name, Vorname, Telefon'."""
    comments = []
    for comment in get_comments(soup):
        if any([layout in comment for layout in layouts]):
            comments.append(comment)

    tables = []
    for comment in comments:
        candidate = comment.findNext()
        if candidate.name == 'table':
            tables.append((candidate, comment))

    return tables


def get_all_person_tables():
    """ Returns a dict with all tables containing information about
    people from all soups ordered by layout. """
    all_tables = []
    for soup in soups:
        all_tables.extend(get_person_tables(soup))

    tables = {}
    for layout in layouts:
        tables[layout] = filter(lambda t: layout in t[1], all_tables)
    return tables


def parse_name(fields):
    """ Returns a tuple name, vorname from a list"""
    if fields[0].lower() in name_parts and len(fields) >= 3:
        return ' '.join(fields[:2]).strip(), ' '.join(fields[2:]).strip()
    return fields[0].strip(), ' '.join(fields[1:]).strip()


def is_title(text):
    return ('.' in text and 'Stv.' not in text) or 'MLaw' in text


def appended_text(field, text):
    if field:
        return field + ' / ' + text
    else:
        return text


def parse_layout3(table):
    # PERSON: Name, Vorname, Telefon
    # more like: Name Vorname
    contacts = []
    for cell in table.findChildren('td'):
        content = cell.contents[0].replace('&nbsp;', ' ').strip()
        if content:
            fields = content.split(' ')
            name, vorname = parse_name(fields)
            contact = Contact()
            contact.name = name
            contact.vorname = vorname
            contacts.append(contact)
    return contacts


def parse_layout5(table):
    # PERSON: Funktion, Name, Vorname
    # more like: Funktion > Name Vorname, Telfon/Ort, Direkt Nr
    contacts = []
    for row in table.findChildren('tr'):
        cells = row.findChildren('td')
        if len(cells) > 1:
            contact = Contact()

            contents = strip(cells[1].contents)
            if '*' in contents:
                contact.asterisk = True
            contents = contents.replace('*', '').strip()
            if not contents:
                continue

            fields = contents.split(',')
            fields = [field.strip() for field in fields]

            # Name & Vorname
            name, vorname = parse_name(fields[0].split(' '))
            if not any([name, vorname]):
                continue
            contact.name = name
            contact.vorname = vorname

            # Telfon, Direkt Nummer, Ort
            if len(fields) >= 2:
                text = fields[1]
                if 'Tel.:' in text:
                    text = text.replace('Tel.:', '').strip()
                    contact.nummer = text
                elif 'direkt:' in text:
                    text = text.replace('direkt:', '').strip()
                    contact.direkt_nr = text
                elif text in municipalities:
                    contact.adresse = text

            # Direkt Nummer
            if len(fields) >= 3:
                text = fields[2]
                assert 'direkt:' in text
                text = text.replace('direkt:', '').replace(' ', '').strip()
                contact.direkt_nr = text

            contacts.append(contact)

    return contacts


def parse_layout9(table):
    # PERSON: Name Vorname, Jahrgang, Beruf, Adresse
    # more like: Name Vorname, Jahrgang, Beruf, Adresse > Partei > Eintritt
    contacts = []
    for row in table.findChildren('tr'):
        # Ignor table titles
        if 'TABtitel' in str(row):
            continue

        cells = row.findChildren('td')
        if len(cells) == 3:
            contact = Contact()

            fields = strip(cells[0].contents).split(',')
            fields = [field.strip() for field in fields]

            # Name & Vorname
            name, vorname = parse_name(fields[0].split(' '))
            contact.name = name
            contact.vorname = vorname

            # Jahrgang
            index = 3
            try:
                contact.jahrgang = str(int(fields[1]))
            except ValueError:
                index = 2

            # Beruf & Adresse
            if index < len(fields):
                if not any([('%i' % i) in fields[index] for i in range(10)]):
                    contact.beruf = fields[index]
                    index += 1
                if index < len(fields):
                    contact.adresse = ' '.join(fields[index:])

            # Partei
            contact.partei = strip(cells[1].contents)

            contacts.append(contact)

    return contacts


def parse_layout10(table):
    # PERSON: Funktion, Name Vorname, Titel, Partei
    # more like: Funktion > Name Vorname, Titel, Partei/Ort
    contacts = []
    for row in table.findChildren('tr'):
        cells = row.findChildren('td')
        if len(cells) > 1:
            contact = Contact()

            contents = strip(cells[1].contents)
            if '*' in contents:
                contact.asterisk = True
            contents = contents.replace('*', '').strip()
            if not contents:
                continue

            fields = contents.split(',')
            fields = [field.strip() for field in fields]

            # Name & Vorname
            name, vorname = parse_name(fields[0].split(' '))
            contact.name = name
            contact.vorname = vorname

            if len(fields) >= 2:
                contact.beruf = fields[1]

            if len(fields) >= 3:
                # guess if it is a politcal party
                text = fields[2]
                if (text.upper() == text and '.' not in text):
                    contact.partei = text
                elif is_title(text):
                    # or part of the title
                    contact.beruf = appended_text(contact.beruf, text)
                else:
                    if text in municipalities:
                        # or an andress
                        contact.adresse = text
                    else:
                        # or profession
                        contact.beruf = appended_text(contact.beruf, text)

            contacts.append(contact)

    return contacts


def parse_layout11(table):
    # PERSON: Funktion, Name Vorname, Partei, Eintritt
    # more like: Funktion > Name Vorname, Partei > Eintritt
    contacts = []
    for row in table.findChildren('tr'):
        cells = row.findChildren('td')
        if len(cells) > 1:
            contact = Contact()

            fields = strip(cells[1].contents).split(',')
            fields = [field.strip() for field in fields]

            # Name & Vorname
            name, vorname = parse_name(fields[0].split(' '))
            if not any([name, vorname]):
                continue
            contact.name = name
            contact.vorname = vorname

            # Partei
            if len(fields) >= 2:
                contact.partei = fields[1]

            contacts.append(contact)

    return contacts


def parse_layout13(table):
    # PERSON: Funktion > Name Vorname, Titel, Adresse
    # More like: Funktion > Name Vorname, Titel, Ort, Ressort
    contacts = []
    for row in table.findChildren('tr'):
        cells = row.findChildren('td')
        if len(cells) > 1:
            contact = Contact()

            contents = strip(cells[1].contents)
            if '*' in contents:
                contact.asterisk = True
            contents = contents.replace('*', '').strip()

            fields = contents.split(',')
            fields = [field.strip() for field in fields]

            # Name & Vorname
            name, vorname = parse_name(fields[0].split(' '))
            if not any([name, vorname]):
                continue
            contact.name = name
            contact.vorname = vorname

            # Titel
            if len(fields) >= 2:
                text = fields[1]
                if text in municipalities:
                    contact.adresse = text
                elif is_title(text):
                    contact.beruf = appended_text(contact.beruf, text)

                if len(fields) >= 3:
                    text = fields[2]
                    if text in municipalities:
                        contact.adresse = text

            contacts.append(contact)

    return contacts


def parse_layout14(table):
    # PERSON: Funktion > Name Vorname, Jg., Titel > Eintritt
    contacts = []
    for row in table.findChildren('tr'):
        cells = row.findChildren('td')
        if len(cells) > 1:
            contact = Contact()

            fields = strip(cells[1].contents).split(',')
            fields = [field.strip() for field in fields]

            # Name & Vorname
            name, vorname = parse_name(fields[0].split(' '))
            contact.name = name
            contact.vorname = vorname

            # Jahrgang
            if len(fields) >= 2:
                index = 2
                try:
                    contact.jahrgang = str(int(fields[1]))
                except ValueError:
                    index = 1

                if index < len(fields):
                    contact.beruf = fields[index]
            contacts.append(contact)

    return contacts


def parse_layout16(table):
    # PERSON: Funktion > Name, Jg., Beruf > Partei > Eintritt
    # Same as 14 except one more row
    contacts = []
    for row in table.findChildren('tr'):
        cells = row.findChildren('td')
        if len(cells) > 1:
            contact = Contact()

            fields = strip(cells[1].contents).split(',')
            fields = [field.strip() for field in fields]

            # Name & Vorname
            name, vorname = parse_name(fields[0].split(' '))
            contact.name = name
            contact.vorname = vorname

            # Jahrgang
            if len(fields) >= 2:
                index = 2
                try:
                    contact.jahrgang = str(int(fields[1]))
                except ValueError:
                    index = 1

                if index < len(fields):
                    contact.beruf = fields[index]

            if len(cells) > 2:
                contact.partei = strip(cells[2].contents)

            contacts.append(contact)

    return contacts


def merge_contacts(contacts):
    """ Merge two or more contacts to one.
    Returns None if not mergable"""
    merged = Contact()
    mergable = True
    for field in vars(contacts[0]).keys():
        if field == 'asterisk':
            continue
        # Get all possible values which are not empty
        attrs = [getattr(contact, field) for contact in contacts]
        values = list(set(attrs) - set(['', u'', None]))
        if len(values) > 1:
            mergable = False
            break
        elif len(values) == 1:
            setattr(merged, field, values[0])
    return merged if mergable else None


def process_contacts(contacts):
    """ Finds duplicates, merges contacts etc. """
    # Remove duplicates
    dic = {str(contact): contact for contact in contacts}
    contacts = list(dic.values())

    # Merge contacts
    dic = {}
    for contact in contacts:
        key = contact.name + contact.vorname
        if key not in dic:
            dic[key] = []
        dic[key].append(contact)

    contacts = []
    for key, value in dic.iteritems():
        if len(value) == 1:
            contacts.append(value[0])
        else:
            merged = merge_contacts(value)
            if merged:
                contacts.append(merged)
            else:
                contacts.extend(value)

    # Move title away from prefession
    for contact in contacts:
        if is_title(contact.beruf):
            contact.titel = contact.beruf
            contact.beruf = ''

    # Sort
    contacts = sorted(contacts, key=lambda contact: str(contact))

    return contacts


def main():
    # Get all tables containing addresses
    tables = get_all_person_tables()

    # Store them for inspection
    for layout in tables.keys():
        with open('people/%s.html' % layout, 'w') as file:
            for table in tables[layout]:
                file.write(str(table[0]))

    # Parse all tables
    contacts = []

    for table in tables['layout3']:
        contacts.extend(parse_layout3(table[0]))

    for table in tables['layout5']:
        contacts.extend(parse_layout5(table[0]))

    for table in tables['layout9']:
        contacts.extend(parse_layout9(table[0]))

    for table in tables['layout10']:
        contacts.extend(parse_layout10(table[0]))

    for table in tables['layout11']:
        contacts.extend(parse_layout11(table[0]))

    for table in tables['layout13']:
        contacts.extend(parse_layout13(table[0]))

    for table in tables['layout14']:
        contacts.extend(parse_layout14(table[0]))

    for table in tables['layout16']:
        contacts.extend(parse_layout16(table[0]))

    contacts = process_contacts(contacts)

    # Export to csv
    with open('contacts.csv', 'w') as file:
        file.write((
            'Name,Vorname,Politische Partei,Jahrgang,Akademischer Titel,Beruf,'
            'Adresse,Telefon,Direktnummer\n'
        ))
        for contact in contacts:
            line = '%s,%s,%s,%s,%s,%s,%s,%s,%s\n' % (
                contact.name, contact.vorname, contact.partei,
                contact.jahrgang, contact.titel, contact.beruf,
                contact.adresse, contact.nummer, contact.direkt_nr
            )
            file.write(line.encode('utf8'))

if __name__ == '__main__':
    main()
