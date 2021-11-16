from src.inverted_intex import InvertedIndex

class QueryProcessor:
    def __init__(self) -> None:
        # First creat the inverted index and load the dictionary
        self._index = InvertedIndex()

        if not self._index.load():
            self._index.build()
        
        self._operands = ["AND", "OR", "NOT"]

    def process(self, q):
        bag = []      
        q_tokens = q.split()
        operand = None

        for token in q_tokens:
            if token in self._operands:
                if not bag:
                    print("Please correct your query!")
                    exit()
                operand = token
            else:
                bag.append(self._index.get(token))
                if len(bag) > 1 and operand != None:
                    sub_result = self._operation(bag, operand)
                    if not sub_result:
                        exit()
                    bag.append(sub_result)
                elif len(bag) > 2 and operand == None:
                    print("Please correct your query, there is no operand!")
                    exit()


        return bag.pop()

    def _operation(self, bag, operand):
        if operand == 'AND':
            return self._index.merge(bag.pop(), bag.pop())
        elif operand == 'OR':
            return self._index.union(bag.pop(), bag.pop())
        elif operand == 'NOT':
            r = bag.pop()
            l = bag.pop()
            return self._index.difference(l, r)
        else:
            print("Wrong operator!")
            return None
