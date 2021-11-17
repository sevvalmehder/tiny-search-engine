from src.query_processor import QueryProcessor

if __name__=="__main__":

    # Create query processor object
    qp = QueryProcessor()

    while True:
        # Take an input from user
        query = input("Please write a query. ('q' for exit): ")

        if query != 'q':
            print("The result: ", qp.process(query))
        else:
            break

    