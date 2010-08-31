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

    def compare_each_other_cb(self, menu, path1, path2):
        '''
        Callback function for the compare with each other menu entry.
        Converts the selected urls to paths and passes them to meld.
        @path1 the url of the fisrst selected element for comparision.
        @path2 the url of the second selected element for comparision.
        '''
        l_path1 = urllib.unquote(path1[7:])
        l_path2 = urllib.unquote(path2[7:])
        os.system(self.comparer_command.format(l_path1, l_path2))
        
    def select_left_side_cb(self, menu, url):
        pass

    def get_file_items(self, window, files):
        '''
        Shows the corresponding menu items to launch the comparision.
        '''
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