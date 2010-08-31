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
'''Provides nautilus menu entries to launch meld from nautilus'''
import os
import nautilus
import urllib

from os import path

class BeyondMeld(nautilus.MenuProvider):
    '''
    This class provides the menu entries in nautilus to compare files with meld.
    '''

    def __init__(self):
        """
        Init method
        """
        self.data_path = path.join(os.environ["HOME"], '.nautilus/BeyondMeld/LeftSide')
        self.comparer_command = '/usr/bin/meld {0} {1}'
        self.left_side = LeftSideItem()
        
    def _get_path_from_url(self, url):
        '''
        Converts the given url to a path
        '''
        return urllib.unquote(url[7:])

    def compare_each_other_cb(self, menu, url1, url2):
        '''
        Callback function for the "compare with each other menu entry".
        Converts the selected urls to paths and passes them to meld.
        path1 -- the url of the first selected element for comparision.
        path2 -- the url of the second selected element for comparision.
        '''
        l_path1 = self._get_path_from_url(url1)
        l_path2 = self._get_path_from_url(url2)
        os.system(self.comparer_command.format(l_path1, l_path2))
        
    def select_left_side_cb(self, menu, url):
        pass

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
                item.connect('activate', self.compare_each_other_cb, files[0].get_uri(), files[1].get_uri())

                return item,
        # Single file or directory selection
        if len(files) == 1:
            if not self.left_side.exists():
                item = nautilus.MenuItem('BeyondMeld::select_left_side', 'Select Left Side To compare...', 'Grabs the selected item for comparision')
                item.connect('activate', self.select_left_side_cb, files[0].get_uri())
                
                return item,
            else:
                if (self.left_side.type() == 'folder' and files[0].is_directory()) or (self.left_side.type() == 'file' and not files[0].is_directory()):
                    pass
            

class LeftSideItem(object):
    '''
    Obtains info about the left side selected item for comparing.
    '''
    def __init__(self):
        '''
        Class initialization.
        '''
        pass
    
    def exists(self):
        '''
        Returns if there are a previously selected item for comparision. 
        '''
        return False
    
    def type(self):    
        '''
        Returns the type of the selected left side item (file|folder).
        '''
        return ''
    
    def path(self):
        '''
        Returns the path of the selected left side item.
        '''
        return ''
        
    def get_name(self):
        '''
        Returns the name of the file or folder selected in the left side.
        '''
        return ''
