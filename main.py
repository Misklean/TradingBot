from paper import paper_trading
import json

def main():
    #paper_trading()

    import json
 
    # Opening JSON file
    f = open('mymain.conf')

    # returns JSON object as 
    # a dictionary
    data = json.load(f)

    # print(data["API_KEY"])
    # print(data["API_SECRET_KEY"])
    # print(data["symbols"])

    paper_trading(data["API_KEY"], data["API_SECRET_KEY"])

    # Closing file
    f.close()

main()