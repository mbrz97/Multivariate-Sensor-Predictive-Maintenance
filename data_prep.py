import os
import openpyxl
import time


def read_excel_files_in_directory(directory_path):
    # Get a list of all files in the directory
    files = os.listdir(directory_path)

    data_dict = {}

    # Iterate through each file in the directory
    for file_name in files:
        data_list = []
        if file_name.endswith('.xlsx'):  # Check if the file is an Excel file
            file_path = os.path.join(directory_path, file_name)
            well_name = os.path.splitext(file_name)[0]

            # Open the Excel file
            workbook = openpyxl.load_workbook(file_path)
            sheet = workbook.active

            # Create a list to store the data from the current sheet
            sheet_data = []

            # Iterate through each row in the sheet and extract data
            for row in sheet.iter_rows(values_only=True):
                listrow = list(row)
                if not sheet_data or listrow[0] != sheet_data[-1][0]:
                    sheet_data.append(list(row))
                else:
                    continue

            # Append the sheet data to the main list

            data_list.append(sheet_data)

            # Close the workbook
            workbook.close()

            data_dict[well_name] = data_list[0]

    return data_dict


def split_healthy_failure(data_well):
    from datetime import datetime

    indices_of_failures = {}
    indices_of_gaps = {}
    num_gaps = 0
    num_fails = 0

    for key, value in data_well.items():
        # mydata = value[0]
        for i in range(len(value)):
            if value[i][5] == "FAILURE":
                num_fails += 1
                if key in indices_of_failures:
                    indices_of_failures[key].append(i)
                else:
                    indices_of_failures[key] = [i]
            if value[i][0] == "GAP":
                num_gaps += 1
                if key in indices_of_gaps:
                    indices_of_gaps[key].append(i)
                else:
                    indices_of_gaps[key] = [i]

    failure_dict = {key: value for key, value in data_well.items() if key in indices_of_failures}
    healthy_dict = {key: value for key, value in data_well.items() if key not in failure_dict}

    for key, value in failure_dict.items():
        temp_val = value
        if key in indices_of_gaps:
            del indices_of_gaps[key]
        for index in sorted(indices_of_failures[key], reverse=True):
            if index < 10:  # new
                temp_val.pop(index)
            failure_dict[key] = temp_val
        del temp_val

    for key, value in failure_dict.items():
        for i in range(len(value)):
            if value[i][0] == "GAP":
                if key in indices_of_gaps:
                    indices_of_gaps[key].append(i)
                else:
                    indices_of_gaps[key] = [i]


    for key, value in failure_dict.items():
        temp_list = value
        for i in range(len(temp_list)):
            if temp_list[i][0] == "GAP":
                continue
            elif i < indices_of_failures[key][0] - 2:
                # x = indices_of_failures[key][0] - 2
                # time_difference = temp_list[x][0] - temp_list[i][0]
                # total_min = int(time_difference.total_seconds() / 3600)
                temp_list[i].append(i)
            else:
                failure_dict[key] = temp_list[:i]
                break
        del temp_list



    # for key, value in failure_dict.items():
    #     temp_val1 = value
    #     if key in indices_of_gaps:
    #         for index in sorted(indices_of_gaps[key], reverse=True):
    #             temp_val1.pop(index)
    #         failure_dict[key] = temp_val1
    #
    # for key, value in failure_dict.items():
    #     temp_val2 = value
    #     if key in indices_of_failures:
    #         for index in sorted(indices_of_failures[key], reverse=True):
    #             temp_val2.pop(index)
    #         failure_dict[key] = temp_val2

    return healthy_dict, failure_dict, indices_of_failures, indices_of_gaps, num_fails, num_gaps


