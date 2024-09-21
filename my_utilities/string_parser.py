import parse

class StringParser:

    formats = None

    @classmethod
    def set_formats(cls, fmts):
        if type(fmts) is list:
            cls.formats = fmts
        else:
            cls.formats = [fmts]
    
    @classmethod
    def add_formats(cls, fmts):
        if cls.formats == None:
            cls.formats = []
        if not (type(fmts) is list):
            fmts = [fmts]
        cls.formats += fmts
    
    @classmethod
    def get_formats(cls):
        return cls.formats
    
    @classmethod
    def sort_formats(cls):
        cls.formats = sorted(cls.formats, reverse=True, key=lambda fmt: len(fmt))

    @staticmethod
    def parse(str):
        if StringParser.formats == None:
            raise Exception('No format(s) given to the Parser')
        for f in StringParser.formats:
            parsed_data = parse.parse(f, str)
            if parsed_data != None:
                return parsed_data.named
        return None
    
    @staticmethod
    def format(data):
        if StringParser.formats == None:
            raise Exception('No format(s) given to the Parser')
        for f in reversed(StringParser.formats):
            try:
                str = f.format(**data)
                return str
            except KeyError:
                pass
        return None
    
    @staticmethod
    def to_cc(str):
        if ' ' not in str:
            return str
        parts = [ p for p in str.lower().split(" ") if p != '' ]
        for i in range(len(parts)):
            part = parts[i]
            parts[i] = part[:1].upper() + part[1:]
        return ''.join(parts)
    
    @staticmethod
    def from_cc(str):
        chars = []
        for c in list(str):
            if c.isupper():
                chars.append(' ')
            chars.append(c)
        return ''.join(chars)
    
    @staticmethod
    def is_date(str):
        for c in '.-_':
            str = str.replace(c, '')
        return str.isnumeric()



if __name__ == '__main__':

    format = "{sort_performer} - {studio} - [{year:d}] [{line}] {title} ({mention_performer}) [{other_info}]"

    #formats = generate_string_variations(['{sort_performer} - {studio} - ', '[{year:d}]', '[{line}]', '{title}', '({mention_performer})', '[{other_info}]'], optinal=(1,2,4,5))
    #for f in formats:
    #    print(f)
    
    a = 0b0101
    print(a)
    print( 1 << 2 )
    print("{:b}".format( 0b0111 & 0b0101 ))


