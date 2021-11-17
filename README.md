# simple-search-system
Simple search system that includes inverted index builder and boolean query processor for information retrieval.

## Usage
This program uses Reuters-21578 Dataset. Please place the dataset before build inverted index.  
Also do not forget to add stopwords in `stopwords.txt` file.
## Run
Programs run with 
`python main.py`
command. Program gets input query and print result until `q` is given.
## Examples
4 different query types are implemented:  
1. Conjunction: w1 AND w2 AND w3...AND wn  
    example: oil AND agriculture AND vegetable  
    result: [3950, 5655, 7625, 8003, 9550, 9756, 10720, 14509, 15341, 18403, 20232]  
2. Disjunction: w1 OR w2 OR w3...OR wn  
    example: hate OR love OR cry  
    result: 1895, 3148, 6338, 7366, 8827, 10890, 17099, 17903, 19559]  
3. Conjunction and Negation: w1 AND w2...AND wn NOT wn+1 NOT wn+2 ...NOT wn+m  
    example: oil AND agriculture AND vegetable NOT price  
    result: [3950, 5655, 7625, 8003, 9550, 9756, 10720, 14509, 15341, 20232]  
4. Disjunction and Negation: w1 OR w2...OR wn NOT wn+1 NOT wn+2 ...NOT wn+m  
    example: hate OR love OR cry NOT money NOT price  
    result:  [1895, 3148, 6338, 7366, 8827, 10890, 17099]  