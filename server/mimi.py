def mimi_sequence_slow(n: int):
    if n==1:
        return [1,1]
    sequence = [1,1]
    for step in range(2, n+1):
        new_sequence = []
        new_sequence.append(sequence[0])
        for i in range(len(sequence)-1):
            element = sequence[i] + sequence[i+1]
            new_sequence.append(element)
            new_sequence.append(sequence[i+1])
        sequence = new_sequence
    return sequence



# def mimi_sequence_test(n: int):
#     if n == 1:
#         return [1,1]
    

#     final_length = 1 << n
#     sequence = [0] * final_length
#     sequence[0] = sequence[1] = 1
#     length = 2
    
    
#     for step in range (2, n+1):
#         new_length = (1 << step)
#         i = length - 1
#         j = new_length - 1
        
#         sequence[j] = sequence[i]
#         j -= 1
#         i -= 1
        
        
#         while i >= 0:
#             sequence[j] = sequence[i] + sequence[i+1]
#             j -= 1
#             sequence[j] = sequence[i]
#             j -= 1
#             i -= 1
#         length = new_length
        
#     return sequence[:length]


        

def count_n(n):
    if n == 1:
        return 2  # Special case for n=1
    
    # Calculate the length of sequence at step n
    length = 2 ** (n-1) + 1
    
    # Initialize sequence
    seq = [0] * length
    seq[0] = seq[-1] = 1  # First and last elements are 1
    
    # Build sequence step by step
    curr_len = 2
    prev_seq = [1, 1]
    
    for step in range(2, n+1):
        new_seq = [0] * (curr_len * 2 - 1)
        new_seq[0] = new_seq[-1] = 1  # First and last elements are 1
        
        # Fill in the new elements
        for i in range(len(prev_seq)-1):
            new_seq[i*2] = prev_seq[i]  # Copy existing elements
            new_seq[i*2 + 1] = prev_seq[i] + prev_seq[i+1]  # Calculate new elements
        new_seq[-2] = prev_seq[-1]  # Copy last element
        
        prev_seq = new_seq
        curr_len = len(new_seq)
    
    return prev_seq.count(n)


print(count_n(4))


