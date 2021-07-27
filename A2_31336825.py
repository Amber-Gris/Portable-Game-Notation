#!/usr/bin/env python
# coding: utf-8

# In[14]:


class PgnHandler:
    """
    3.2 filtering the game data
    remove metadata
    remove the gama result
    extract a list containing each game as a clean string
    write the game string in a file
    """
    def __init__(self, file_path):
        """
        file_path is the path of the file to be processed
        file_content is used to hold the content of the entire file
        cleaned_content_list is used to save the move information of each game
        """
        self.file_path = file_path
        self.file_content = ''
        self.cleaned_content_list = []
        
    def get_file_path(self):
        return self.file_path
    
    def set_file_path(self, file_path):
        self.file_path = file_path
        
    def get_file_content(self):
        return self.file_content
    
    def get_cleaned_content_list(self):
        return self.cleaned_content_list
    
    def read_file(self):   
        """
        read the entire file
        use the file_content to record the file content
        """
        try:
            file_handler = open(self.file_path, 'r', encoding = 'ISO-8859-1')
            self.file_content = file_handler.read()
        except IOError:
            print('The file_path is invalid')
            return None
        else:
            file_handler.close()
        finally:
            print('The file reading is done')
            
    def remove_meta_data(self):
        """
        Separate mata data and move information first
        then remove the result at the end of each move information
        put the extracted clean string into the cleaned_content_list
        """
        # four possible results
        results = ['1-0', '0-1', '1/2-1/2', '*']
        # split mata data and move information with \n\n
        for element in self.file_content.split('\n\n'):
            # remove meta data(starts with '[') and null character string
            if not element.replace('\n', '').startswith('[') and element.strip() != '':
                # remove the result
                for the_result in results:
                    element = element.replace(the_result, '')
                # remove previously interspersed \n
                element = element.replace('\n', '')
                # add \n after every element
                element += '\n'
                self.cleaned_content_list.append(element)
        # remove the last \n
        self.cleaned_content_list[-1] = self.cleaned_content_list[-1].replace('\n', '')
        
    def write_file(self, file_path):
        """
        sse the file_path parameter to pass in the specified file path
        write the content of the cleaned_content_list to the file of the specified path
        
        """
        try:
            file_handler = open(file_path, 'w')
            file_handler.writelines(self.cleaned_content_list)
        except IOError:
            print('The file_path is invalid')
        else:
            file_handler.close()
        finally:
            print('The file writing is done')


# In[15]:


class GameStringHandler:
    """
    3.3 sub files
    get the move informaton from the game_string.txt file    
    divide the move information of white and black of each game and put them into different files    
    """
    def __init__(self, file_path):
        """
        file_path is the path of the file to be processed
        file_content_list is used to keep the content readed from specified file 
        """
        self.file_path = file_path
        self.file_content_list = []
        
    def get_file_path(self):
        return self.file_path
    
    def set_file_path(self, file_path):
        self.file_path = file_path
    
    def get_file_content_list(self):
        return self.file_content_list
    
    def read_file(self):
        """
        open the file in the specified path in read mode
        put the content which readed into the file_content_list
        """
        try:
            file_handler = open(self.file_path, 'r')
            self.file_content_list = file_handler.readlines()
        except IOError:
            print('The file_path is invalid')
            return None
        else:
            file_handler.close()
        finally:
            print('The file reading is done')
    
    def divide_files(self):
        """
        put the move information of white and black of each game into different files
        create a sub_file folder to save these files
        """
        # game_index is the index of each game
        for game_index in range(1,len(self.file_content_list)+1):
            # game_str keep the total move information of each game
            game_str = self.file_content_list[game_index-1]
            # set file name, save these files to sub_file
            filename_w = './sub_file/' + str(game_index) + 'w'
            filename_b = './sub_file/' + str(game_index) + 'b'
            # open files in write mode
            file_handler_w = open(filename_w, 'w')
            file_handler_b = open(filename_b, 'w')        
            # remove \n
            game_str = game_str.replace('\n', '')
            # divide by dot notation and remove the '1'
            moving_list = game_str.split('.')[1:]
            for each_move in moving_list:
                # divide each part by space 
                each_move = each_move.split(' ')
                # output the black and white of each game to the file respectively 
                file_handler_w.write(each_move[0] + '\n')
                file_handler_b.write(each_move[1] + '\n')
            file_handler_w.close()
            file_handler_b.close()


