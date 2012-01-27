//Author: Robert Griesmeyer                                                             
//Date: 11-17-2010                                                                      
// Purpose: Take in weighted coefficient data and plot them using those points with     
// their respective ratings and then take the k-nearest to determine likes and dislikes\
                                                                                        
// of songs that we are going to call the query set.  We know nothing about the query   
// besides that of their coefficients.                                                  
// In this implemenation the data points are 10 dimentional; each 
//corresponds to a certain                                                                    // genre weight that specifies which of the genres the song is similar to.              
//                                                                                      
#include <iostream>
#include <string>
#include <cstring>
#include <fstream>
#include <cctype>
#include <vector>
#include <map>
#include <stdio.h>
#include <sstream>
using namespace std;

//STANN                                                                                 
#include <sfcnn.hpp>
#include <bruteNN.hpp>
#include <dpoint.hpp>
#include <test.hpp>

typedef reviver::dpoint<float, 10> Point;

/* return true if success                                   *                           
 * points - vector of points to graph in cloud              *                           
 * names - filenames of points                              *
 * classtypes_ - class values for each point                *
 * filename_ - name of arff file that contains              */
bool read_arff(vector<Point> &points, vector<string> &names,
               vector<unsigned int> &classtypes_, char* filename_) {
  ifstream f_plot;
  string lineread;
  vector<float> values;
  f_plot.open(filename_);
  if(f_plot == NULL) perror("Error opening file datafile.");
  else {
    while(getline(f_plot, lineread)) {
      if(*lineread.begin() == '%' && lineread.find("filename") != -1) {
        int start, end;
        long unsigned int classvalue_;
        string id;
	string value;
	string line;
	stringstream iss;
        start = lineread.find_last_of('/') + 1;  // get rid of delim                    
        end = lineread.find_last_of('.');
        id = lineread.substr(start, end - start);
        names.push_back(id);  // insert name                                            

	getline(f_plot, line);
	iss << line;
	while(getline(iss, value, ',')) {
	  values.push_back(atof(value.c_str()));
	}
	iss.clear();
	
	classtypes_.push_back((unsigned int)values.back());  //insert class                             
	values.pop_back();  // get rid of class value
        Point tempPoint(&values[0]);
        points.push_back(tempPoint);  //insert point                                    
	values.clear();
      }
    }
  }
}

int get_majority_vote(vector<unsigned int> classtypes,
                      vector<long unsigned int> k_ind, vector<string> names) {
  int total = 0;
  for(int k = 0; k < k_ind.size(); k++) {
    if(classtypes[k_ind[k]] > 0) {
      total++;
    }
  }
  if(total > (k_ind.size() / 2))
    return 1;
  else
    return 0;
}


int main(int argc, char** argv) {
  vector<Point> train_points;
  vector<string> train_names;
  vector<unsigned int> train_classtypes;
  vector<Point> test_points;
  vector<string> test_names;
  vector<unsigned int> test_classtypes;
  vector<long unsigned int> k_ind;
  char* train = argv[1];
  char* test = argv[2];
  unsigned int K;
  unsigned int NUM_TEST;
  
  read_arff(train_points, train_names, train_classtypes, train);
  read_arff(test_points, test_names, test_classtypes, test);
  if(argc < 3) {
    perror("USAGE: <main> <train_arff> <test_arff> <k>");
    exit(1);
  }
  K = atoi(argv[3]);
  sfcnn<Point, 10, float> NN(&train_points[0], train_points.size());
  for(int i = 0; i < test_points.size(); ++i) {
    NN.ksearch(test_points[i], K, k_ind);
    
    cout << test_names[i] << '\t' <<
      get_majority_vote(train_classtypes, k_ind, train_names) << endl;
  }
  
  return 0;
}
