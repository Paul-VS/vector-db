def count_words(file_path):
    with open(file_path, 'r') as file:
        text = file.read()
        words = text.strip().split()
        return len(words)

if __name__ == '__main__':
    file_path = 'sveltekit-docs.txt'    
    word_count = count_words(file_path)
    print("Number of words:", word_count)

