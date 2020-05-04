"""Dataset : contains information specific to train/test data"""

class Dataset:
    def __init__(self, title="dataset"):
        self.title = title
        self.content = []
        self.nb_entities = 0
        self.labels = []
        self.hash = ""
        return
        
        
    def __repr__(self):
        return {'title "': self.title, '" nEntitities': self.nb_entities, 'lstEntities': self.most_common}
        
        
    def __str__(self):
        """print(obj)"""
        return 'the dataset "'+ self.title +'" has '+ str(self.nb_entities) +' entities.'
    
    
    def get_title(self):
        return self.title
    
    
    def get_content(self):
        return self.content
    
    
    def get_nb_entities(self):
        return self.nb_entities
    
    
    def get_labels(self):
        return self.labels


    def get_hash(self):
        return self.hash
    
    
    def filter_json(self, json_file):
        content = []
        for o in json_file:
            try:
                text = o['text']
                try:
                    entities = o['entities']
                    if not text or not entities : 
                        return

                except:
                    return
            except:
                return
            obj = {'text' : text, 'entities' : entities}
            content.append(obj)
        self.content = content
        return True
    
    
    def is_correct(self):
        """checks if the content of the file is correct"""

        r_str = "((\"[^\"]+\")|(\'[^\']+\'))"
        r_entity = "\[\d+,\s*\d+,\s*" + r_str + "\]"
        for obj in self.content:
            entity = obj['entities']
            if not entity :
                return False
            for e in entity:
                if not re.fullmatch(r_entity, str(e)) or e[0] >= e[1]:
                    return False
        return True
    
    
    def metadata(self):
        """completes the object properties to create metadata"""
        
        labels = []
        nb_entities = 0
        for obj in self.content:
            self.nb_entities += len(obj['entities'])
            for e in obj['entities']:
                labels.append(e[2])
        
        #dictionary of labels ordered by frequency of appearance
        dic = {}
        for word in labels:
            dic.setdefault(word, 0)
            dic[word] += 1
        self.labels = sorted(dic.items() , key = lambda x: x[1], reverse = True)
            
        #MD5 hash - encoded data in hexadecimal format.
        self.hash = hashlib.md5(str(self.content).encode()).hexdigest()
        return self.labels