import glob
import get_data
import run_knn
from math import *


__author__ = 'Robert Griesmeyer'
__date__ = 'May 21st 2011'
__doc__ = """ This module is for the use of accuaracy checking of the\
k-nearest neighbor algorithm execution.  The parts tested are the predictions\
outputted by the recommender system and also an increasing number of k\
per each interation of the algorithm is used to check for higher accuracies relating\
to the varience of the K variable used in the algorithm.  """

videosloc_ = '/home/tathagata/UserVideoDownloads/tathagata_vdos/video_downloads/'


def run_test(username_='tathagata', samplesize=.10, K=5):
    """
    username_ - user in smartplayer.user_rating db table
    samplesize_ - what percentage will be the cutoff for cross validation;
    example:
        .10 - 10% will be test and 90% will be train
    The sample set is changed per each interation of the KNN algorithm;
    Therefore, for a samplesize of .10 the algorithm will run
    10 times while changing the subset which will be the testing set
    and which subset will be the training set.
    RETURN:
        Return values are the RMSE, correct value, incorrect value , respectively.
        
    """
    print '--------- Running Tests and cross validation ----------'
    print 'Size of k = {0}'.format(K)
    print 'Cross validating with partition size: {0}'.format(samplesize)
    pred_d = dict()
    actual_d = dict()
    actual_d = get_data.get_user_rat(username_)
    video_list = glob.glob(videosloc_ + '*.wav')
    testnum_ = len(video_list) * samplesize
    correct = 0
    incorrect = 0
    RMSE_val = 0
    while(len(video_list) != 0):
        test_l = []
        for i in xrange(int(floor(testnum_))):
            test_l.append(video_list.pop().split('/')[-1].replace('.wav', ''))
            if(len(video_list) == 0):
                break
        # run tests
        pred_d = run_knn.run_all(username_, test_l, K)
        for song, pred in pred_d.iteritems():
            print 'Actual {0}: Predicted: {1}'.format(actual_d[song], pred)
            if(int(actual_d[song]) == int(pred)):
                correct += 1
            else:
                incorrect += 1
            
            RMSE_val += (int(pred) - int(actual_d[song]))**2
        del test_l #empty list

    RMSE = sqrt((RMSE_val)/len(actual_d))                 
    return RMSE, correct, incorrect


def run_all_ks(username_='tathagata', samplesize_=0.1):
    """
    Run for k | k = 1 to sqrt(n)
    """
    k_d = {}
    corr_d = {}
    incorr_d = {}
    actual_d = get_data.get_user_rat(username_)
    upto = int(sqrt(len(actual_d)))
    for k in xrange(1, upto):
        k_d[k], corr_d[k], incorr_d[k] = run_test(username_, samplesize_, k)
        if(k == 1 or incorr_d[k] < low_incorr_num):
            bestk = k
            low_incorr_num = incorr_d[k]
            low_RMSE = k_d[k]
        print 'for k = {0} the RMSE was {1}'.format(str(k), str(k_d[k]))
        print 'for k = {0} the correct was {1}'.format(str(k), str(corr_d[k]))
        print 'for k = {0} the incorrect was {1}'.format(str(k), str(incorr_d[k]))
    print 'Best value of k to use is {0}'.format(str(bestk))
    print 'Number of incorrect for this k was {0}'.format(str(low_incorr_num))
    print 'Lowest RMSE was {0}'.format(str(low_RMSE))

    
if __name__ == "__main__":
    """RMSE, correct, incorrect = run_test('tathagata', .1, 22)
    print 'Root mean squared error is {0}'.format(RMSE)
    print 'Number of incorrect predictions: {0}'.format(incorrect)
    print 'Number of correct predictions: {0}'.format(correct)
    """
    run_all_ks()
    