def split_to_gaps(failure_dict, healthy_dict, gap_index, failure_index):
    # Copying keys without values using the keys() method and iteration
    healthy_dict_split = {key: [] for key in healthy_dict.keys()}
    failure_dict_split = {key: [] for key in failure_dict.keys()}

    # healthy_dict_split = {}
    # failure_dict_split = {}

    for key, value in healthy_dict.items():
        if key in gap_index:
            healthy_dict_split[key].extend([value[0:gap_index[key][0]]])
            if len(gap_index[key]) == 1:
                healthy_dict_split[key].extend([value[gap_index[key][0] + 1:]])
                continue
            else:
                for i in range(len(gap_index[key]) - 1):
                    startIndex = gap_index[key][i] + 1
                    endIndex = gap_index[key][i + 1]
                    # if (startIndex-endIndex) < 10:
                    #     continue
                    # mydata = value[0]
                    # getting data between two gaps
                    healthy_dict_split[key].extend([value[startIndex:endIndex]])
                else:
                    healthy_dict_split[key].extend([value[endIndex + 1:]])
        else:
            healthy_dict_split[key] = [value]

    for key, value in failure_dict.items():
        if key in gap_index:
            failure_dict_split[key].extend([value[0:gap_index[key][0]]])
            if len(gap_index[key]) == 1:
                failure_dict_split[key].extend([value[gap_index[key][0] + 1:]])
                continue
            else:
                for i in range(len(gap_index[key]) - 1):
                    startIndex = gap_index[key][i] + 1
                    endIndex = gap_index[key][i + 1]
                    # if (startIndex-endIndex) < 10:
                    #     continue
                    # mydata = value[0]
                    # getting data between two gaps
                    failure_dict_split[key].extend([value[startIndex:endIndex]])
                else:
                    failure_dict_split[key].extend([value[endIndex + 1:]])
        else:
            failure_dict_split[key] = [value]

    # for key, value in failure_dict.items():
    #     if key in gap_index:
    #         failure_dict_split[key].extend([value[0:gap_index[key][0]]])
    #         for i in range(len(gap_index[key]) - 1):
    #             startIndex = gap_index[key][i] + 1
    #             endIndex = gap_index[key][i + 1]
    #             # mydata = value[0]
    #             # getting data between two gaps
    #             failure_dict_split[key].extend([value[startIndex:endIndex]])
    #         else:
    #             failure_dict_split[key].extend([value[endIndex + 1:]])
    #     else:
    #         failure_dict_split[key] = [value]

    #
    # for key in failure_dict_split.keys():
    #     value = failure_dict[key]
    #     for i in range(len(gap_index[key]) - 1):
    #         startIndex = gap_index[key][i] + 1
    #         endIndex = gap_index[key][i + 1]
    #         # getting data between two gaps
    #         # if key in failure_dict_split:
    #         failure_dict_split[key].extend(value[0][startIndex:endIndex])
    #         # else:
    #         #     failure_dict_split[key] = value[0][startIndex:endIndex]

    # for key, value in failure_dict.items():
    #     for i in range(len(gap_index[key]) - 1):
    #         startIndex = gap_index[key][i] + 1
    #         endIndex = gap_index[key][i + 1]
    #         mydata = value[0]
    #         # getting data between two gaps
    #         failure_dict_split[key].extend(mydata[startIndex:endIndex])

    del healthy_dict_split['bl-08']

    return healthy_dict_split, failure_dict_split


def round_intervals(healthy_dict_split):
    # Assuming time intervals of 10 minutes
    from datetime import datetime
    from datetime import timedelta

    interval = timedelta(minutes=10)
    delta_set = {}
    healthy_dict_n = {}

    for key, value in healthy_dict_split.items():
        delta_set[key] = []
        for i, mlist in enumerate(value):
            if len(mlist) >= 2:
                if isinstance(mlist[1][0], str):
                    print(mlist[1][0])
                if isinstance(mlist[0][0], str):
                    print(mlist[0][0])
                # mlist[i][1] = datetime.strptime(mlist[i][1], '%Y-%m-%d %H:%M:%S')

                # mlist[i][0] = datetime.strptime(mlist[i][0], '%Y-%m-%d %H:%M:%S')

                delta = mlist[1][0] - mlist[0][0]
                delta_set[key].append(delta)
                # if delta == timedelta(seconds=62):
                #     for j in range(len(mlist)):
                #         if j == 0:
                #             continue
                #         else:
                #             mlist[j][0] = mlist[j][0] - timedelta(seconds=j*2)
                #     healthy_dict_n[key][i] = mlist

    return delta_set, healthy_dict_split


def convert_freq(healthy_dict_split):
    from datetime import timedelta
    feature_label = []
    for key, value in healthy_dict_split.items():

        for listoflists in value:
            if len(listoflists) > 450:
                delta = listoflists[1][0] - listoflists[0][0]
                if delta == timedelta(seconds=300):
                    lists_half = listoflists[::2]
                    if len(lists_half) > 435:
                        make_window(feature_label, lists_half)
                elif delta == timedelta(seconds=600):
                    if len(listoflists) > 435:
                        make_window(feature_label, listoflists)
                elif delta == timedelta(seconds=30):
                    lists_30s = listoflists[::20]
                    if len(lists_30s) > 435:
                        make_window(feature_label, lists_30s)
                elif delta == timedelta(seconds=60):
                    lists_60s = listoflists[::10]
                    if len(lists_60s) > 435:
                        make_window(feature_label, lists_60s)
                else:
                    continue
            else:
                continue

    return feature_label


def make_window(feature_labels, list_of_lists, num_features=2, num_labels=1, num_stride=6):
    # Input is the list of lists
    # Assuming frequency of 10 min (600 sec)
    # Features = 2 days
    # Labels = 1 day
    # Stride = 6 hours
    stride = 0

    # for i in range(len(list_of_lists) // (num_stride * 6)):
    while (2 + (stride + num_features * 24 * 6) + num_labels * 24 * 6 + num_stride * 6) < len(list_of_lists):
        stride += num_stride * 6
        feature = list_of_lists[stride:1 + stride + num_features * 24 * 6]
        label = list_of_lists[
                1 + stride + num_features * 24 * 6:2 + (stride + num_features * 24 * 6) + num_labels * 24 * 6]
        feature_labels.append([feature, label])

    return feature_labels


