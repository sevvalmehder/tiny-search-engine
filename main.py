from src.boolean_query_processor import BooleanQueryProcessor
from src.query_processor import QueryProcessor

def run_boolean_query_processor():
    
    # Create query processor object
    bqp = BooleanQueryProcessor()

    while True:
        # Take an input from user
        query = input("Please write a query. ('q' for exit): ")

        if query != 'q':
            print("The result: ", bqp.process(query))
        else:
            break

def run_query_processor():
    # Create query processor object
    qp = QueryProcessor()

    while True:
        # Take an input from user
        query = input("Please write a query. ('q' for exit): ")

        if query != 'q':
            print("The result: ", qp.process(query))
        else:
            break

if __name__ == "__main__":
    
    #run_boolean_query_processor
    run_query_processor()