/*!40000 ALTER TABLE `customer_country` DISABLE KEYS */;
INSERT INTO `customer_country` VALUES (1,'India'),(2,'USA');
/*!40000 ALTER TABLE `customer_country` ENABLE KEYS */;

/*!40000 ALTER TABLE `customer_state` DISABLE KEYS */;
INSERT INTO `customer_state` VALUES (1,'Gujarat',1),(2,'Maharastra',1),(3,'Texas',2),(4,'Florida',2);
/*!40000 ALTER TABLE `customer_state` ENABLE KEYS */;

/*!40000 ALTER TABLE `customer_city` DISABLE KEYS */;
INSERT INTO `customer_city` VALUES (1,'Ahemedabad',1),(2,'Mumbai',2),(3,'Miami',4),(4,'Houston',3);
/*!40000 ALTER TABLE `customer_city` ENABLE KEYS */;

/*!40000 ALTER TABLE `customer_area` DISABLE KEYS */;
INSERT INTO `customer_area` VALUES (1,'Vejalpur',1),(2,'Navrangpura',1),(3,'Andheri',2),(4,'Bandra',2),(5,'Aventura',3),(6,'Allapattah',3),(7,'Memorial',4);
/*!40000 ALTER TABLE `customer_area` ENABLE KEYS */;


/*!40000 ALTER TABLE `customer_category` DISABLE KEYS */;
INSERT INTO `customer_category` VALUES (1,'Traditional',NULL),(2,'Western',NULL),(3,'Kurti',1),(4,'Sarees',1),(5,'Shirts',2);
/*!40000 ALTER TABLE `customer_category` ENABLE KEYS */;



INSERT INTO `customer_company` VALUES (1,'Paneri Designer & Ladies','F-9, Chandraprabhu Complex, Nr. Maharaj Samos','7383536601','solanki.manish11122@gmail.com','Mr. Manish Solanki',2);
/*!40000 ALTER TABLE `customer_company` ENABLE KEYS */;



/*!40000 ALTER TABLE `customer_gallary` DISABLE KEYS */;
INSERT INTO `customer_gallary` VALUES (1,'Gallary/b3.jpg'),(2,'Gallary/b5.jpg'),(3,'Gallary/b2.jpg'),(4,'Gallary/b1.jpg'),(5,'Gallary/b8.jpg'),(6,'Gallary/b8_IZlfCh8.jpg'),(7,'Gallary/b6.jpg');
/*!40000 ALTER TABLE `customer_gallary` ENABLE KEYS */;

/*!40000 ALTER TABLE `customer_productcolor` DISABLE KEYS */;
INSERT INTO `customer_productcolor` VALUES (1,'Red'),(2,'Blue'),(3,'Green'),(4,'Yellow'),(5,'Purple'),(6,'Black'),(7,'White'),(8,'All Colors');
/*!40000 ALTER TABLE `customer_productcolor` ENABLE KEYS */;


/*!40000 ALTER TABLE `customer_productsize` DISABLE KEYS */;
INSERT INTO `customer_productsize` VALUES (1,'Extra Small'),(2,'Small'),(3,'Medium'),(4,'Large'),(5,'Extra Large'),(6,'All Sizes');
/*!40000 ALTER TABLE `customer_productsize` ENABLE KEYS */;
/*!40000 ALTER TABLE `customer_product` DISABLE KEYS */;
INSERT INTO `customer_product` VALUES (3,'Modern Umbrella Kurti',500,10,0.1,'Modern Umbrella Kurti,Specially Designed and Handmade by us.With great authenticity we offer you this kurti in many materials you like.','ProductImg/1_o5AaQkw.jpg',3,8,1,6),(4,'Stylish Kurti set with dupatta',600,15,0.1,'Black stylish Dress with dupatta.','ProductImg/2.png',3,8,1,6),(5,'Georgette Updown Top',780,5,0.2,'Latest Georgette Updown top is here! In multi colors and in all Sizes with many designs!','ProductImg/28.jpg',5,8,1,6),(6,'Designer Blouse with back design',250,12,0.1,'With embroidery work on blouse having gota patti','ProductImg/7.jpg',4,8,1,6),(7,'Back neck design Blouse',450,5,0.1,'Blouse with backneck design,Trending fashion right now!Available in many colors,materials and sizes.','ProductImg/6.jpg',4,8,1,6),(8,'Authentic blouse design with embroidery',650,2,0.3,'Sleeveless blouse with embroidery and in new style!Have it in your Own way!','ProductImg/11.jpg',4,1,1,3);
/*!40000 ALTER TABLE `customer_product` ENABLE KEYS */;



