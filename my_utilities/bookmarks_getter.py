import os
import json
import datetime


'''
v1.0
Supported browsers:
- Brave
- Chrome
'''
class BookmarksGetter:

    default_bookmarks_paths = [
        r'%localappdata%\Google\Chrome\User Data\Default\Bookmarks',
        r'%localappdata%\BraveSoftware\Brave-Browser\User Data\Default\Bookmarks',
    ]

    @classmethod
    def get_bookmarks(cls, browser, foldername=None, domain=None, sortby=None, reverse=False):
        bookmarks_path = next( (pth for pth in cls.default_bookmarks_paths if (browser.lower() in pth.lower() )) , None)
        if bookmarks_path == None:
            print('Cannot find bookmarks for browser named "{}"'.format(browser))
            return
        bookmarks_path = bookmarks_path.replace(r'%localappdata%', os.getenv('LOCALAPPDATA'))
        with open(bookmarks_path, 'r') as f:
            bookmarks_json = json.load(f)
        if browser.lower() in 'chrome chromium bravesoftware edge':
            bookmarks = cls._get_bookmarks_Chrome(bookmarks_json, foldername=foldername, domain=domain)
        else:
            print('ERROR: "{}" is in an unknown browser family'.format(browser))
            return []
        bookmarks = [ b for b in bookmarks if (foldername==None or foldername in b.get('location')) ]
        bookmarks = [ b for b in bookmarks if (domain==None or domain.lower() in b.get('url').lower()) ]
        if sortby:
            bookmarks.sort( key=lambda bk: bk.get(sortby), reverse=reverse )
        return bookmarks

    @classmethod
    def _get_bookmarks_Chrome(cls, bookmarks_json, foldername=None, domain=None):
        base_objects = bookmarks_json['roots']['bookmark_bar'].get('children')
        return cls._get_bookmarks_as_list_Chrome(base_objects)
    
    @classmethod
    def _get_bookmarks_as_list_Chrome(cls, array, location=None):
        bookmarks = []
        for obj in array:
            if obj.get('type') == 'url':
                obj['location'] = location if location else ''
                obj['date_added_fmt'] = cls.windows_epoch_readable(obj['date_added'])
                obj['date_last_used_fmt'] = cls.windows_epoch_readable(obj['date_last_used'])
                if obj.get('date_modified'):
                    obj['date_modified_fmt'] = cls.windows_epoch_readable(obj['date_modified'])
                bookmarks.append(obj)
            elif obj.get('type') == 'folder':
                name = obj.get('name')
                children = obj.get('children')
                new_location = f'{location}/{name}' if location else name
                bookmarks.extend(cls._get_bookmarks_as_list_Chrome(children, new_location))
        return bookmarks


    ### HELPER METHODS
    @classmethod
    def windows_epoch_readable(cls, us):
        windows_epoch_start = datetime.datetime(1601, 1, 1)
        return str(windows_epoch_start + datetime.timedelta(microseconds=int(us)))