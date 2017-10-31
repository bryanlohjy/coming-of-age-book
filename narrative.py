import os
import random
import copy
import math

event_sequences = {
            'infancy': [ 'parents', 'playing'], # life, firsts, parents
            'childhood': [ 'kindergarten' ],  # kindergarten, learning, friends, parents
            'adolescence': [ 'school', 'prom', 'first_drink', 'party' ],  # highschool, parties, friends, romance
            'early_adult': [ 'moving_out', 'university', 'twenty_first', 'graduation', 'work' ], # independence, travel, graduation, early career
            'mid_adult': [ 'marriage', 'children' ], # settling down, career, marriage, children
            'late_adult': [ 'retirement', 'grandchildren', 'spouse_death', 'sickness' ] # retirement, grandchildren
        }

def get_image_map():
    image_map = {}
    base_path = 'temp/downloads/'
    for life_stage in os.listdir(base_path):
        image_map[life_stage] = { 'filler': [] }

        for item in os.listdir(base_path+life_stage):
            if os.path.isdir('{}{}/{}'.format(base_path, life_stage, item)): # if there is a folder of images
                image_map[life_stage][item] = [] # create an array of paths
                for folder_image in os.listdir('{}{}/{}'.format(base_path, life_stage, item)):
                    image_map[life_stage][item].append('{}{}/{}/{}'.format(base_path, life_stage, item, folder_image))

            else:
                image_map[life_stage]['filler'].append('{}{}/{}'.format(base_path, life_stage, item))
        
    return image_map

image_map = get_image_map()

def random_pop(arr):
    return arr.pop(random.randrange(len(arr)))

class Story:
    def __init__(self, num_pages):
        self.num_pages = num_pages
        self.events = self.init_events()
        print('Creating story...')
    def init_events(self):
        class Event:
            def __init__(self, name=None, index=None, life_stage=None, images=[], moment=None):
                self.name = name
                self.index = index
                self.life_stage = life_stage
                self.images = images
                self.moment = moment
        
        event_map = copy.deepcopy(event_sequences)
        events = []
        life_stages = list(event_sequences)
        life_map = copy.deepcopy(image_map)
        for i in range(self.num_pages):
            life_stage = ''
            images = []
            moment = None
            if i == 0:
                life_stage = 'birth'
                birth_image = random.choice(life_map['birth']['filler'])
                images.append(birth_image)
            elif i == self.num_pages - 1:
                life_stage = 'death'
            else:
                i = i - 1 
                mapped_index = math.floor((i / (self.num_pages - 2)) * len(life_stages))
                life_stage = life_stages[mapped_index]
                if len(event_map[life_stage]) > 0: # if there are events left to be added
                    moment = event_map[life_stage].pop(0) # pick next life event and remove from array
                    while len(images) < 5: # pick between 3 to 5 images
                        if len(life_map[life_stage][moment]) > 0: 
                            image = random_pop(life_map[life_stage][moment])
                        elif len(life_map[life_stage]['filler']) > 0: # if out of moment images, use filler
                            image = random_pop(life_map[life_stage]['filler']) 
                        else: # if out of filler images, break
                            break
                        images.append(image)
                    if len(life_map[life_stage][moment]) > 0:
                        life_map[life_stage]['filler'] = life_map[life_stage]['filler'] + life_map[life_stage][moment] # if there are pictures left in the life event, chuck them in the filler array
                else: # if generic page ( no event )
                    while len(images) < 5: # pick between 2 to 3 images
                        if len(life_map[life_stage]['filler']) > 0: # pick first from filler images
                            image = random_pop(life_map[life_stage]['filler'])
                        else: # if out of images to pick from, break
                            # print(life_stage, 'out of filler')
                            break
                        images.append(image)           

                i = i + 1

            event = Event(index=i, life_stage=life_stage, images=images, moment=moment)
            events.append(event)
        return events