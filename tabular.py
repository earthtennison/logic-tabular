# this program will simplified the logic function using tabular method for any number of variable.
import copy
import itertools


def count_1(ss):
    return sum(1 for s in ss if s == '1')


def dec_to_bin(i):
    return bin(i).replace("0b", "").zfill(len(VARIABLES))


def diff_1_place(p1, p2):
    """usage: print(diff_1_place("1001", "1000"))"""
    misplace = 0
    misplace_index = -1
    for index, (bit1, bit2) in enumerate(zip(p1, p2)):
        if bit1 != bit2:
            misplace += 1
            misplace_index = index
        if misplace > 1:
            return False
    if misplace == 1:
        return p1[:misplace_index] + 'x' + p1[misplace_index + 1:]


def display_list(p_list):
    for i in range(len(p_list)):
        print("#" * 10, "list ", i + 1, "#" * 10)
        for j in range(len(p_list[i])):
            for k in range(len(p_list[i][j])):
                print(p_list[i][j][k])
            print("- " * 10)


# find essential prime implicants
def find_essential():
    global essentials, prime_implicant_list

    # delete minterm in dont cares
    delete_minterms(DONTCARES)

    deleted_minterms = []
    for m in MINTERMS:
        minterm_count = 0
        essential_prime_implicant = None
        for prime_implicant in prime_implicant_list:
            if m in prime_implicant[0]:
                minterm_count += 1
                essential_prime_implicant = copy.deepcopy(prime_implicant)

        if minterm_count == 1:
            if essential_prime_implicant not in essentials:
                essentials.append(copy.deepcopy(essential_prime_implicant))

            for d in essential_prime_implicant[0]:
                if d not in deleted_minterms:
                    deleted_minterms.append(d)
    delete_minterms(deleted_minterms)


def delete_minterms(deleted_minterms):
    # delete minterm in prime implicant
    global prime_implicant_list
    for m in deleted_minterms:
        for prime_implicant in prime_implicant_list:
            if m in prime_implicant[0]:
                prime_implicant[0].remove(m)
            if len(prime_implicant[0]) == 0:
                prime_implicant_list.remove(prime_implicant)


def check_row():
    global prime_implicant_list
    # check dominating row
    deleted_prime_implicants = []
    for p1, p2 in itertools.combinations(prime_implicant_list, 2):
        # print(p1,p2)
        if set(p1[0]).issubset(set(p2[0])) and p1[3] == p2[3] and p1[0] != p2[0]:
            prime_implicant_list.remove(p1)
        elif set(p2[0]).issubset(set(p1[0])) and p1[3] == p2[3] and p1[0] != p2[0]:
            prime_implicant_list.remove(p2)


def check_column():
    global prime_implicant_list
    # check dominating column
    present_minterms = {}
    for index, prime_implicant in enumerate(prime_implicant_list):
        minterms = prime_implicant[0]
        for m in minterms:
            if m not in present_minterms.keys():
                present_minterms[m] = [index]
            else:
                present_minterms[m].append(index)

    key_list = list(present_minterms.keys())
    val_list = list(present_minterms.values())
    deleted_minterms = []
    for p1_indice, p2_indice in itertools.combinations(present_minterms.values(), 2):
        # print(p1,p2)
        if set(p1_indice).issubset(set(p2_indice)):
            deleted_minterms.append(key_list[val_list.index(p2_indice)])
        elif set(p2_indice).issubset(set(p1_indice)):
            deleted_minterms.append(key_list[val_list.index(p1_indice)])

    delete_minterms(deleted_minterms)


def bit_to_variable(bits):
    out = ""
    for i, bit in enumerate(bits):
        if bit == '0':
            out += VARIABLES[i] + "'"
        elif bit == '1':
            out += VARIABLES[i]
        elif bit == 'x':
            pass
    return out


