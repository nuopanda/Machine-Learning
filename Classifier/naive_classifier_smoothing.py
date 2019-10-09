import glob
import math

# smoothing version
def main():
    spam_words_dict = {}
    ham_words_dict = {}
    ham_directory = './data/ham/*.words'
    spam_directory = './data/spam/*.words'
    spam_words_count = 0
    ham_words_count = 0
    spam_files_count = 0
    ham_files_count = 0
    spam_files_count ,spam_words_count = parseFile(spam_words_dict, spam_files_count, spam_words_count, spam_directory)
    ham_files_count, ham_words_count = parseFile(ham_words_dict, ham_files_count, ham_words_count, ham_directory)
    v = 180000
    a = 0.0001
    unseen_log_prob_ham = math.log(a/(v*a + ham_words_count))
    unseen_log_prob_spam = math.log(a/(v*a + spam_words_count))
    calculateLogProb(spam_words_dict, spam_words_count,a, v)
    calculateLogProb(ham_words_dict, ham_words_count, a, v)
    log_prob_ham = math.log(ham_files_count/(ham_files_count + spam_files_count))
    log_prob_spam = math.log(spam_files_count/(ham_files_count + spam_files_count))
        
    # use Test Set to predict 
    test_directory = './data/test/*.words'
    result, spam_list = getTestResult(test_directory, spam_words_dict, ham_words_dict, log_prob_spam,
                             log_prob_ham, unseen_log_prob_ham, unseen_log_prob_spam)
    print(spam_list)
    #calculate precision
    true_spam_list = parseTruthFile()
    precision, recall = calculatePrecision(spam_list, true_spam_list)
    print(precision, recall)
    filename = "./resulttable.csv"
    writeResultTable(filename, result, true_spam_list)

def parseFile(dict, type_count, words_count, directory):
    for filename in glob.glob(directory):
        f = open(filename)
        type_count += 1
        for line in f.readlines():
            words_count += 1
            if line in dict.keys():
                dict[line] += 1
            else:
                dict[line] = 1
    return type_count, words_count
        
def calculateLogProb(dict, count, a , v):
    for i in dict.keys():
        prob = (dict[i] + a) /(count + v * a)
        dict[i] = math.log(prob, 2)
        
def getTestResult(directory, spam_dict, ham_dict, log_prob_spam, log_prob_ham,
                 unseen_log_prob_ham, unseen_log_prob_spam):
    result = {}
    for filename in glob.glob(directory):
        f = open(filename)
        key = filename[filename.rfind("/")+1 : filename.rfind(".")]
        sum_log_prob_ham = 0
        sum_log_prob_spam = 0
        for line in f.readlines():
            if (line in spam_dict and line in ham_dict):
                sum_log_prob_ham += ham_dict[line]
                sum_log_prob_spam += spam_dict[line]
            elif (line in spam_dict and line not in ham_dict):
                sum_log_prob_ham += unseen_log_prob_ham
                sum_log_prob_spam += spam_dict[line]
            elif (line in ham_dict and line not in spam_dict):
                sum_log_prob_spam += unseen_log_prob_spam
                sum_log_prob_ham += ham_dict[line]
        sum_log_prob_ham += log_prob_ham
        sum_log_prob_spam += log_prob_spam
        if (sum_log_prob_ham >= sum_log_prob_spam):
            result[int(key)] = "ham"
        else:
            result[int(key)] = "spam"
    # for i in sorted (result.keys()) :  
    #     print(i, result[i])
    spam_list = []
    for i in result.keys():
        if (result[i] == "spam"):
            spam_list.append(int(i))
    spam_list.sort(reverse=False)
    # print(spam_list)
    return result, spam_list

def parseTruthFile():
    true_spam_list = []
    f = open("./data/truthfile.txt", "r")
    for line in f.readlines():
        true_spam_list.append(int (line))
    print(true_spam_list)
    return true_spam_list
    
def calculatePrecision(spam_list, true_spam_list):
    true_number = 0
    true_spam_size = len(true_spam_list)
    spam_list_size = len(spam_list)
    for i in spam_list:
        if i in true_spam_list:
            true_number += 1
    precision = true_number/true_spam_size
    recall = true_number/spam_list_size
    return precision, recall

def writeResultTable(filename, result, true_spam_list):
    file = open(filename,"w")
    for i in sorted (result.keys()): 
        truth = ""
        if (i in true_spam_list):
            truth = " spam"
        else:
            truth = " ham"
        line = str(i) + " " + result[i] + truth +"\n"
        file.writelines(line) 
    file.close()


main()
