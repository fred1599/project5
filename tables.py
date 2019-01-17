TABLES = {}

TABLES['category'] = (
    "CREATE TABLE IF NOT EXISTS `category` ("
    "  `id` int(11) NOT NULL AUTO_INCREMENT,"
    "  `name` varchar(100) NOT NULL,"
    "  `meal` varchar(2000) NOT NULL,"
    "  PRIMARY KEY (`id`)"
    ") ENGINE=InnoDB")

TABLES['meal'] = (
    "CREATE TABLE IF NOT EXISTS `meal` ("
    "  `id` int(11) NOT NULL AUTO_INCREMENT,"
    "  `product` varchar(100) NOT NULL,"
    "  `grade` varchar(1) NOT NULL,"
    "  `ingredients` varchar(100) NOT NULL,"
    "  `magasin` varchar(100) NOT NULL,"
    "  `url` varchar(1000) NOT NULL,"
    "  PRIMARY KEY (`id`)"
    ") ENGINE=InnoDB")
