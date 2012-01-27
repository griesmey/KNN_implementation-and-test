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
    test_filename = userid_ + '_test.mf'
    train_filename = userid_ + '_train.mf'
    if dir_.endswith('/') == False:
        dir_ += '/'
    train_mffile_ = open(train_filename, 'w')
    test_mffile_ = open(test_filename, 'w')
    """
    query database for all songs that the user liked or
    disliked and put then in a list
    """
    
    D_videos = get_data.get_user_rat(userid_)
    for song in querysongs_:
        songpath = dir_ + song + '.wav'
        if os.path.isfile(songpath):
            test_mffile_.write(songpath + '\t0\n')
    for song, rating in D_videos.iteritems():
        if song in querysongs_: # don't include test songs 
            continue
        songpath = dir_ + song + '.wav'
        if os.path.isfile(songpath):
            train_mffile_.write(songpath + '\t' + str(rating) + '\n')

    return train_filename, test_filename, D_videos


def create_arff(pathtotrainingfile_, pathtotestingfile_):
    """
    userid_
    dir_ - dir that contains the mf file created
    by this program

    returns str containing name of new file
    """
    sys.path.append(
        '/home/tathagata/SmartPlayerModules/Audio/audiomodules/generator')
    import coeffGenerator
    
    train_arff = coeffGenerator.create_mfccs(pathtotrainingfile_)
    test_arff = coeffGenerator.create_mfccs(pathtotestingfile_)
    coeffGenerator.create_genre_coeffs(train_arff)
    coeffGenerator.create_genre_coeffs(test_arff)
    
    
    return 'stacked_' + train_arff, 'stacked_' + test_arff


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
    train_knn = ''
    song_d = dict()
    trainfile_ = ''
    Loc = '/home/tathagata/UserVideoDownloads/tathagata_vdos/video_downloads/'
    old = os.getcwd()
    os.chdir(DATADIR_)
    train_name, test_name, song_d = create_mf(userid_, videos_, Loc)
    train_knn, test_name = create_arff(train_name, test_name)
    knn_file = format_arff(train_knn, song_d)
    os.chdir(old)
    print(DATADIR_ + knn_file)
    print(DATADIR_ + test_name)
    return DATADIR_ + knn_file, DATADIR_ + test_name

if __name__ == "__main__":
    L = []
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
    trainname, testname, D = create_mf(user, L, Loc)
    trainname, testname = create_arff(trainname, testname)
    knn_file = format_arff(trainname, D)
    print(knn_file)
    print(testname)
