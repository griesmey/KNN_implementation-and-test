import subprocess
import prepare_data

DATADIR_ = '/home/tathagata/SmartPlayerModules\
/Audio/audiomodules/KNN/KNN/KNN_py/data/'


def run_all(userid_, songids_, K):
    """
    runs the prepare_data functions
    to create datasets and then runs the
    knn C++ program to get results written to file and then
    reads the file written to by running the C++ program

    Return: Returns a dict with the songids and the corresponding
            predictions
    """
    trainfile_, testfile_ = prepare_data.run(userid_, songids_)
    print(trainfile_)
    print(testfile_)
    outfile = DATADIR_ + userid_ + '_output'
    command = '/home/tathagata/SmartPlayerModules/Audio/audiomodules/KNN/KNN/KNN_c/knn ' + trainfile_ + ' ' + testfile_ + ' ' + str(K) + '\
     > ' + outfile
    # subprocess.call blocks until command has completed
    subprocess.call(command, 0, None, None, None, None, None, False, True)

    return read_knn_out(outfile)


def read_knn_out(filename_):
    """
    reads file that knn C++ file
    outputs and then returns that data
    as a python dictionary
    """
    ret_d = dict()
    for line in open(filename_):
        myline = line.split()
        ret_d[myline[0]] = myline[1]
    return ret_d


if __name__ == "__main__":
    L = []
    L.append('ZYqSiNf1T_U')
    L.append('ZyiU6PLyBRo')
    L.append('zTl3fGeKgjU')
    L.append('zoCCssAajyA')
    L.append('ZnTCLQWAs8k')
    L.append('ZngfMvCwwFo')
    L.append('ZmsAKIpE12o')
    L.append('zkLlsb10vBk')
    L.append('zkbDBRXUkss')
    L.append('Zjb5o2EbPpY')
    D = dict()
    D = run_all('tathagata', L, 5)
    print(D)
