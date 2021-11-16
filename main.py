from src.query_processor import QueryProcessor

if __name__=="__main__":

    qp = QueryProcessor()

    while True:
        # Take an imput from user
        query = input("Please write a query. ('q' for exit): ")

        if query != 'q':
            print("The result: ", qp.process(query))
        else:
            break

    