# In[16]:


import pandas as pd

def get_first_move_list():
    """
    read each file in turn according to the game_index
    get the first move of each game from each file
    """
    first_move_w = []
    first_move_b = []
    # 1 is the index of first game, 2111 is the index of last game plus 1
    for game_index in range(1,2111):
        #filename
        filename_w = './sub_file/' + str(game_index) + 'w'
        filename_b = './sub_file/' + str(game_index) + 'b'
        # open files
        file_handler_w = open(filename_w, 'r')
        file_handler_b = open(filename_b, 'r')
        # get the first move
        move_w_content = file_handler_w.readlines()[0]
        move_b_content = file_handler_b.readlines()[0]
        # handle special situations that one side surrenders at the beginning
        if move_w_content.strip() != '':
             first_move_w.append(move_w_content)
        if move_b_content.strip() != '':
             first_move_b.append(move_b_content)
    return first_move_w, first_move_b

def get_first_move_dict(first_move_w_list, first_move_b_list):
    """
    use first_move_w_list and first_move_b_list to generate two dicts respectively
    key represents where to move
    value represents how many times this move presents in the first step in these games 
    """
    # create two empty dicts
    first_move_w_dict = {}
    first_move_b_dict = {}
    # put the first move of white in the first_move_w_dict
    for move in first_move_w_list:
        if move in first_move_w_dict:
            first_move_w_dict[move] += 1
        else:
            first_move_w_dict[move] = 1
            
    for move in first_move_b_list:
        if move in first_move_b_dict:
            first_move_b_dict[move] += 1
        else:
            first_move_b_dict[move] = 1
    return first_move_w_dict, first_move_b_dict

def get_first_move_dataframe():
    """
    use first_move_w_dict and first_move_b_dict to make two dataframes 
    returns these two dataframes as a tuple
    """
    # get two first move lists
    first_move_w_list, first_move_b_list = get_first_move_list()
    # get two first move dicts
    first_move_w_dict, first_move_b_dict = get_first_move_dict(first_move_w_list, first_move_b_list)
    # create dataframe from the dict
    first_move_w_dataframe = pd.DataFrame.from_dict(first_move_w_dict, orient = 'index', columns = ['count'])
    first_move_b_dataframe = pd.DataFrame.from_dict(first_move_b_dict, orient = 'index', columns = ['count'])
    return first_move_w_dataframe, first_move_b_dataframe


# In[21]:


import matplotlib.pyplot as plt
import pandas as pd

def plot_the_result():
    """
    3.5 Plotting
    use two dataframes to generate a bar graph which contains the ten most common first moves
    """
    # get two dataframes
    first_move_w_dataframe, first_move_b_dataframe = get_first_move_dataframe()
    # add the player column to distinguish white and black
    first_move_w_dataframe['player'] = 'w'
    first_move_b_dataframe['player'] = 'b'
    # concat two dataframes
    total_df = pd.concat([first_move_w_dataframe, first_move_b_dataframe])
    # sort total dataframe by count
    total_df.sort_values(by = 'count', inplace = True, ascending = False)
    # reset the index
    total_df.reset_index(inplace = True)
    # get the first ten elements
    total_df = total_df[:10]
    # if the player is white, put the value of the count column into the count_w column
    total_df['count_w'] = total_df['count'][total_df.player == 'w']
    # if the player is black, put the value of the count column into the count_b column
    total_df['count_b'] = total_df['count'][total_df.player == 'b']
    # generate the bar graph
    total_df.plot.bar(x = 'index', y = ['count_w', 'count_b'], title = 'first_moves')
    # show the graph
    plt.show() 


# In[22]:


if __name__ == '__main__':
    # 3.2 filtering the game data
    pgn_file_handler = PgnHandler('chess_game.pgn')
    pgn_file_handler.read_file()
    pgn_file_handler.remove_meta_data()
    pgn_file_handler.write_file('game_string.txt')
    # 3.3 sub files
    game_string_handler = GameStringHandler('./game_string.txt')    
    game_string_handler.read_file()
    game_string_handler.divide_files()
    # 3.4 Dataframe counts
    first_move_w_dataframe, first_move_b_dataframe = get_first_move_dataframe()
    # 3.5 Plotting 
    plot_the_result()


# In[ ]:


"""
The probability that the first move of white is d4 or e4 is very high.
The probability that the first move of black is Nf6 or c5 is very high.
"""

