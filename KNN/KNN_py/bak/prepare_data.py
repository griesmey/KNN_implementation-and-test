"""
Prepare the data for running the KNN classifier and recommender

"""
import os
import get_data
import sys

DATADIR_ = '/home/tathagata/SmartPlayerModules/Audio/\
audiomodules/KNN/KNN/KNN_py/data/'


def create_mf(userid_, querysongs_, dir_):
    """
    userid_ - userid for user in smartplayer database
    querysongs_ - list of song(s) that need ratings
    dir - dir is a directory that contains all of the songs/videos
          in .wav format

    Create mf file that contain these songs with either
    a like or a dislike with them.
    This what an mf file should look like:

    /User/Rob/files/rap1.wav    1
    /User/Rob/files/rap2.wav    1
    /User/Rob/files/rap3.wav    1
    /User/Rob/files/rap4.wav    0

    Returns - name of file written to
    """
    new_filename = userid_ + '.mf'
    if dir_.endswith('/') == False:
        dir_ += '/'
    mffile_ = open(new_filename, 'w')

    """
    query database for all songs that the user liked or
    disliked and put then in a list
    """

    D_videos = get_data.get_user_rat(userid_)
    for song in querysongs_:
        songpath = dir_ + song + '.wav'
        if os.path.isfile(songpath):
            mffile_.write(songpath + '\t0\n')
            D_videos[song] = 0  # test song has rating 0
    for song, rating in D_videos.iteritems():
        if song in querysongs_: # don't include test songs 
            continue
        songpath = dir_ + song + '.wav'
        if os.path.isfile(songpath):
            mffile_.write(songpath + '\t' + str(rating) + '\n')

    return new_filename, D_videos


def create_arff(pathtofile_):
    """
    userid_
    dir_ - dir that contains the mf file created
    by this program

    returns str containing name of new file
    """
    sys.path.append(
        '/home/tathagata/SmartPlayerModules/Audio/audiomodules/generator')
    import coeffGenerator
    arff = coeffGenerator.create_mfccs(pathtofile_)
    coeffGenerator.create_genre_coeffs(arff)


    return 'stacked_' + arff


def format_arff(pathtofile_, ratings_dict):
    """
    creates new arff file that contains genre coefficients
    and the ratings for each file
    """
    newfile_ = 'knn_' + pathtofile_
    file_p = open(newfile_, 'w')
    cursong_ = ''
    for line in open(pathtofile_):
        if line.startswith('%'):
            cursong_ = line.split('/')[-1].replace('.wav\n', '')
            file_p.write(line)
        elif line[0].isdigit():
            temp = line.split(',')
            temp[-1] = str(ratings_dict[cursong_])
            for i in temp:
                if(i == temp[-1]):
                    file_p.write(i + '\n')
                else:
                    file_p.write(i + ',')
        else:
            file_p.write(line)

    return newfile_


def run(userid_, videos_):
    """
    userid_  - username from smartplayer database
    videos_ - list of videos to rate
    Return: returns name of the knn arff file to be
    used in C++ program parameters
    """
    song_d = dict()
    name = ''
    genrename_ = ''
    Loc = '/home/tathagata/UserVideoDownloads/tathagata_vdos/video_downloads/'
    old = os.getcwd()
    os.chdir(DATADIR_)
    name, song_d = create_mf(userid_, videos_, Loc)
    genrename_ = create_arff(name)
    knn_file = format_arff(genrename_, song_d)
    os.chdir(old)
    return DATADIR_ + knn_file

if __name__ == "__main__":
    L = []
    name = ''
    D = dict()
    L.append('ZYqSiNf1T_U')
    L.append('zTl3fGeKgjU')
    L.append('ZoSVZ7tXbxo')
    L.append('ZnTCLQWAs8k')
    L.append('ZmsAKIpE12o')
    L.append('Zjb5o2EbPpY')
    Loc = '/home/tathagata/UserVideoDownloads/tathagata_vdos/video_downloads/'
    user = 'tathagata'
    knn_file = ''
    name, D = create_mf(user, L, Loc)
    genrename_ = create_arff(name)
    knn_file = format_arff(genrename_, D)
    print(knn_file)
