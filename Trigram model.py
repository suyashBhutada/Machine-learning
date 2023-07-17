      def guess(self, word): # word input example: "_ p p _ e "
        ###############################################
        # Replace with your own "guess" function here #
        ###############################################

        # clean the word so that we strip away the space characters
        # replace "_" with "." as "." indicates any character in regular expressions
        clean_word = word[::2].replace("_","_")
        unigram_counts = None


        # Build unigram model. Count character frequency.
        def unigram(corpus):
            unigram_counts = Counter()
            for word in corpus:
                for char in word:
                    unigram_counts[char] += 1
            return unigram_counts

        unigram_counts = unigram(self.full_dictionary)

        def unigram_guesser(mask, guessed, unigram_counts ):
          copy_dict = unigram_counts.copy() 
          for char in guessed:
              del copy_dict[char]
          return max(copy_dict, key=copy_dict.get)
          
        bigram_counts = None

        # add $ to the front of a word since this is a Bigram Model.
        def convert_word(word):
            return "$" + word

        # Collect bigram counts. Because we don't delete keys in dictionary and counter will return 0 for unseen pattern,
        # we don't need to add char for dictionary as Unigram Based on Word Length approach.
        def bigram(corpus):
            bigram_counts = defaultdict(Counter)
            for word in corpus:
                word = convert_word(word)
                # generate a list of bigrams
                bigram_list = zip(word[:-1], word[1:])
                # iterate over bigrams
                for bigram in bigram_list:
                    first, second = bigram
                    bigram_counts[first][second] += 1
            return bigram_counts
        bigram_counts = bigram(self.full_dictionary)

        def bigram_prob(key, char, bigramcounts):
          prev_word_counts = bigramcounts[key]
          total_counts = float(sum(prev_word_counts.values()))
          return prev_word_counts[char] / float(sum(prev_word_counts.values()))

        def bigram_guesser(mask, guessed, bigram_counts=bigram_counts, unigram_counts=unigram_counts): # add extra arguments if needed
          # available is a list that does not contain the character in guessed
          available = list(set(string.ascii_lowercase) - set(guessed))
          
          # The probabilities of available character
          bigram_probs = []
          
          for char in available:
              char_prob = 0
              for index in range(len(mask)):
                  # The first case is that the first char has not been guessed
                  if index == 0 and mask[index] == '_':
                      char_prob +=  bigram_prob('$', char, bigram_counts)
                  # The second case is that the other chars have not been guessed
                  elif mask[index] == '_':
                      # if the previous word has been guessed apply bigram
                      if not mask[index - 1] == '_':
                          char_prob +=  bigram_prob(mask[index - 1], char, bigram_counts)
                      # If the previous word has not been guessed apply unigram
                      else:
                          char_prob +=  unigram_counts[char] / float(sum(unigram_counts.values()))
                      
                  # The final case is that the character is guessed so we skip this position
                  else:
                      continue
              bigram_probs.append(char_prob)
          # Return the max probability of char
          return available[bigram_probs.index(max(bigram_probs))]
        # add $$ to the front of a word
        def trigram_convert_word(word):
            return "$$" + word

        # collect trigram counts
        def trigram(corpus):
            trigram_counts = Counter()
            bigram_counts = defaultdict(Counter)
            
            for word in corpus:
                word = trigram_convert_word(word)
                
                # generate a list of trigrams
                trigram_list = zip(word[:-2], word[1:-1], word[2:])
                
                # generate a list of bigrams
                bigram_list = zip(word[:-1], word[1:])
                
                # iterate over trigrams
                for trigram in trigram_list:
                    first, second, third = trigram
                    element = first+second+third
                    trigram_counts[element] += 1
                    
                # iterate over bigrams
                for bigram in bigram_list:
                    first, second = bigram
                    bigram_counts[first][second] += 1
                    
            return trigram_counts, bigram_counts
        trigram_counts, bigram_counts_for_trigram = trigram(self.full_dictionary)

        # Calculate trigram probability
        def trigram_prob(wi_2, wi_1, char, trigram_counts, bigram_counts):
            return trigram_counts[wi_2 + wi_1 + char] / float(bigram_counts[wi_2][wi_1])
        print(trigram_counts)
        
        def my_amazing_ai_guesser(mask, guessed, bigram_counts=bigram_counts_for_trigram, trigram_counts=trigram_counts, 
                          unigram_counts=unigram_counts):
            # available is a list that does not contain the character in guessed
            available = list(set(string.ascii_lowercase) - set(guessed))
            # The probabilities of available character
            trigram_probs = []
            # if len(mask) = 1, means that there is only a character. Therefore, need to pad in order to avoid error from 
            # traverse mask[index -2] and mask[index -1] 
            mask = '$$' + mask
            
            trigram_lambda = 0.6
            bigram_lambda = 0.3
            unigram_lambda = 0.1

            for char in available:
                char_prob = 0
                for index in range(len(mask)):
                    # The first case is that the first char has not been guessed
                    if index == 0 and mask[index] == '_':
                        char_prob += trigram_lambda * trigram_prob('$', '$', char, trigram_counts, bigram_counts)
                    # The second case is that the second char has not been guessed
                    if index == 1 and mask[index] == '_':
                        # If the previous word has been guessed, apply trigram
                        if not mask[index - 1] == '_':
                            char_prob += trigram_lambda * trigram_prob('$', mask[index - 1], char, trigram_counts, bigram_counts)
                        # If the previous word has not been guessed, apply unigram
                        else:
                            char_prob +=  unigram_lambda * unigram_counts[char] / float(sum(unigram_counts.values()))
                    # The third case is that the other chars have not been guessed
                    elif mask[index] == '_':
                        # If wi-2 and wi-1 have been guessed, apply trigram
                        if not mask[index - 2] == '_' and not mask[index - 1] == '_':
                            char_prob += trigram_lambda * trigram_prob(mask[index - 2], mask[index - 1], char, 
                                                                    trigram_counts, bigram_counts)
                        # If wi-2 hasn't been guessed but wi-1 has been guessed, apply bigram
                        elif mask[index - 2] == '_' and not mask[index - 1] == '_':
                            char_prob += bigram_lambda * bigram_prob(mask[index - 1], char, bigram_counts)
                        # If wi-1 hasn't been guessed, apply unigram
                        else:
                            char_prob +=  unigram_lambda * unigram_counts[char] / float(sum(unigram_counts.values()))
                    # The final case is that the character is guessed so we skip this position
                    else:
                        continue
                trigram_probs.append(char_prob)
            # Return the max probability of char
            return available[trigram_probs.index(max(trigram_probs))]

        return( my_amazing_ai_guesser(clean_word,self.guessed_letters) )