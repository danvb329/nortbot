# -*- coding: utf-8 -*-

"""
The MIT License (MIT)

Copyright (c) 2019 Nortxort

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""

import time


class PlayList:
    """ Class to do various playlist operation with.

    TODO: Implement playlist delay?
    """

    def __init__(self):
        self.track_list = []
        self.track_index = 0
        self.current_track = None
        self.is_paused = False

    @property
    def track(self):
        """
        Returns the current track in the track list.

        :return: The current Track or None if no track is being timed.
        :rtype: Track | None
        """
        return self.current_track

    @property
    def current_index(self):
        """
        Return the current track list index.

        :return: The current index of the track list.
        :rtype: int
        """
        return self.track_index

    @property
    def last_index(self):
        """
        Return the last index of the track list.

        :return: The last index in the track list.
        :rtype: int
        """
        if len(self.track_list) == 0:
            return 0
        else:
            return len(self.track_list) - 1

    @property
    def has_active_track(self):
        """
        Check if the track list has a active track based on time and pause state.

        :return: True if active else False.
        :rtype: bool
        """
        if self.is_paused:
            return True
        if self.elapsed == 0:
            return False
        if self.elapsed > 0:
            return True
        return False

    @property
    def elapsed(self):
        """
        Returns the current track elapsed time.

        :return: The elapsed track time in seconds.
        :rtype: int | float
        """
        if self.current_track is not None:
            if self.is_paused:
                return self.current_track.pause
            elapsed = time.time() - self.current_track.start
            if elapsed > self.current_track.time:
                return 0
            return elapsed
        return 0

    @property
    def remaining(self):
        """
        Returns the current track remaining time.

        :return: The remaining time in seconds.
        :rtype: int | float
        """
        if self.current_track is not None:
            time_left = self.current_track.time - self.elapsed
            return time_left
        return 0

    @property
    def next_track(self):
        """
        Returns the next track in the track list

        :return: The next Track in the track list or None if the track list is empty.
        :rtype: Track | None
        """
        if len(self.track_list) > 0:
            if self.track_index <= len(self.track_list):  # self.last_index:
                next_track = self.track_list[self.track_index]
                self.current_track = next_track
                self.current_track.start = time.time()
                self.track_index += 1
                return next_track
            return None

    @property
    def is_last_track(self):
        """
        Check if the track list is at the last index.

        :return: True if last track list index, else False. None if the track list is empty.
        :rtype: bool | None
        """
        if len(self.track_list) > 0:
            if self.track_index >= len(self.track_list):
                return True
            return False
        return None

    @property
    def queue(self):
        """
        Return the queue of the track list.

        :return: The track list length and the remaining tracks.
        :rtype: tuple
        """
        if len(self.track_list) > 0:
            remaining = len(self.track_list) - self.track_index
            queue = (len(self.track_list), remaining)
            return queue

    def start(self, owner, track):
        """
        Start a track to be timed.

        :param owner: The nick of the user who started the track.
        :type owner: str
        :param track: The Track object.
        :type track: Track
        :return: The track as a Track.
        :rtype: Track
        """
        if self.is_paused:
            self.is_paused = False
        self.current_track = track
        self.current_track.owner = owner
        self.current_track.start = time.time()
        return self.current_track

    def play(self, offset):
        """
        Play or search a track.

        :param offset: The time in seconds to start playing from.
        :type offset: int | float
        :return: The remaining track time in seconds.
        :rtype: int | float
        """
        if self.is_paused:
            self.is_paused = False
        self.current_track.start = time.time() - offset
        return self.remaining

    def replay(self):  # TODO: check if this is working correct.
        """
        Replay(re-time) the current track.

        :return: The current track.
        :rtype: Track
        """
        if self.is_paused:
            self.is_paused = False
        self.current_track.start = time.time()
        return self.current_track

    def pause(self, offset=0):
        """
        Pause a track.

        :param offset: The time in seconds to pause the track at.
        :type offset: int | float
        """
        self.is_paused = True
        if offset != 0:
            self.current_track.pause = offset
        else:
            self.current_track.pause = time.time() - self.current_track.start

    def stop(self):
        """ Stop a track. """
        self.is_paused = False
        self.current_track.start = 0
        self.current_track.pause = 0

    def add(self, owner, track):
        """
        Add a track to the track list.

        :param owner: The nick name of the user adding the track.
        :type owner: str
        :param track: The Track object.
        :type track: Track
        :return: The track as Track.
        :rtype: Track
        """
        if track.id:
            track.owner = owner
            self.track_list.append(track)
            return track

    def add_list(self, owner, tracks):
        """
        Add a list of track data to the track list.

        :param owner: The nick name of the user adding the tracks.
        :type owner: str
        :param tracks: A list of Track objects.
        :type tracks: list
        """
        if len(tracks) > 0:
            for track in tracks:
                self.add(owner, track)

    def clear(self):
        """
        Clear the track list for all items.

        :return: True if cleared successfully, else False.
        :rtype: bool
        """
        if len(self.track_list) > 0:
            self.track_list[:] = []
            self.track_index = 0
            return True
        return False

    def get_tracks(self, amount=5, from_index=True):
        """
        Get a list of Track's from the track list.

        :param amount: The amount of Track's to get.
        :type amount: int
        :param from_index: Get Track's from the current track list index.
        :type from_index: bool
        :return: A list of Track objects.
        :rtype: list
        """
        start_index = 0
        result = []
        if len(self.track_list) > 0:
            if from_index:
                start_index = self.track_index
            ic = 0
            for i in range(start_index, len(self.track_list)):
                if ic <= amount - 1:
                    _track = (i, self.track_list[i])
                    result.append(_track)
                    ic += 1
        return result

    def next_track_info(self, jump=0):
        """
        Get the next Track object in the track list.

        :param jump: Instead of getting the next track, use this to jump in the track list.
        :type jump: int
        :return: The index of the Track and the Track.
        :rtype: tuple | None
        """
        if jump != 0:
            if self.track_index + jump < len(self.track_list):
                return self.track_index + jump, self.track_list[self.track_index + jump]
        elif self.track_index < len(self.track_list):
            return self.track_index, self.track_list[self.track_index]

    def delete(self, indexes, by_range=False):
        """
        Delete track list items by index.

        :param indexes: A list of indexes to delete.
        :type indexes: list
        :param by_range: Delete a range of indexes.
        :type by_range: bool
        :return: A dictionary containing information about the delete operation.
        :rtype: dict | None
        """
        tracks = list(self.track_list)
        deleted_indexes = []
        for i in sorted(indexes, reverse=True):
            if self.track_index <= i < len(self.track_list):
                del self.track_list[i]
                deleted_indexes.append(str(i))
        deleted_indexes.reverse()
        if len(deleted_indexes) > 0:
            _result = dict()
            if by_range:
                _result['from'] = deleted_indexes[0]
                _result['to'] = deleted_indexes[-1]
            elif len(deleted_indexes) == 1:
                _result['track_title'] = tracks[int(deleted_indexes[0])].title
            _result['deleted_indexes'] = deleted_indexes
            _result['deleted_indexes_len'] = len(deleted_indexes)
            return _result
        return None
