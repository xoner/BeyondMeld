#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
# Author: David Pascual Rocher
# Contact: dapasroc@gmail.com

'''Provides nautilus menu entries to launch meld from nautilus'''
import os
import nautilus
import urllib
import json
import re

from os import path

def _get_path_from_url(url):
    '''
    Converts the given url to a path
    @param url the url to be converted
    @type url string
    @returns the corresponding path to the given url
    @rtype string
    '''
    return urllib.unquote(url[7:])

class BeyondMeld(nautilus.MenuProvider):
    '''
    This class provides the menu entries in nautilus to compare files with meld.
    '''

    def __init__(self):
        """
        Init method
        """
        self.data_path = path.join(os.environ["HOME"], '.nautilus/BeyondMeld/LeftSide')
        self.comparer_command = '/usr/bin/meld {0} {1}&'
        self.left_side = LeftSideItem(self.data_path)
        
        # bakcend initialization.
        directory_location = path.split(self.data_path)[0]
        if not path.exists(directory_location):
            os.mkdir(directory_location)

    def compare_each_other_cb(self, menu, path1, path2):
        '''
        Callback function for the "compare with each other menu entry".
        Converts the selected urls to paths and passes them to meld.
        @param path1 the path of the first selected element for comparision.
        @type path1 string
        @param path2 the path of the second selected element for comparision.
        @type path2 string
        '''
        if self.left_side.exists():
            self.left_side.cleanup()
            self.left_side = LeftSideItem(self.data_path)
        
        os.system(self.comparer_command.format(path1, path2))

      
    def select_left_side_cb(self, menu, url):
        '''
        Callback function for the "Select left side".
        Stores the path in url as the left side for comparision.
        @param url the url of the left side item to be compared.
        '''
        l_path = _get_path_from_url(url)
        self.left_side.select_left_path(l_path)

    def get_file_items(self, window, files):
        '''
        Shows the corresponding menu items to launch the comparision.
        '''
        # More than two files/folders selected not supported. 
        if len(files) > 2:
            return
        
        # Two folders or files comparision.
        if len(files) == 2:
            if (files[0].is_directory() and files[1].is_directory()) or (not files[0].is_directory() and not files[1].is_directory()):
                item = nautilus.MenuItem('BeyondMeld::compare_each_other_dirs', 'Compare Each Other...', 'Compare the selected items one with another')
                l_path1 = _get_path_from_url(files[0].get_uri())
                l_path2 = _get_path_from_url(files[1].get_uri()) 
                item.connect('activate', self.compare_each_other_cb, l_path1, l_path2)

                return item,
        # Single file or directory selection
        if len(files) == 1:
            items = []
            items.append(nautilus.MenuItem('BeyondMeld::select_left_side',
                        'Select Left Side To compare...',
                        'Grabs the selected item for comparision'))
            items[0].connect('activate', self.select_left_side_cb, files[0].get_uri())
                
            if self.left_side.exists():
                if (self.left_side.type() == 'folder' and files[0].is_directory()) or (self.left_side.type() == 'file' and not files[0].is_directory()):
                    items.append(nautilus.MenuItem('BeyondMeld::compare_with',
                     'Compare with "' + self.left_side.get_name() + '"',
                     'Compares the selected item with the selected item as the left side'))
                    
                    l_path = _get_path_from_url(files[0].get_uri())
                    items[len(items) - 1].connect('activate', self.compare_each_other_cb, self.left_side.path(), l_path)
            return items

class LeftSideItem(object):
    '''
    Obtains info about the left side selected item for comparing.
    '''
    def __init__(self, conf_path):
        '''
        Class initialization.
        '''
        # Create the config file if not exists.
        if not path.exists(conf_path):
            with open(conf_path, 'w') as l_file:       
                l_file.write('')
                l_file.close()
        
        # Initialize variables.
        self.data_path = conf_path
        self.left_side = {}
        
        # Read the stored left side item if any
        if path.exists(self.data_path):
            file_content = open(self.data_path).read()
            if len(file_content) != 0:
                try:
                    self.left_side = json.loads(file_content)
                except:
                    self.left_side = {}
    
    def exists(self):
        '''
        Returns if there are any previously selected item for comparision. 
        '''
        try:
            if re.match("(file|folder)", self.left_side["type"]) and path.exists(self.left_side["path"]): 
                return True
        except:
            return False
        
        return False
    
    def type(self):    
        '''
        Returns the type of the selected left side item (file|folder).
        '''
        try:
            return self.left_side["type"]
        except:
            return 'None'
    
    def path(self):
        '''
        Returns the path of the selected left side item.
        '''
        try:
            return self.left_side["path"]
        except:
            return 'None'
        
    def get_name(self):
        '''
        Returns the name of the file or folder selected in the left side.
        '''
        return path.split(self.left_side["path"])[1]
    
    def select_left_path(self, item_path):
        '''
        Stores the selected file/folder in path as the left side item for comparision.
        '''
        self.left_side = {}
        if path.exists(item_path):
            self.left_side["type"] = 'file' if path.isfile(item_path) else 'folder'
            self.left_side["path"] = item_path
        try:
            with open(self.data_path, "w") as l_file:
                l_file.write(json.dumps(self.left_side))
        except:
            pass
    
    def cleanup(self):
        '''
        Cleans the selected right side.
        '''
        os.remove(self.data_path)
        
        self.left_side = {}