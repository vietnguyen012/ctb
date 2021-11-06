def process():
    sent_count = 0
    text_line = []
    with open("/root/self-attentive-parser/src/data/VTB_VLSP21_text.txt") as text:
        lines = text.readlines()
        for i,line in enumerate(lines):
            print(i,line)
            if line.strip() != "</s>":
                sent = line[4:].strip()
                underscore_token_text = sent.split()
                nonunscore_token_mapping = {}
                for text in underscore_token_text:
                    if text =="_làm_sao" or text =="_Làm_sao":
                        tls = text[1:].split("_")
                    else:
                        tls = text.split("_")
                    if text not in nonunscore_token_mapping.keys():
                        nonunscore_token_mapping[text] = []
                        for token in tls:
                            nonunscore_token_mapping[text].append(token)
                    else:
                        for token in tls:
                            nonunscore_token_mapping[text].append(token)
                for key,value in nonunscore_token_mapping.items():
                    if len(key.split("_")) < len(value):
                        nonunscore_token_mapping[key] = list(set(value))
                        if len(key.split("_")) > len(set(value)) and len(list(set(value))) == 1 :
                            nonunscore_token_mapping[key] = len(key.split("_"))*list(set(value))
                text_line.append(nonunscore_token_mapping)
            if i == 14806:
                print()
    def find_coressding_word(word_map,phrase):
        for k in word_map.keys():
            if sorted(phrase) == sorted(word_map[k]):
                return k
        return False
    with open("/root/self-attentive-parser/src/data/VTB_VLSP21_tree.txt") as infile:
        treebank = infile.read()
        treebank = treebank[4:-4]
        treebank = treebank.split("\n</s>\n<s>\n")
        start = None
        list_tree = []
        for i,tree in enumerate(treebank):
            tree_tokens = tree.replace("("," ( ").replace(")"," ) ").replace("\n","").strip().split()
            underscore_tree = []
            found = False
            for j,token in enumerate(tree_tokens):
                if i == 3 and token=="chương":
                    print()
                phrase = []
                k=j
                while tree_tokens[k] != ")" and k < len(tree_tokens)-1:
                    phrase.append(tree_tokens[k])
                    k+=1
                find_cor_words = find_coressding_word(text_line[i],phrase)
                if find_cor_words and found == False:
                    underscore_tree.append(find_cor_words)
                    found = True
                elif found == True and token != ")":
                    continue
                else:
                    found = False
                    underscore_tree.append(token)
            list_tree.append(("(TOP " + " ".join(underscore_tree)+")"))
        assert len(text_line) == len(list_tree)
        from random import shuffle
        shuffle(list_tree)
        porp = 0.1
        train_data = list_tree[:int((1-porp)*len(list_tree))]
        val_data = list_tree[int((1-porp)*len(list_tree)):]
        import os
        with open('data/train_tree', 'w') as f1:
            for line in train_data:
                f1.write(line + os.linesep)
            f1.close()
        with open('data/dev_tree', 'w') as f2:
            for line in val_data:
                f2.write(line + os.linesep)
            f2.close()
    infile.close()
if __name__ == "__main__":
    process()