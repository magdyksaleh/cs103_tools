#BY MAGDY SALEH
#DATE: 24/02/2019

import collections
import argparse
import random
import csv
import sys


def read_txt_file(filename):
    student_data = collections.defaultdict(list)
    #read filename from command line
    with open(filename) as raw_file:
        for line in raw_file:
            line = line.strip().split(",")
            #remove the filename, line tage that is printed to js console
            line[-1] = line[-1].split(" ")
            line[-1] = " ".join(line[-1])
            #Bug with cfg feedback on sets problem
            if len(line) > 5:
                line[4] += ",".join(line[5:])
                line = line[:5] 
            (sunet_id, email, problem_id, score, feedback) = line
            student_data[(sunet_id, email)].append((problem_id, score, feedback))
    return student_data


def create_labels(question_ids):
    # output csv file format needs to of the form:
    # sunet, email, [question_score, question_feedback] <-> for each question
    """
    Generates the assignments labels (first line of csv) from txt file
    """
    labels = ["sunet", "email"]
    for question_id in question_ids:
        labels.extend([question_id, "{} - Comment".format(question_id)])
    print("________________________________________")
    print(labels)
    print("________________________________________")
    ret = input("Creating the folliwng rows - Please ensure that they are correct [Y/n]: ")
    if ret != "Y":
        print("There is something wrong with question ids - please fix them in the txt2csv.py file in the create labels function.")
        sys.exit()
    return labels

def create_csv_data_rows(labels, student_data, q_ids, default_if_missing):
    csv_rows = [labels]
    for item in student_data.items():
        sunet_id, email = item[0]
        score_info = item[1]
        csv_line = [sunet_id, email]
        student_score = {q_id: (score, feedback) for q_id, score, feedback in score_info}


        [csv_line.extend(list(student_score.get(q_id, (0, default_if_missing)))) for q_id in q_ids]
        csv_rows.append(csv_line)
    
    return csv_rows

def adjust_csv_rows(csv_rows, new_scores):
    """Adjust scores by qId
    
    Arguments:
        csv_rows {list} 
        new_scores {list}
    """

    for i, row in enumerate(csv_rows):
        if i == 0: continue
        for j, new_score in enumerate(new_scores):
            if int(csv_rows[i][2+2*j]) == 0:
                continue
            csv_rows[i][2+2*j] = new_score
    
    return csv_rows


def test_csv_rows(csv_rows):
#enusre same lengths 
# TODO: make better
    i1, i2 = random.randint(0, len(csv_rows)-1), random.randint(0, len(csv_rows)-1)
    try:
        assert(len(csv_rows[i1]) == len(csv_rows[i2]))
    except:
        print(csv_rows[i1])
        print(csv_rows[i2])
        print("lengths don't match")
        sys.exit()

def write2csv(csv_rows, csv_filename):
    with open(csv_filename, "w+") as writeFile:
        writer = csv.writer(writeFile)
        writer.writerows(csv_rows)

def main():
    # TODO: need to store problem specific information in read_txt_file as we are losing info-- see 
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    args = parser.parse_args()
    print("Reading raw input from:", args.filename)
    student_data = read_txt_file(args.filename)
    
    #change based on pset
    q_ids = ['PS6.6i', 'PS6.6ii', 'PS6.6iii', 'PS6.7ii']
    new_scores = [2, 3, 3, 3]
    
    print("Here are the questions and number of points per question:\n")
    print(list(zip(q_ids, new_scores)))
    ret = input("\nPlease confirm that they are correct [Y/n]: ")
    if ret != "Y":
        print("Please fix the questions ids / scores in the txt2csv.py file itself!")
        sys.exit()



    labels = create_labels(q_ids)
    csv_rows = create_csv_data_rows(labels, student_data, q_ids, "N/A")
    csv_rows = adjust_csv_rows(csv_rows, new_scores)
    test_csv_rows(csv_rows)
    csv_filename = args.filename.split(".")[0] + ".csv" #switch extension to .csv
    write2csv(csv_rows, csv_filename)
    print("\nDone!")

if __name__ == "__main__":
    main()
   
   
   
   
   
   
   
   