def label_failure(data_well):
    indices_of_failures = {}
    indices_of_gaps = {}
    num_gaps = 0
    num_fails = 0

    for key, value in data_well.items():
        # mydata = value[0]
        for i in range(len(value)):
            if value[i][5] == "FAILURE":
                num_fails += 1
                if key in indices_of_failures:
                    indices_of_failures[key].append(i)
                else:
                    indices_of_failures[key] = [i]

    failure_dict = {key: value for key, value in data_well.items() if key in indices_of_failures}

    for key, value in failure_dict.items():
        temp_val = value
        if key in indices_of_gaps:
            del indices_of_gaps[key]
        for index in sorted(indices_of_failures[key], reverse=True):
            temp_val.pop(index)
            failure_dict[key] = temp_val

    for key, value in failure_dict.items():
        for i in range(len(value)):
            if value[i][0] == "GAP":
                if key in indices_of_gaps:
                    indices_of_gaps[key].append(i)
                else:
                    indices_of_gaps[key] = [i]

    return healthy_dict, failure_dict, indices_of_failures, indices_of_gaps, num_fails, num_gaps


if __name__ == "__main__":
    # Replace 'directory_path' with the path to the directory containing the Excel files
    excel_path = r'D:\AI\naft\code wells only\excel wells'

    # Record the start time
    start_time = time.time()

    # Call the function
    data_well = read_excel_files_in_directory(excel_path)

    # Record the end time
    end_time = time.time()

    # Calculate the elapsed time
    elapsed_time = end_time - start_time
    print(f"Time taken to run the code: {elapsed_time:.2f} seconds")

    healthy_well, failure_well, failure_indices, gap_indices, number_of_fails2, number_of_gaps2 = split_healthy_failure(
        data_well)

    # Remove Failures and GAPS in the failure data
    new_failure = {}
    for key, value in failure_well.items():
        my_list = value
        #for i in range(len(value)-1, -1, -1):
        for i in reversed(range(len(value))):
            if my_list[i][0] == "GAP" or my_list[i][5] == "FAILURE":
                my_list.pop(i)
        new_failure[key] = my_list
        del my_list




    #
    # for key, value in failure_well.items():
    #     listolists = value
    #     for index in sorted(failure_indices[key], reverse=True):
    #         listolists.pop(index)
    #     failure_well[key] = listolists

    healthy_dict_splitted, failure_dict_splitted = split_to_gaps(failure_well, healthy_well, gap_indices,
                                                                 failure_indices)

    deltaset, healthy_dict_splitted2 = round_intervals(healthy_dict_splitted)

    lastlist = convert_freq(healthy_dict_splitted)

    deltaset2, failure_dict_splitted2 = round_intervals(failure_dict_splitted)
    failurelist = convert_freq(failure_dict_splitted)

    # with open('output.txt', 'w') as file:
    #     file.write(str(lastlist))

    # import pickle
    # with open('data.pkl', 'wb') as file:
    #     pickle.dump(lastlist, file)
    # =================================================== RUN BELOW

    # or len(lastlist[i][1]) != 145      len(lastlist[i][0]) != 289

    import joblib

    # Save the data using joblib
    joblib.dump(lastlist, 'datalast.joblib')
    joblib.dump(failurelist, 'datafailure.joblib')
    joblib.dump(failure_well, 'failure_well.joblib')
    joblib.dump(new_failure, 'new_failure.joblib')


    def contains_word(lst, word):
        for item in lst:
            if isinstance(item, list):
                if contains_word(item, word):
                    print(item)
                    return True
            elif isinstance(item, str):
                if word in item:
                    print(item)
                    return True
        return False


    word_to_find = "GAP"
    for key, value in healthy_dict_splitted.items():
        if contains_word(value, word_to_find):
            # print(f"The word '{word_to_find}' was found in the nested list.")
            print(key)
        # else:
        #     # print(f"The word '{word_to_find}' was not found in the nested list.")


    def contains_string(data):
        if isinstance(data, str):
            return True
        elif isinstance(data, list):
            return any(contains_string(item) for item in data)
        return False


    # Example usage:
    print(contains_string(failurelist))  # This should print True

    word_to_find = "FAILURE"

    if contains_word(failurelist, word_to_find):
        # print(f"The word '{word_to_find}' was found in the nested list.")
        print("key")
    # else:
    #     # print(f"The word '{word_to_find}' was not found in the nested list.")


    joblib.dump(failure_well, 'failure_all.joblib')
