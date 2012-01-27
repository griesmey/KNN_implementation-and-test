import os
import sys
import MySQLdb
import shutil


def get_user_rat(userid_):
    '''
    returns a dict
    songid -> rating
    example:
    {
    4h3bfnff : 1,
    54483hfuUo : 0,
    fh3kn_fk : 0,
    ...
    ...
    }
    '''
    try:
        sqlstring_pos = """select v.id from youtube_video v, \
         user_rating u where v.video_id = u.video_id and \
         u.userid = '""" + userid_.strip() + """' and u.rating = 1"""
        sqlstring_neg = """select v.id from youtube_video v,\
         user_rating u where v.video_id = u.video_id and\
         u.userid = '""" + userid_.strip() + """' and u.rating = -1"""
        # print(sqlstring_pos)
        # print(sqlstring_neg)
        db = MySQLdb.connect(host = 'matrix.cs.fsu.edu',
                             user = 'smartplayer',
                             passwd = 'smartplayer123',
                             db = 'SmartPlayer')
        c = db.cursor()
        c.execute(sqlstring_pos)
        pos = c.fetchall()

        c.close()
        d = db.cursor()
        d.execute(sqlstring_neg)
        neg = d.fetchall()
        d.close()

    except:
        print("SQL EXCEPTION: sql except")

    ret_d = dict()
    for song in pos:
        ret_d[song[0]] = 1
    for song in neg:
        ret_d[song[0]] = 0
    return ret_d

if __name__ == "__main__":
    D = dict()
    D = get_user_rat('chaity')
    print(D)
