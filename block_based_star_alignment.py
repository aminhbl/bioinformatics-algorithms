import math


def global_align(x, y, s_match=3, s_mismatch=-1, s_gap=-2):
    A = []

    for i in range(len(y) + 1):
        A.append([0] * (len(x) + 1))

    for i in range(len(y) + 1):
        A[i][0] = s_gap * i

    for i in range(len(x) + 1):
        A[0][i] = s_gap * i

    for i in range(1, len(y) + 1):

        for j in range(1, len(x) + 1):
            A[i][j] = max(

                A[i][j - 1] + s_gap,

                A[i - 1][j] + s_gap,

                A[i - 1][j - 1] + (s_match if (y[i - 1] == x[j - 1] and y[i - 1] != '-') else 0) + (

                    s_mismatch if (y[i - 1] != x[j - 1] and y[i - 1] != '-' and x[j - 1] != '-') else 0) + (

                    s_gap if (y[i - 1] == '-' or x[j - 1] == '-') else 0)

            )

    align_X = ""

    align_Y = ""

    i = len(x)

    j = len(y)

    while i > 0 or j > 0:

        current_score = A[j][i]

        if i > 0 and j > 0 and (

                ((x[i - 1] == y[j - 1] and y[j - 1] != '-') and current_score == A[j - 1][i - 1] + s_match) or

                ((y[j - 1] != x[i - 1] and y[j - 1] != '-' and x[i - 1] != '-') and current_score == A[j - 1][

                    i - 1] + s_mismatch) or

                ((y[j - 1] == '-' or x[i - 1] == '-') and current_score == A[j - 1][i - 1] + s_gap)

        ):

            align_X = x[i - 1] + align_X

            align_Y = y[j - 1] + align_Y

            i = i - 1

            j = j - 1

        elif i > 0 and (current_score == A[j][i - 1] + s_gap):

            align_X = x[i - 1] + align_X

            align_Y = "-" + align_Y

            i = i - 1

        else:

            align_X = "-" + align_X

            align_Y = y[j - 1] + align_Y

            j = j - 1

    return align_X, align_Y, A[len(y)][len(x)]


def alignment_score(MSA):
    score = 0
    for i in range(len(MSA[0])):
        for j in range(len(MSA)):
            for k in range(j + 1, len(MSA)):
                if MSA[j][i] == MSA[k][i]:
                    if MSA[j][i] == '-':
                        score += 0
                    else:
                        score += 3

                elif MSA[j][i] != '-' and MSA[k][i] != '-':
                    score += -1
                else:
                    score += -2

    return score


def blocked_star(sequences):
    main_block = star_alignment(sequences)
    new_main_block = main_block

    curr_score = alignment_score(main_block)
    prev_score = -1 * math.inf

    while curr_score > prev_score:

        valid_columns = [False for _ in range(len(main_block[0]))]

        for i in range(len(main_block[0])):
            for j in range(len(main_block)):
                if j + 1 < len(main_block):

                    if main_block[j][i] == '-':
                        valid_columns[i] = True
                        break

                    if main_block[j][i] != main_block[j + 1][i]:
                        valid_columns[i] = True
                        break

        begin = None
        end = None
        block_points = {}
        for i in range(len(valid_columns)):
            if valid_columns[i]:
                if begin is None:
                    begin = i
                else:
                    end = i
            if not valid_columns[i]:
                if end is not None:
                    block_points[begin] = end
                begin = None
                end = None
        if end is not None:
            block_points[begin] = end

        for start, finish in block_points.items():
            finish += 1

            block = {}
            for i in range(len(main_block)):
                block[i] = main_block[i][start:finish].replace('-', '')

            block = star_alignment(block)

            new_main_block = {}
            for j in range(len(main_block)):
                new_main_block[j] = main_block[j][:start] + block[j] + main_block[j][finish:]

            prev_score = curr_score
            curr_score = alignment_score(new_main_block)

            if curr_score > prev_score:
                main_block = new_main_block

    print(curr_score)
    main_block = sorted(main_block.items())
    for seq in main_block:
        print(seq[1])

        
def star_alignment(sequences):
    similarities = {}
    n = len(sequences)
    for i in range(n):
        similarities[i] = {}

    for i in range(n):
        for j in range(i + 1, n):
            seq1, seq2, score = global_align(sequences[i], sequences[j])
            similarities[j][i] = score
            similarities[i][j] = score

    sum_of_pairs = [0 for _ in range(n)]
    for seq in similarities:
        sum_of_pairs[seq] = sum(similarities[seq].values())

    max_SOP = max(sum_of_pairs)
    center_index = sum_of_pairs.index(max_SOP)

    center = sequences[center_index]

    sorted_indices = sorted(similarities[center_index], key=lambda x: similarities[center_index][x], reverse=True)

    last_center = None
    aligned = {}

    for seq_index in sorted_indices:
        seq1, seq2, _ = global_align(sequences[seq_index], center)
        center = seq2

        if last_center is None:
            last_center = center
            aligned[seq_index] = seq1

        else:
            step = 0
            while True:
                if step < min(len(last_center), len(seq2)) and last_center[step] == seq2[step]:
                    step += 1
                elif step < len(seq2):
                    if seq2[step] == '-':
                        for j in aligned:
                            aligned[j] = aligned[j][:step] + '-' + aligned[j][step:]
                        last_center = last_center[:step] + '-' + last_center[step:]
                else:
                    aligned[seq_index] = seq1
                    break

    aligned[center_index] = center
    return aligned


def main():
    n = int(input())
    sequences = {}
    for i in range(n):
        sequences[i] = input()

    blocked_star(sequences)


if __name__ == '__main__':
    main()
