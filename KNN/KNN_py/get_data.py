import os
import sys
import MySQLdb
import shutil


def get_user_rat(userid_, query_list):
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
    query_list: contains youtube_videos
    that need ratings
    '''
    try:
        sqlstring_pos = """select feat.genre from yt_song_feats feat, user_rating u,\
youtube_video v where v.videoid = u.videoid and v.ytid = feat.ytid and \
u.userid = '""" + userid_.strip() + """' and u.rating = 1"""
        sqlstring_neg = """select feat.genre from yt_song_feats feat, user_rating u,\
youtube_video v where v.videoid = u.videoid and v.ytid = feat.ytid and \
u.userid = '""" + userid_.strip() + """' and u.rating = -1"""
        
        #print(sqlstring_pos)
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
        
        e = db.cursor()
        ret_q = {}
        for song in query_list:
            e.execute("""select feat.genre from yt_song_feats feat where ytid = '\
""" + song + """'""")
            query = e.fetchall()

            ret_q[query[0][0]] = 0
        e.close()


    except Exception as e:
        print(e)


    ret_d = dict()
    for song in pos:
        ret_d[song[0]] = 1
    for song in neg:
        ret_d[song[0]] = 0
    return ret_d, ret_q

def create_testing_file(D_QUE):
    """
    @input:
    D_QUE - dict containing arff files and 0 rating(dummy value 
    not factored into computation)
    @output:
    file is created which is the testing arff file
    """
    return create_arff_file(D_QUE, 1)

def create_training_file(D_RAT):
    """
    D_RAT contains dict with key being the youtube_id
    and the value being the rating(either 0 or 1)
        example:
    {
    4h3bfnff : 1,
    54483hfuUo : 0,
    fh3kn_fk : 0,
    ...
    ...
    }
    """
    return create_arff_file(D_RAT, 0)
    
def create_arff_file(D_RAT, version):
    """
    @input: D_RAT
    
    D_RAT contains dict with key being the youtube_id
    and the value being the rating(either 0 or 1)
        example:
    {
    4h3bfnff : 1,
    54483hfuUo : 0,
    fh3kn_fk : 0,
    ...
    ...
    }
    version -
    version contains either 0 or 1
        0 is for training file
        1 is for testing file

    @output: training file
    """

    if(version == 0):
        filename_ = 'training.arff'
    elif(version == 1):
        filename_ = 'testing.arff'
    count = 0
    try:
        file_desc_ = open(filename_, 'w')
        
    except IOException as e:
        print(e)


    for a, b in D_RAT.iteritems():
        new_arff = append_rating(a, b)

        if(count != 0):
            new_arff = strip_attributes(new_arff)

        file_desc_.write(new_arff + '\n')
        count += 1

    file_desc_.close()
    return filename_

def strip_attributes(arff_file):
    """
    strip of out the @attribute portion of the arff file
    and return only the feature vector and filename portion 
    of the file
    @input:
    arff_file str
    @output
    arff_file str
    """
    start = arff_file.find('% filename')
    new_arff = arff_file[start:]
    return new_arff

def append_rating(arff, rating):
    """
    @input:
    arff - arff file string
    rating - either 0/1
    @output 
    new arff file with rating entered
    at end of feature vector
    """
    ret = ''
    ret = arff[:arff.find('% filename')]
    vector_part = arff[arff.find('% filename'):]
    
    vector = vector_part.split(',')
    vector[-1] = rating
    for i, item in enumerate(vector):
        if(i > len(vector) - 11):
            ret += ',' + str(item)
        else:
            ret += str(item)
        
    return ret


def run(username_, video_list_):
    """
    @input
    username_ - username of smartplayer user
    video_list_ - videos that you want recommended
    ratings on
    """
    D_RAT = dict()
    D_QUE = dict()  # query songs
    D_RAT, D_QUE = get_user_rat(username_, video_list_)
    f_train = create_training_file(D_RAT)
    f_test = create_testing_file(D_QUE)
    
    return f_train, f_test
    
if __name__ == "__main__":
    L = []
    L.append('ZYqSiNf1T_U')
    L.append('zTl3fGeKgjU')
    L.append('ZoSVZ7tXbxo')
    L.append('ZnTCLQWAs8k')
    L.append('ZmsAKIpE12o')
    L.append('Zjb5o2EbPpY')

    f_train, f_test = run('tathagata', L)
    print(f_train)
    print(f_test)