if __name__ == "__main__":
    # declare the function we need to optimize

    # ['w', 'x', 'y', 'z']
    VARIABLES = ['w', 'x', 'y', 'z']

    # [2, 3, 6, 9, 10, 11, 14, 15]
    MINTERMS = [2, 3, 6, 9, 10, 11, 14, 15]

    # [1, 7, 8]
    DONTCARES = [1, 7, 8]

    # 1) create list of logic combination

    all_terms = sorted(MINTERMS + DONTCARES)

    first_implicant_lists = []
    ref_implicant = dec_to_bin(0)
    if 0 in all_terms:
        first_implicant_lists.append([[[0], dec_to_bin(0), False]])
    # create first list
    for i in range(len(VARIABLES)):
        implicant_list = []
        for m in all_terms:
            if count_1(dec_to_bin(m)) == i + 1:
                implicant_list.append([[m], dec_to_bin(m), False])
        first_implicant_lists.append(implicant_list)

    # create next lists
    combine_implicant_lists = [first_implicant_lists]
    for list_index in range(len(first_implicant_lists) - 1):
        implicant_lists = []
        for i in range(len(combine_implicant_lists[list_index]) - 1):
            implicant_list = []
            implicant_list_1, implicant_list_2 = combine_implicant_lists[list_index][i], \
                                                 combine_implicant_lists[list_index][i + 1]
            for j, implicant_1 in enumerate(implicant_list_1):
                for k, implicant_2 in enumerate(implicant_list_2):
                    new_implicant = diff_1_place(implicant_2[1], implicant_1[1])
                    if new_implicant:
                        implicant_list.append([sorted(implicant_1[0] + implicant_2[0]), new_implicant, False])
                        combine_implicant_lists[list_index][i][j][2] = True
                        combine_implicant_lists[list_index][i + 1][k][2] = True
            implicant_lists.append(implicant_list)
        combine_implicant_lists.append(implicant_lists)

    # filter duplicated implicant lists
    for i in range(len(combine_implicant_lists)):
        for j in range(len(combine_implicant_lists[i])):
            minterm_list = []
            unique_list = []
            for k in range(len(combine_implicant_lists[i][j])):
                if combine_implicant_lists[i][j][k][0] not in minterm_list:
                    unique_list.append(combine_implicant_lists[i][j][k])
                minterm_list.append(combine_implicant_lists[i][j][k][0])

            combine_implicant_lists[i][j] = unique_list

    display_list(combine_implicant_lists)

    # 2) cover table

    # find all prime implicants
    prime_implicant_list = []
    essentials = []
    for i in range(len(combine_implicant_lists)):
        for j in range(len(combine_implicant_lists[i])):
            for k in range(len(combine_implicant_lists[i][j])):
                if combine_implicant_lists[i][j][k][2] == False:
                    new_prime_implicant = combine_implicant_lists[i][j][k]
                    # add list number to compare cost in next step
                    new_prime_implicant.append(i + 1)
                    prime_implicant_list.append(new_prime_implicant)

    iteration = 5
    for i in range(iteration):

        find_essential()
        check_row()
        check_column()

        if len(prime_implicant_list) == 0:
            break

    else:

        present_minterms = {}
        for index, prime_implicant in enumerate(prime_implicant_list):
            minterms = prime_implicant[0]
            for m in minterms:
                if m not in present_minterms.keys():
                    present_minterms[m] = [index]
                else:
                    present_minterms[m].append(index)

        # print(present_minterms)
        multiple_essentials = []

        minterms_left = []
        for m_list in present_minterms.values():
            for m in m_list:
                minterms_left.append(m)

        p_combi_list = list(itertools.combinations(minterms_left, len(present_minterms.keys())))
        # print(p_combi_list)
        for i, key in enumerate(present_minterms.keys()):
            for p_combi in p_combi_list:
                if p_combi[i] not in present_minterms[key]:
                    p_combi_list.remove(p_combi)
        # print(p_combi_list)
        for p_combi in p_combi_list:
            new_essentials = [ess for ess in essentials]
            for p in p_combi:
                new_essentials.append(prime_implicant_list[p])

            multiple_essentials.append(new_essentials)

    if multiple_essentials is not None:
        for essentials in multiple_essentials:
            # display essentials
            output = ""
            for i, ess in enumerate(essentials):
                output += bit_to_variable(ess[1])
                if i < len(essentials) - 1:
                    output += " + "

            print("simplified terms -->", output)

    else:
        # display essentials
        output = ""
        for i, ess in enumerate(essentials):
            output += bit_to_variable(ess[1])
            if i < len(essentials) - 1:
                output += " + "

        print("simplified terms -->", output)
