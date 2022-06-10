from math import log2, inf
from itertools import islice
from itertools import permutations


def build_profile(residues, sequences):
    num_of_rows = len(residues)
    num_of_columns = len(sequences[0])
    profile = {residues[i]: [2 for _ in range(num_of_columns)]
               for i in range(num_of_rows)}

    scaler = len(sequences) + 2 * num_of_rows
    for col in range(num_of_columns):
        residues_count = {}
        for seq in sequences:
            residue = seq[col]
            if residue in residues_count:
                residues_count[residue] += 1
            else:
                residues_count[residue] = 1

        for i in range(num_of_rows):
            profile[residues[i]][col] += residues_count.get(residues[i], 0)
            profile[residues[i]][col] /= scaler

    for i in range(num_of_rows):
        overall_freq = sum(profile[residues[i]]) / num_of_columns
        for j in range(num_of_columns):
            profile[residues[i]][j] /= overall_freq
            profile[residues[i]][j] = log2(profile[residues[i]][j])

    return profile


def get_score(seq, profile):
    score = 0
    for pos in range(len(seq)):
        score += profile[seq[pos]][pos]
    return score


def window(seq, n=2):
    it = iter(seq)
    result = tuple(islice(it, n))
    if len(result) == n:
        yield result
    for elem in it:
        result = result[1:] + (elem,)
        yield result


def best_subsequence_permutations(long_sequence, profile):
    number_of_columns = len(list(profile.values())[0])
    score_subseq = {}

    for i in range(number_of_columns):
        subsequences = ["".join(x) for x in window(long_sequence, i + 1)]
        for sub in subsequences:
            if i == number_of_columns - 1:
                score_subseq[sub] = get_score(sub, profile)
            else:
                sub += ('-' * (number_of_columns - i - 1))
                for aligned_subsequence in set([''.join(p) for p in permutations(sub)]):
                    if aligned_subsequence.replace('-', '') in long_sequence:
                        score_subseq[aligned_subsequence] = get_score(aligned_subsequence, profile)

    return max(score_subseq, key=score_subseq.get)


def generate_subsequences(ungapped_sub, reach):
    subsequences = {ungapped_sub: 1}
    while reach > 0:
        annex_subs = dict()
        for sub in subsequences:
            for i in range(0, len(sub) + 1):
                new_sub = sub[0:i] + '-' + sub[i:]
                annex_subs[new_sub] = 1
        subsequences = annex_subs
        reach -= 1
    return subsequences


def best_subsequence(long_sequence, profile):
    num_of_columns = len(list(profile.values())[0])
    max_score = -inf
    best_sub = ''
    end = num_of_columns
    while end > 0:
        index = 0
        while index < len(long_sequence):
            ungapped_sub = long_sequence[index:index + end]
            reach = num_of_columns - end
            for sub in generate_subsequences(ungapped_sub, reach):
                score = get_score(sub, profile)
                if max_score < score:
                    best_sub = sub
                    max_score = score
            index += 1
        end -= 1

    return best_sub


def main():
    sequences = []
    n = int(input())
    for i in range(n):
        seq = input()
        sequences.append([residue for residue in seq])

    long_sequence = input()

    residues = set()
    for seq in sequences:
        for residue in seq:
            residues.add(residue)

    profile = build_profile(list(residues), sequences)
    best = best_subsequence(long_sequence, profile)

    print(best)


if __name__ == '__main__':
    main()
