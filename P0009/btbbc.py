#
# btbbc.py
# Created by Hexapetalous on Feb 3, 2016.
#
# This is a part of P0009.
# `btbbc` means 'BTBB with Classes.'
#
# Copyright (c) 2016 Hexapetalous. All rights reserved.
#
import P0009.btbb as btbb


class Floors(object):
    def __init__(self, url):
        super(Floors, self).__init__()
        self.tid = btbb.get_tid_from_url(url)
        self.floors = []
        raw_floors = btbb.get_all_floors(url)
        for raw_floor in raw_floors:
            self.floors.append(Floor(raw_floor))

    def valuable(self):
        return self.floors != []

    def get_floors(self):
        return self.floors


class Floor(object):
    def __init__(self, raw_floor):
        super(Floor, self).__init__()
        self.content = btbb.floor_get_content(raw_floor)
        self.floor_index = btbb.floor_get_floor_number(raw_floor)
        self.post_id = btbb.floor_get_post_id(raw_floor)


class FloorInFloors(object):
    """
    All the comments in a post.
    """
    def __init__(self, floors):
        super(FloorInFloors, self).__init__()
        self.tid = floors.tid
        self.floor_in_floors = btbb.get_floor_in_floors(self.tid, -1)

    def get_comments(self):
        result = []
        for fif in self.floor_in_floors:
            result.append(Comments(fif))
        return result


class Comments(object):
    """
    All the comments in a floor.
    """
    def __init__(self, floor_in_floor):
        super(Comments, self).__init__()
        raw_comments = btbb.comments_get_comments(floor_in_floor)
        self.post_id = btbb.comment_get_post_id(raw_comments[0])
        self.comments = []
        for rc in raw_comments:
            self.comments.append(Comment(rc))


class Comment(object):
    def __init__(self, raw_comment):
        super(Comment, self).__init__()
        self.content = btbb.comment_get_content(raw_comment)


class Post(object):
    def __init__(self, url):
        super(Post, self).__init__()
        # This is a design mistake.
        self.new_real_floors = []
        floors = Floors(url)
        if not floors.valuable():
            print('*_*')
            pass
        self.floor_list = floors.get_floors()
        self.floor_in_floors = FloorInFloors(floors).get_comments()
        self.real_floors = []

    def match(self):
        for floor in self.floor_list:
            real_floor = [floor, None]
            pid = floor.post_id
            for comments in self.floor_in_floors:
                if comments.post_id == pid:  # Found!
                    real_floor[1] = comments
                    break
            self.real_floors.append(real_floor)

    def migration(self):
        for rf in self.real_floors:
            nrf = {'floor': rf[0], 'comments': None}
            if rf[1] is not None:
                nrf['comments'] = rf[1].comments
            self.new_real_floors.append(nrf)
        self.new_real_floors.sort(key=lambda n: n['floor'].floor_index)

    def get_real_floors(self):
        return self.new_real_floors
