seeds = ['n1.mydb.net:27017', 'n2.mydb.net:27017', 'n3.mydb.net:27017']
connection = Mongo::ReplSetConnection.new(seeds)
