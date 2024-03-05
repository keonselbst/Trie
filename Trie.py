class TrieNode:
    def __init__(self):
        self.children = [None] * 26
        self.isEndOfWord = False


class TrieTree:
    def __init__(self):
        self.root = self.getNode()

    def getNode(self):
        return TrieNode() # для создания новых узлов

    def insert(self, key):
        pCrawl = self.root
        for i in range(len(key)):
            index = ord(key[i]) - ord('a') #добавляется в дерево. индекс буквы вычисляется по букве 'a'
            if not pCrawl.children[index]:
                pCrawl.children[index] = self.getNode()# если отсутствует, создается
            pCrawl = pCrawl.children[index] #переход
        pCrawl.isEndOfWord = True

    def search(self, key):
        pCrawl = self.root
        for i in range(len(key)):
            index = ord(key[i]) - ord('a')
            if not pCrawl.children[index]: # если отсутствует
                return False
            pCrawl = pCrawl.children[index] #перемещается к следующему
        if pCrawl.isEndOfWord:
            return True
        else:
            return False

    def remove(self, key):
        if not self.search(key): #проверка на ключ
            return False

        pCrawl = self.root
        for i in range(len(key)): # каждая буква ключа проверяется поочередно
            index = ord(key[i]) - ord('a')
            pCrawl = pCrawl.children[index]
        if pCrawl.children: # Если есть дочерние узлы - фолс
            pCrawl.isEndOfWord = False
        else:
            len_word = len(key) # от конца до начала ключа deleting
            while True: # Цикл до тех пор, пока есть дочерние узлы
                for i in range(len_word):
                    index = ord(key[i]) - ord('a')
                    pCrawl = pCrawl.children[index]
                if not pCrawl.children:
                    del pCrawl
                    len_word -= 1
                else:
                    break

    def del_even_words(self):
        even_words = []
        for i in range(26):
            pCrawl = self.root
            word = '' # Создается пустая строка
            letter_counter = 0 #для отслеживания количества букв в слове
            if pCrawl.children[i]:
                pCrawl = pCrawl.children[i]
                word += chr(ord('a') + i) # добавляем букву, ув. count
                letter_counter += 1
                if pCrawl.children:
                    self._find_even_words(pCrawl, word, even_words, letter_counter)
        for even_word in even_words: #Для каждого найденного слова
            self.remove(even_word)

    def _find_even_words(self, pCrawl, word, even_words, letter_counter): # рекурсивно ищет слова
        for i in range(26):
            if pCrawl.children[i]:
                pCrawl = pCrawl.children[i]
                word += chr(ord('a') + i) #Добавляем букву к слову и ув. count
                letter_counter += 1
                if pCrawl.isEndOfWord: #Если конец и четное, то в список even_words
                    if (word not in even_words) and (letter_counter % 2 == 0):
                        even_words.append(word)
                if pCrawl.children:
                    self._find_even_words(pCrawl, word, even_words, letter_counter)

    def print_tree(self):
        visited = []
        for i in range(26):
            pCrawl = self.root
            word = ''
            if pCrawl.children[i]:
                pCrawl = pCrawl.children[i]
                word += chr(ord('a') + i)
                if pCrawl.isEndOfWord:
                    if word not in visited:
                        visited.append(word) #Если не посещено, добавляем в список
                if pCrawl.children:
                    self._print_word(pCrawl, word, visited)
        for i in range(len(visited)):
            print(visited[i])
        return visited # После обхода всех слов в списке = print

    def _print_word(self, pCrawl, word, visited):
        for i in range(26):
            if pCrawl.children[i]:
                pCrawl = pCrawl.children[i]
                word += chr(ord('a') + i)
                if pCrawl.isEndOfWord:
                    if word not in visited: # Если конец и не посещено слово
                        visited.append(word)
                if pCrawl.children:
                    self._print_word(pCrawl, word, visited)


if __name__=='__main__':
    with open('input.txt') as f:
        contents = f.read()
    f.close

    keys = []
    k = ''
    for i in range(len(contents)):
        if contents[i] != ' ':
            k += contents[i]
        else:
            keys.append(k)
            k = ''
    keys.append(k)

    trie = TrieTree()
    for key in keys:
        trie.insert(key)

    print("Trie initialized with words from file.")
    while True:
        print("\n1. Insert new word")
        print("2. Delete word")
        print("3. Search word")
        print("4. Print tree")
        print("5. Deleting even words")
        print("6. Write a tree to a file")
        print("7. Exit")

        choice = input("Enter choice: ")

        if choice == '1':
            word = input("Enter word to insert: ")
            trie.insert(word)
            print("Word inserted into trie.")
        elif choice == '2':
            word = input("Enter word to delete: ")
            trie.remove(word)
            print("Word deleted from trie.")
        elif choice == '3':
            word = input("Enter word to search: ")
            if trie.search(word):
                print("Word found in trie.")
            else:
                print("Word not found in trie.")
        elif choice == '4':
            print("Words in trie-tree:")
            trie.print_tree()
        elif choice == '5':
            trie.del_even_words()
            print("Word deleted from trie.")
        elif choice == '6':
            with open('output.txt', 'w') as f:
                for word in trie.print_tree():
                    f.write(f'{word} ')
            f.close()
        elif choice == '7':
            break
        else:
            print("Invalid choice. Please try again.")